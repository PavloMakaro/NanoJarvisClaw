import datetime
from datetime import timezone, timedelta
import sys
sys.path.append('modules')

from schedule_reminder import get_tomorrow_schedule, format_schedule_message, get_today_schedule, check_if_need_reminder
from irkutsk_time import get_irkutsk_time

def send_evening_reminder():
    """Отправляет вечернее напоминание о парах на завтра"""
    try:
        # Получаем расписание на завтра
        schedule = get_tomorrow_schedule()

        # Форматируем сообщение
        message = format_schedule_message(schedule, "🌙 Вечернее напоминание на завтра")

        # Добавляем время
        irkutsk_time = get_irkutsk_time()
        message += f"\n\n⏰ Время напоминания: {irkutsk_time['time']}"

        return message
    except Exception as e:
        return f"Ошибка при формировании вечернего напоминания: {str(e)}"

def send_morning_reminder():
    """Отправляет утреннее напоминание о парах на сегодня"""
    try:
        # Проверяем, нужно ли отправлять напоминание
        reminder_check = check_if_need_reminder()

        if reminder_check['need_reminder']:
            return reminder_check['message']
        else:
            # Если не время для утреннего напоминания, все равно показываем расписание
            schedule = get_today_schedule()
            if schedule['lessons']:
                message = format_schedule_message(schedule, "☀️ Утреннее напоминание о парах")
                irkutsk_time = get_irkutsk_time()
                message += f"\n\n⏰ Время: {irkutsk_time['time']}"
                return message
            else:
                return None
    except Exception as e:
        return f"Ошибка при формировании утреннего напоминания: {str(e)}"

def setup_daily_reminders():
    """Настраивает ежедневные напоминания"""
    # Вечернее напоминание в 20:00
    evening_time = "20:00"

    # Утреннее напоминание за 2 часа до первой пары
    # Будем проверять каждый час с 6:00 до 10:00
    morning_check_times = ["06:00", "07:00", "08:00", "09:00"]

    return {
        'evening_reminder': evening_time,
        'morning_check_times': morning_check_times,
        'description': 'Автоматические напоминания о расписании пар'
    }

def check_and_send_reminders():
    """Проверяет и отправляет все необходимые напоминания"""
    messages = []

    # Проверяем утренние напоминания
    morning_msg = send_morning_reminder()
    if morning_msg:
        messages.append(morning_msg)

    # Проверяем вечерние напоминания (после 18:00)
    irkutsk_time = get_irkutsk_time()
    if irkutsk_time['hour'] >= 18:
        evening_msg = send_evening_reminder()
        if evening_msg:
            messages.append(evening_msg)

    return messages

def get_reminder_status():
    """Возвращает статус системы напоминаний"""
    setup = setup_daily_reminders()
    irkutsk_time = get_irkutsk_time()

    status = [
        f"📅 Статус напоминаний о расписании:",
        f"• Текущее время в Иркутске: {irkutsk_time['time']}",
        f"• Вечернее напоминание: {setup['evening_reminder']}",
        f"• Утренние проверки: {', '.join(setup['morning_check_times'])}",
        f"• Система активна и готова к работе!"
    ]

    return "\n".join(status)