import datetime
from datetime import timezone, timedelta

def get_irkutsk_time():
    """Возвращает текущее время в Иркутске (UTC+8)"""
    # Иркутское время: UTC+8
    irkutsk_tz = timezone(timedelta(hours=8))

    # Получаем текущее время в UTC
    utc_now = datetime.datetime.now(timezone.utc)

    # Конвертируем в иркутское время
    irkutsk_now = utc_now.astimezone(irkutsk_tz)

    return {
        'date': irkutsk_now.strftime('%Y-%m-%d'),
        'time': irkutsk_now.strftime('%H:%M:%S'),
        'day_of_week': irkutsk_now.strftime('%A'),
        'full_datetime': irkutsk_now.strftime('%Y-%m-%d %H:%M:%S'),
        'is_working_day': irkutsk_now.weekday() < 5,  # Пн-Пт = рабочие дни
        'irkutsk_tz': 'UTC+8'
    }

def check_bus_schedule():
    """Проверяет расписание автобуса 55 для текущего времени"""
    irkutsk_time = get_irkutsk_time()
    current_hour = int(irkutsk_time['time'].split(':')[0])
    current_minute = int(irkutsk_time['time'].split(':')[1])

    # Расписание автобуса 55 из 6 микрорайона (рабочие дни)
    schedule_weekdays = [
        '05:45', '05:55', '06:05', '06:15', '06:25', '06:35', '06:45', '07:05', '07:35', '07:45',
        '08:05', '08:25', '08:45', '09:05', '09:25', '09:45', '10:05', '10:35', '11:05', '11:15',
        '11:35', '11:45', '11:55', '12:05', '12:15', '12:25', '12:55', '13:25', '13:35', '13:55',
        '14:15', '14:35', '15:15', '15:35', '15:55', '16:05', '16:25', '16:55', '17:05', '17:25',
        '17:35', '17:45', '17:55', '18:05', '18:15', '18:25', '18:45', '19:15', '19:25', '20:45'
    ]

    # Расписание на выходные
    schedule_weekends = [
        '05:45', '06:05', '06:25', '06:45', '07:05', '08:05', '08:25', '08:45', '09:05', '10:35',
        '11:35', '11:55', '12:15', '12:55', '13:55', '14:15', '14:35', '16:05', '16:25', '17:25',
        '17:45', '18:05', '18:25', '18:45', '20:45'
    ]

    # Выбираем расписание в зависимости от дня
    schedule = schedule_weekdays if irkutsk_time['is_working_day'] else schedule_weekends

    # Находим ближайшие рейсы
    current_time_str = f"{current_hour:02d}:{current_minute:02d}"
    next_buses = []

    for bus_time in schedule:
        bus_hour = int(bus_time.split(':')[0])
        bus_minute = int(bus_time.split(':')[1])

        # Проверяем, если автобус еще не ушел
        if (bus_hour > current_hour) or (bus_hour == current_hour and bus_minute > current_minute):
            # Вычисляем время ожидания
            wait_minutes = (bus_hour - current_hour) * 60 + (bus_minute - current_minute)
            next_buses.append({
                'time': bus_time,
                'wait_minutes': wait_minutes,
                'arrival': f"через {wait_minutes} минут"
            })
            if len(next_buses) >= 5:  # Показываем 5 ближайших
                break

    return {
        'current_time': irkutsk_time,
        'next_buses': next_buses,
        'schedule_type': 'рабочие дни' if irkutsk_time['is_working_day'] else 'выходные дни'
    }