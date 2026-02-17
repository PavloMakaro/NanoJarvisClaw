import datetime
from datetime import timezone, timedelta
import json
import os

SCHEDULE_FILE = 'downloads/schedule_data.json'

# Базовое расписание из изображения
BASE_SCHEDULE = {
    'числитель': {
        'ПН': [
            {'time': '8:30-9:50', 'subject': 'МДК ТОРА', 'room': 'след.м 8:30-9:50 Информатика А301'},
            {'time': '10:00-11:20', 'subject': 'Техническая механика', 'room': 'П207'},
            {'time': '11:50-13:10', 'subject': 'ПБДД', 'room': 'П313'}
        ],
        'ВТ': [
            {'time': '8:30-9:50', 'subject': '', 'room': 'каб'},
            {'time': '10:00-11:20', 'subject': 'Английский язык', 'room': 'А107'},
            {'time': '11:50-13:10', 'subject': 'Электротехника', 'room': 'А402'},
            {'time': '13:20-14:40', 'subject': 'Информатика', 'room': 'А301'},
            {'time': '15:00-16:20', 'subject': 'Психология общения', 'room': 'А110'}
        ],
        'СР': [
            {'time': '8:30-9:50', 'subject': 'МДК Устройство авт.', 'room': 'П313'},
            {'time': '10:00-11:20', 'subject': 'Физическая культура', 'room': 'сп.зал'},
            {'time': '11:50-13:10', 'subject': 'Инженерная графика', 'room': 'А111'}
        ],
        'ЧТ': [
            {'time': '8:30-9:50', 'subject': 'МДК Устройство авт.', 'room': 'П313'},
            {'time': '10:00-11:20', 'subject': '', 'room': ''},
            {'time': '11:50-13:10', 'subject': 'Инженерная графика', 'room': 'А111'}
        ],
        'ПТ': [
            {'time': '8:30-9:50', 'subject': 'Электротехника', 'room': 'А402'},
            {'time': '10:00-11:20', 'subject': 'МДК Устройство авт.', 'room': 'П313'},
            {'time': '11:50-13:10', 'subject': 'Основы философии', 'room': 'А207'}
        ],
        'СБ': [
            {'time': '8:30-9:50', 'subject': 'Техническая механика', 'room': 'П207'},
            {'time': '10:00-11:20', 'subject': '', 'room': ''},
            {'time': '11:50-13:10', 'subject': 'ПБДД', 'room': 'П313'},
            {'time': '13:20-14:40', 'subject': 'МДК Материалы авт.', 'room': 'а203'}
        ]
    },
    'знаменатель': {
        'ПН': [
            {'time': '8:30-9:50', 'subject': 'Информатика', 'room': 'А301'},
            {'time': '10:00-11:20', 'subject': 'МДК Материалы авт.', 'room': 'а203'},
            {'time': '11:50-13:10', 'subject': 'Английский язык', 'room': 'А107'}
        ],
        'ВТ': [
            {'time': '8:30-9:50', 'subject': '', 'room': 'каб'},
            {'time': '10:00-11:20', 'subject': 'МДК Устройство авт.', 'room': 'Г313'},
            {'time': '11:50-13:10', 'subject': 'ПБДД', 'room': 'Г313'},
            {'time': '13:20-14:40', 'subject': 'Техническая механика', 'room': 'П207'},
            {'time': '15:00-16:20', 'subject': '', 'room': ''}
        ],
        'СР': [
            {'time': '8:30-9:50', 'subject': 'Физическая культура', 'room': 'сп.зал'},
            {'time': '10:00-11:20', 'subject': 'МДК Устройство авт.', 'room': 'Г313'},
            {'time': '11:50-13:10', 'subject': '', 'room': ''}
        ],
        'ЧТ': [
            {'time': '8:30-9:50', 'subject': 'Инженерная графика', 'room': 'А111'},
            {'time': '10:00-11:20', 'subject': 'Психология общения', 'room': 'Г103'},
            {'time': '11:50-13:10', 'subject': 'ПБДД', 'room': 'Г313'}
        ],
        'ПТ': [
            {'time': '8:30-9:50', 'subject': 'МДК Устройство авт.', 'room': 'Г313'},
            {'time': '10:00-11:20', 'subject': 'МДК ТОРА', 'room': 'след.м'},
            {'time': '11:50-13:10', 'subject': 'Инженерная графика', 'room': 'А111'}
        ],
        'СБ': [
            {'time': '8:30-9:50', 'subject': 'Основы философии', 'room': 'А207'},
            {'time': '10:00-11:20', 'subject': 'МДК Материалы авт.', 'room': 'а203'},
            {'time': '11:50-13:10', 'subject': 'Электротехника', 'room': 'А402'},
            {'time': '13:20-14:40', 'subject': 'МДК Устройство авт.', 'room': 'Г313'}
        ]
    }
}

def get_irkutsk_time():
    """Возвращает текущее время в Иркутске"""
    irkutsk_tz = timezone(timedelta(hours=8))
    utc_now = datetime.datetime.now(timezone.utc)
    irkutsk_now = utc_now.astimezone(irkutsk_tz)

    return {
        'date': irkutsk_now.strftime('%Y-%m-%d'),
        'time': irkutsk_now.strftime('%H:%M'),
        'day_of_week_ru': ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'][irkutsk_now.weekday()],
        'day_of_week': irkutsk_now.strftime('%A'),
        'hour': irkutsk_now.hour,
        'minute': irkutsk_now.minute
    }

def get_current_week_type():
    """Определяет текущий тип недели (числитель/знаменатель)"""
    # По умолчанию - числитель (как вы сказали)
    # Можно будет обновлять через команды
    try:
        with open(SCHEDULE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('current_week_type', 'числитель')
    except:
        return 'числитель'

def set_week_type(week_type):
    """Устанавливает тип недели"""
    data = {'current_week_type': week_type}
    with open(SCHEDULE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"Установлена неделя: {week_type}"

def get_tomorrow_schedule():
    """Возвращает расписание на завтра"""
    now = get_irkutsk_time()
    week_type = get_current_week_type()

    # Определяем день недели завтра
    days_ru = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    today_index = days_ru.index(now['day_of_week_ru'])
    tomorrow_index = (today_index + 1) % 7
    tomorrow_day = days_ru[tomorrow_index]

    # Если воскресенье - нет пар
    if tomorrow_day == 'ВС':
        return {
            'day': tomorrow_day,
            'week_type': week_type,
            'lessons': [],
            'message': 'Завтра воскресенье - выходной!'
        }

    # Получаем расписание
    schedule = BASE_SCHEDULE.get(week_type, {}).get(tomorrow_day, [])

    # Фильтруем пустые пары
    lessons = [lesson for lesson in schedule if lesson.get('subject', '').strip()]

    return {
        'day': tomorrow_day,
        'week_type': week_type,
        'lessons': lessons,
        'count': len(lessons)
    }

def get_today_schedule():
    """Возвращает расписание на сегодня"""
    now = get_irkutsk_time()
    week_type = get_current_week_type()

    # Если воскресенье - нет пар
    if now['day_of_week_ru'] == 'ВС':
        return {
            'day': now['day_of_week_ru'],
            'week_type': week_type,
            'lessons': [],
            'message': 'Сегодня воскресенье - выходной!'
        }

    # Получаем расписание
    schedule = BASE_SCHEDULE.get(week_type, {}).get(now['day_of_week_ru'], [])

    # Фильтруем пустые пары
    lessons = [lesson for lesson in schedule if lesson.get('subject', '').strip()]

    return {
        'day': now['day_of_week_ru'],
        'week_type': week_type,
        'lessons': lessons,
        'count': len(lessons)
    }

def format_schedule_message(schedule_data, title="Расписание"):
    """Форматирует расписание в читаемое сообщение"""
    if not schedule_data['lessons']:
        return f"{title}: {schedule_data.get('message', 'Нет пар')}"

    lines = [f"📚 {title} ({schedule_data['week_type']}, {schedule_data['day']}):"]

    for i, lesson in enumerate(schedule_data['lessons'], 1):
        subject = lesson['subject']
        time = lesson['time']
        room = lesson.get('room', '')

        room_text = f" ({room})" if room else ""
        lines.append(f"{i}. {time} - {subject}{room_text}")

    lines.append(f"\nВсего пар: {schedule_data['count']}")
    return "\n".join(lines)

def check_if_need_reminder():
    """Проверяет, нужно ли отправлять утреннее напоминание"""
    now = get_irkutsk_time()

    # Проверяем время: между 6:00 и 10:00
    if 6 <= now['hour'] < 10:
        schedule = get_today_schedule()
        if schedule['lessons']:
            return {
                'need_reminder': True,
                'message': format_schedule_message(schedule, "⏰ Утреннее напоминание о парах")
            }

    return {'need_reminder': False}
