import json
import re
import traceback
import asyncio
import os
from core.llm import LLMService

class Agent:
    def __init__(self, tools_registry, system_prompt=None):
        self.llm = LLMService()
        self.tools = tools_registry

        # Load system prompt from file if not provided
        if not system_prompt:
            try:
                # Look in root directory now
                with open("system_prompt.txt", "r", encoding="utf-8") as f:
                    self.system_prompt = f.read()
            except Exception as e:
                print(f"Error loading system prompt: {e}")
                self.system_prompt = "You are a helpful AI agent."
        else:
            self.system_prompt = system_prompt

    def _build_prompt(self, history):
        # With Native Function Calling, we don't need to inject descriptions into text
        # But we must ensure the placeholder is handled if it exists
        try:
            system_msg = self.system_prompt.format(tool_descriptions="Tools are provided via API.")
        except Exception as e:
            # Fallback if formatting fails (e.g. braces issues)
            try:
                system_msg = self.system_prompt.replace("{tool_descriptions}", "Tools are provided via API.")
            except:
                system_msg = self.system_prompt

        messages = [{"role": "system", "content": system_msg}]
        messages.extend(history)
        return messages

    async def run(self, user_input, history=None, tool_context=None):
        """
        Main ReAct loop. Yields status updates asynchronously.
        Returns final response text.
        """
        if history is None:
            history = []

        # Add user input to history if it's new
        if not history or history[-1]["role"] != "user":
            history.append({"role": "user", "content": user_input})

        max_turns = 15 # Reduced limit
        turn = 0

        definitions = self.tools.get_definitions()

        while turn < max_turns:
            turn += 1
            yield {"status": "thinking", "message": "Analysing request..."}

            # 1. Call LLM with streaming
            messages = self._build_prompt(history)

            # Use DeepSeek for complex reasoning
            stream_gen = await self.llm.generate(
                messages,
                provider="deepseek",
                model="default",
                stream=True,
                tools=definitions
            )

            response_content = ""
            tool_calls_buffer = [] # List of dicts to reconstruct tool calls

            try:
                async for chunk in stream_gen:
                    delta = None
                    if hasattr(chunk, 'choices') and chunk.choices:
                         delta = chunk.choices[0].delta

                    if delta:
                        # Handle content
                        if delta.content:
                            response_content += delta.content
                            yield {"status": "final_stream", "content": delta.content}

                        # Handle tool calls
                        if delta.tool_calls:
                            for tc in delta.tool_calls:
                                if tc.index is not None:
                                    while len(tool_calls_buffer) <= tc.index:
                                        tool_calls_buffer.append({"id": "", "function": {"name": "", "arguments": ""}, "type": "function"})

                                    current_tc = tool_calls_buffer[tc.index]
                                    if tc.id:
                                        current_tc["id"] += tc.id
                                    if tc.function:
                                        if tc.function.name:
                                            current_tc["function"]["name"] += tc.function.name
                                        if tc.function.arguments:
                                            current_tc["function"]["arguments"] += tc.function.arguments

            except asyncio.CancelledError:
                raise  # Propagate cancellation immediately
            except Exception as e:
                print(f"Error in stream: {e}")
                pass

            # Prepare Assistant Message
            assistant_msg = {"role": "assistant", "content": response_content}
            if tool_calls_buffer:
                assistant_msg["tool_calls"] = tool_calls_buffer

            history.append(assistant_msg)

            # 2. Check for Tool Call
            if tool_calls_buffer:
                for tool_call in tool_calls_buffer:
                    func_name = tool_call["function"]["name"]
                    args_str = tool_call["function"]["arguments"]
                    call_id = tool_call["id"]

                    try:
                        args = json.loads(args_str)
                    except:
                        args = {} # Or handle error

                    yield {"status": "tool_use", "tool": func_name, "args": args}

                    # Execute Tool
                    try:
                        if self.tools.is_async(func_name):
                            coro = self.tools.execute(func_name, tool_context=tool_context, **args)
                            if asyncio.iscoroutine(coro):
                                result = await coro
                            else:
                                result = coro
                        else:
                            result = await asyncio.to_thread(self.tools.execute, func_name, tool_context=tool_context, **args)

                        result_str = str(result)
                    except Exception as e:
                        result_str = f"Error: {str(e)}"

                    # CROP RESULT (Observation)
                    if len(result_str) > 2000:
                        result_str = result_str[:2000] + "... (truncated)"

                    # Append Tool Message (OpenAI format)
                    history.append({
                        "role": "tool",
                        "tool_call_id": call_id,
                        "content": result_str,
                        "name": func_name
                    })

                    result_msg = f"Tool '{func_name}' output:\n{result_str}"
                    yield {"status": "observation", "result": result_msg}

            else:
                # No tool call = Final Answer
                yield {"status": "final", "content": response_content}
                return

        yield {"status": "final", "content": "Error: Maximum turns reached."}
