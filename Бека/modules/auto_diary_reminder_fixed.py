import datetime
import sys
import asyncio
sys.path.append('modules')

from irkutsk_time import get_irkutsk_time

async def setup_diary_reminder_async():
    """Настраивает ежедневное напоминание для дневника в 20:00 (асинхронная версия)"""

    # Время напоминания
    reminder_time = "20:00"

    # Текст напоминания
    reminder_text = "📓 ВРЕМЯ ДЛЯ ДНЕВНИКА!\n\nНе забудьте сделать запись в дневнике о сегодняшнем дне.\n\nЧто интересного произошло сегодня?\nКакие задачи выполнили?\nЧто планируете на завтра?\n\nИспользуйте команду /diary или просто напишите 'дневник'"

    # Настраиваем повторяющуюся задачу
    try:
        # Импортируем здесь, чтобы избежать циклических импортов
        from scheduler_tools import schedule_recurring_task

        result = await schedule_recurring_task(
            time=reminder_time,
            prompt=reminder_text,
            agent_runner=None  # Будет автоматически подставлен
        )

        return {
            "status": "success",
            "message": f"Напоминание для дневника настроено на {reminder_time}",
            "details": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка при настройке напоминания: {str(e)}"
        }

def setup_diary_reminder():
    """Синхронная обертка для настройки напоминания"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(setup_diary_reminder_async())
        loop.close()
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка в синхронной обертке: {str(e)}"
        }

def check_diary_reminder_status():
    """Проверяет статус напоминания для дневника"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']

    # Парсим время
    current_hour = int(current_time.split(':')[0])
    current_minute = int(current_time.split(':')[1])

    reminder_hour = 20
    reminder_minute = 0

    # Вычисляем время до напоминания
    if current_hour < reminder_hour or (current_hour == reminder_hour and current_minute < reminder_minute):
        time_diff = (reminder_hour * 60 + reminder_minute) - (current_hour * 60 + current_minute)
        hours = time_diff // 60
        minutes = time_diff % 60

        if hours > 0:
            time_str = f"через {hours} ч {minutes} мин"
        else:
            time_str = f"через {minutes} мин"
    else:
        time_diff = (24 * 60) - (current_hour * 60 + current_minute) + (reminder_hour * 60 + reminder_minute)
        hours = time_diff // 60
        minutes = time_diff % 60
        time_str = f"завтра через {hours} ч {minutes} мин"

    return {
        "reminder_time": "20:00",
        "current_time": current_time,
        "next_reminder_in": time_str,
        "status": "active"
    }

def get_diary_stats():
    """Получает статистику по дневнику"""
    import os

    diary_file = "data/diary.txt"

    if os.path.exists(diary_file):
        with open(diary_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Считаем количество записей (по датам)
        dates = []
        lines = content.split('\n')
        for line in lines:
            if line.startswith('## '):
                dates.append(line[3:].strip())

        return {
            "exists": True,
            "file_size": os.path.getsize(diary_file),
            "entry_count": len(dates),
            "last_entry": dates[-1] if dates else "нет записей"
        }
    else:
        return {
            "exists": False,
            "message": "Файл дневника не найден"
        }

def get_all_reminders_summary():
    """Получает сводку по всем напоминаниям"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']

    summary = []
    summary.append("📋 СВОДКА ПО ВСЕМ НАПОМИНАНИЯМ:")
    summary.append(f"• Текущее время: {current_time}")
    summary.append("")

    # 1. Напоминание для дневника
    diary_status = check_diary_reminder_status()
    summary.append("📓 НАПОМИНАНИЕ ДЛЯ ДНЕВНИКА:")
    summary.append(f"   • Время: {diary_status['reminder_time']}")
    summary.append(f"   • Следующее: {diary_status['next_reminder_in']}")

    # 2. Напоминания о расписании пар
    summary.append("")
    summary.append("📚 НАПОМИНАНИЯ О РАСПИСАНИИ:")
    summary.append("   • Вечернее: 20:00 (о парах на завтра)")
    summary.append("   • Утренние: 06:00, 07:00, 08:00, 09:00 (о парах на сегодня)")

    # 3. Статистика дневника
    diary_stats = get_diary_stats()
    summary.append("")
    summary.append("📊 СТАТИСТИКА ДНЕВНИКА:")
    if diary_stats['exists']:
        summary.append(f"   • Записей: {diary_stats['entry_count']}")
        summary.append(f"   • Последняя: {diary_stats['last_entry']}")
    else:
        summary.append(f"   • {diary_stats['message']}")

    return "\n".join(summary)

if __name__ == "__main__":
    # Тестируем функции
    print(get_all_reminders_summary())