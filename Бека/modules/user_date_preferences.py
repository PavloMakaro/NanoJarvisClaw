#!/usr/bin/env python3
"""
Модуль для учета предпочтений пользователя по дате.
Хранит информацию о том, какой год актуален для пользователя.
"""

from modules.check_current_date import get_current_datetime_info

class UserDatePreferences:
    """
    Управляет предпочтениями пользователя по дате.
    """

    def __init__(self):
        self.preferences = {
            'preferred_year': 2026,  # По умолчанию - текущий системный год
            'year_source': 'system_current',  # system_current, user_specified, historical
            'user_confirmed': False,
            'notes': 'Пользователю нужна информация за 2026 год'
        }

    def update_preferences(self, user_input):
        """
        Обновляет предпочтения на основе ввода пользователя.
        """
        input_lower = user_input.lower()

        # Определяем, какой год нужен пользователю
        if '2026' in input_lower or 'двадцать шест' in input_lower:
            self.preferences['preferred_year'] = 2026
            self.preferences['year_source'] = 'user_specified'
            self.preferences['user_confirmed'] = True
            self.preferences['notes'] = 'Пользователь явно указал 2026 год'

        elif '2024' in input_lower or 'двадцать четвёрт' in input_lower:
            self.preferences['preferred_year'] = 2024
            self.preferences['year_source'] = 'user_specified'
            self.preferences['user_confirmed'] = True
            self.preferences['notes'] = 'Пользователь явно указал 2024 год'

        elif any(word in input_lower for word in ['текущ', 'сейчас', 'сегодн', 'этот год']):
            current_year = get_current_datetime_info().get('year', 2026)
            self.preferences['preferred_year'] = current_year
            self.preferences['year_source'] = 'system_current'
            self.preferences['user_confirmed'] = True
            self.preferences['notes'] = f'Пользователю нужна текущая информация ({current_year} год)'

        return self.preferences

    def get_date_context(self):
        """
        Возвращает контекст даты для ответа.
        """
        current_info = get_current_datetime_info()
        current_year = current_info.get('year', 2026)

        context = {
            'system_year': current_year,
            'preferred_year': self.preferences['preferred_year'],
            'year_source': self.preferences['year_source'],
            'user_confirmed': self.preferences['user_confirmed'],
            'notes': self.preferences['notes'],
            'is_aligned': current_year == self.preferences['preferred_year'],
            'current_date': current_info.get('system_datetime', '2026-02-16')
        }

        return context

    def format_response_intro(self, user_query):
        """
        Форматирует введение для ответа с учетом предпочтений по дате.
        """
        context = self.get_date_context()

        if context['is_aligned']:
            return f"""
✅ **ДАЕТСЯ АКТУАЛЬНАЯ ИНФОРМАЦИЯ:**
📅 Системная дата: {context['current_date']}
🎯 Запрос обрабатывается для {context['preferred_year']} года

"""
        else:
            return f"""
⚠️ **РАСХОЖДЕНИЕ В ДАТАХ:**
📅 Системная дата: {context['current_date']}
🎯 Но вам нужна информация за {context['preferred_year']} год
🔍 Буду искать данные за {context['preferred_year']} год

"""

def get_smart_date_handling_instruction():
    """
    Возвращает умную инструкцию по обработке дат.
    """
    return """

{'='*80}
🎯 **УМНАЯ ОБРАБОТКА ДАТ (ОБНОВЛЕНО 16.02.2026):**

**ПРИНЦИПЫ:**
1. **НЕ ПРЕДПОЛАГАТЬ** какой год "правильный"
2. **СЛУШАТЬ ПОЛЬЗОВАТЕЛЯ** - если сказал "2026", значит 2026
3. **СИСТЕМНАЯ ДАТА МОЖЕТ БЫТЬ КОРРЕКТНОЙ** (сейчас 2026 год)

**АЛГОРИТМ:**
1. Проверить get_current_time() → сейчас 2026-02-16
2. Спросить/уточнить у пользователя:
   • Если запрос о "текущих" событиях → использовать 2026 год
   • Если пользователь указал год → использовать указанный
   • Если неясно → уточнить: "Какой год вас интересует?"

**КОНКРЕТНО ДЛЯ ЭТОГО ПОЛЬЗОВАТЕЛЯ:**
• Ему нужна информация за 2026 год
• Системная дата 2026 корректна для его запросов
• Не нужно "исправлять" дату или предупреждать о "будущем"

**ПРИМЕР:**
Пользователь: "Какие турниры по CS2 идут сейчас?"
Вы: "✅ Ищу актуальную информацию за 2026 год..."
{'='*80}
"""

# Глобальный экземпляр с настройками пользователя
user_date_prefs = UserDatePreferences()

# Обновляем настройки на основе последнего сообщения пользователя
user_date_prefs.update_preferences(
    "Блять а с чего ты взял что мне нужен 24 год мне наоборот нужен 26"
)

if __name__ == "__main__":
    print("=== НАСТРОЙКИ ДАТЫ ПОЛЬЗОВАТЕЛЯ ===")
    prefs = user_date_prefs.get_date_context()
    for key, value in prefs.items():
        print(f"{key}: {value}")

    print("\n" + "="*60)
    print("Пример введения для ответа:")
    print(user_date_prefs.format_response_intro("Какие турниры по CS2 идут сейчас?"))

    print("\n" + get_smart_date_handling_instruction())