import datetime
import os
import sys
sys.path.append('modules')

from irkutsk_time import get_irkutsk_time
from schedule_reminder import get_today_schedule, get_tomorrow_schedule
from auto_schedule_reminders import setup_daily_reminders

def check_all_reminders():
    """Проверяет все активные напоминания в системе"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']

    # Парсим время для получения часа и минуты
    current_hour = int(current_time.split(':')[0])
    current_minute = int(current_time.split(':')[1])

    result = []
    result.append("🔔 АКТИВНЫЕ НАПОМИНАНИЯ В СИСТЕМЕ")
    result.append(f"• Текущее время в Иркутске: {current_time}")
    result.append("")

    # 1. Напоминания о расписании пар
    result.append("📚 1. НАПОМИНАНИЯ О РАСПИСАНИИ ПАР:")
    schedule_reminders = setup_daily_reminders()
    result.append(f"   • Вечернее напоминание: {schedule_reminders['evening_reminder']}")
    result.append(f"   • Утренние проверки: {', '.join(schedule_reminders['morning_check_times'])}")

    # Проверяем, когда будет следующее напоминание
    evening_hour, evening_minute = map(int, schedule_reminders['evening_reminder'].split(':'))
    if current_hour < evening_hour or (current_hour == evening_hour and current_minute < evening_minute):
        time_diff = (evening_hour * 60 + evening_minute) - (current_hour * 60 + current_minute)
        hours = time_diff // 60
        minutes = time_diff % 60
        if hours > 0:
            result.append(f"   • Следующее вечернее напоминание через: {hours} ч {minutes} мин")
        else:
            result.append(f"   • Следующее вечернее напоминание через: {minutes} минут")
    else:
        result.append(f"   • Вечернее напоминание сегодня уже прошло")

    # Проверяем утренние напоминания
    morning_times = schedule_reminders['morning_check_times']
    next_morning = None
    next_morning_diff = None
    for mt in morning_times:
        m_hour, m_minute = map(int, mt.split(':'))
        if current_hour < m_hour or (current_hour == m_hour and current_minute < m_minute):
            time_diff = (m_hour * 60 + m_minute) - (current_hour * 60 + current_minute)
            hours = time_diff // 60
            minutes = time_diff % 60
            if hours > 0:
                next_morning = f"{mt} (через {hours} ч {minutes} мин)"
            else:
                next_morning = f"{mt} (через {minutes} мин)"
            next_morning_diff = time_diff
            break

    if next_morning:
        result.append(f"   • Следующая утренняя проверка: {next_morning}")
    else:
        result.append(f"   • Утренние проверки сегодня уже завершены")

    # 2. Проверяем напоминания из дневника
    result.append("")
    result.append("📓 2. НАПОМИНАНИЯ ДЛЯ ДНЕВНИКА:")
    diary_file = "data/diary.txt"
    if os.path.exists(diary_file):
        with open(diary_file, 'r', encoding='utf-8') as f:
            content = f.read()
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if today in content:
                result.append("   • Запись в дневнике сегодня уже сделана ✓")
            else:
                result.append("   • Запись в дневнике сегодня еще не сделана")
    else:
        result.append("   • Файл дневника не найден")

    # 3. Проверяем одноразовые напоминания (если бы они хранились где-то)
    result.append("")
    result.append("⏰ 3. ОДНОРАЗОВЫЕ НАПОМИНАНИЯ:")
    result.append("   • Для просмотра одноразовых напоминаний нужен доступ к job_queue")
    result.append("   • Обычно они хранятся в памяти бота")

    # 4. Общая информация
    result.append("")
    result.append("📊 ОБЩАЯ ИНФОРМАЦИЯ:")

    # Проверяем расписание на сегодня
    today_schedule = get_today_schedule()
    if today_schedule['lessons']:
        result.append(f"   • Сегодня пар: {len(today_schedule['lessons'])}")
        first_lesson = today_schedule['lessons'][0]
        result.append(f"   • Первая пара: {first_lesson['time']} - {first_lesson['subject']}")
    else:
        result.append("   • Сегодня пар нет")

    # Проверяем расписание на завтра
    tomorrow_schedule = get_tomorrow_schedule()
    if tomorrow_schedule['lessons']:
        result.append(f"   • Завтра пар: {len(tomorrow_schedule['lessons'])}")
    else:
        result.append("   • Завтра пар нет")

    return "\n".join(result)

def get_reminder_summary():
    """Краткая сводка по напоминаниям"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']
    current_hour = int(current_time.split(':')[0])
    current_minute = int(current_time.split(':')[1])

    summary = []
    summary.append("📋 СВОДКА ПО НАПОМИНАНИЯМ:")

    # Определяем тип дня
    if current_hour < 12:
        summary.append("• Сейчас утро, будут утренние напоминания о парах")
    elif current_hour < 18:
        summary.append("• Сейчас день, напоминаний нет до вечера")
    else:
        summary.append("• Сейчас вечер, скоро вечернее напоминание о парах на завтра")

    # Проверяем вечернее напоминание
    evening_time = "20:00"
    evening_hour, evening_minute = map(int, evening_time.split(':'))

    if current_hour < evening_hour or (current_hour == evening_hour and current_minute < evening_minute):
        time_diff = (evening_hour * 60 + evening_minute) - (current_hour * 60 + current_minute)
        hours = time_diff // 60
        minutes = time_diff % 60
        if hours > 0:
            summary.append(f"• Вечернее напоминание через: {hours} ч {minutes} мин (в {evening_time})")
        else:
            summary.append(f"• Вечернее напоминание через: {minutes} мин (в {evening_time})")
    else:
        summary.append(f"• Вечернее напоминание сегодня уже было в {evening_time}")

    return "\n".join(summary)

if __name__ == "__main__":
    print(check_all_reminders())
    print("\n" + "="*50 + "\n")
    print(get_reminder_summary())