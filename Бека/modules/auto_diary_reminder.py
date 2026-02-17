import datetime
import sys
sys.path.append('modules')

from irkutsk_time import get_irkutsk_time
from scheduler_tools import schedule_recurring_task

def setup_diary_reminder():
    """Настраивает ежедневное напоминание для дневника в 20:00"""

    # Время напоминания
    reminder_time = "20:00"

    # Текст напоминания
    reminder_text = "📓 ВРЕМЯ ДЛЯ ДНЕВНИКА!\n\nНе забудьте сделать запись в дневнике о сегодняшнем дне.\n\nЧто интересного произошло сегодня?\nКакие задачи выполнили?\nЧто планируете на завтра?\n\nИспользуйте команду /diary или просто напишите 'дневник'"

    # Настраиваем повторяющуюся задачу
    try:
        result = schedule_recurring_task(
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

if __name__ == "__main__":
    # Тестируем функции
    print("📓 НАСТРОЙКА НАПОМИНАНИЯ ДЛЯ ДНЕВНИКА\n")

    # Настраиваем напоминание
    setup_result = setup_diary_reminder()
    print(f"Статус: {setup_result['status']}")
    print(f"Сообщение: {setup_result['message']}")

    print("\n" + "="*50 + "\n")

    # Проверяем статус
    status = check_diary_reminder_status()
    print(f"Текущее время: {status['current_time']}")
    print(f"Время напоминания: {status['reminder_time']}")
    print(f"Следующее напоминание: {status['next_reminder_in']}")

    print("\n" + "="*50 + "\n")

    # Проверяем статистику
    stats = get_diary_stats()
    if stats['exists']:
        print(f"Файл дневника: найден ({stats['file_size']} байт)")
        print(f"Количество записей: {stats['entry_count']}")
        print(f"Последняя запись: {stats['last_entry']}")
    else:
        print(f"Файл дневника: {stats['message']}")