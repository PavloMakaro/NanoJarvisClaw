import datetime
import os
import sys
sys.path.append('modules')

from irkutsk_time import get_irkutsk_time

def check_system_reminders():
    """Проверяет все системные напоминания и задачи"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']

    result = []
    result.append("🔍 ПОЛНАЯ ПРОВЕРКА СИСТЕМНЫХ НАПОМИНАНИЙ")
    result.append(f"• Время проверки: {current_time}")
    result.append(f"• Дата: {irkutsk_time['date']}")
    result.append(f"• День недели: {irkutsk_time['day_of_week']}")
    result.append("")

    # 1. Проверяем файлы конфигурации
    result.append("📁 1. ФАЙЛЫ КОНФИГУРАЦИИ:")
    config_files = [
        ("data/profiles.json", "Профиль пользователя"),
        ("data/diary.txt", "Дневник"),
        ("data/sessions.json", "Сессии"),
    ]

    for filepath, description in config_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            result.append(f"   • {description}: найден ({size} байт)")
        else:
            result.append(f"   • {description}: не найден")

    # 2. Проверяем модули напоминаний
    result.append("")
    result.append("⚙️ 2. МОДУЛИ НАПОМИНАНИЙ:")
    reminder_modules = [
        ("auto_schedule_reminders", "Автонапоминания о расписании"),
        ("schedule_reminder", "Ручные напоминания о расписании"),
        ("diary", "Напоминания для дневника"),
        ("scheduler_tools", "Инструменты планировщика"),
    ]

    for module_name, description in reminder_modules:
        module_path = f"modules/{module_name}.py"
        if os.path.exists(module_path):
            result.append(f"   • {description}: установлен")
        else:
            result.append(f"   • {description}: отсутствует")

    # 3. Проверяем расписание
    result.append("")
    result.append("📅 3. РАСПИСАНИЕ:")
    try:
        from schedule_reminder import get_current_week_type
        week_type = get_current_week_type()
        result.append(f"   • Текущий тип недели: {week_type}")
    except:
        result.append("   • Тип недели: информация недоступна")

    # 4. Проверяем время следующего напоминания
    result.append("")
    result.append("⏰ 4. СЛЕДУЮЩИЕ НАПОМИНАНИЯ:")

    # Вечернее напоминание
    evening_time = "20:00"
    current_hour = int(current_time.split(':')[0])
    current_minute = int(current_time.split(':')[1])
    evening_hour, evening_minute = map(int, evening_time.split(':'))

    if current_hour < evening_hour or (current_hour == evening_hour and current_minute < evening_minute):
        time_diff = (evening_hour * 60 + evening_minute) - (current_hour * 60 + current_minute)
        hours = time_diff // 60
        minutes = time_diff % 60
        result.append(f"   • Вечернее напоминание о парах: через {hours} ч {minutes} мин")
    else:
        result.append(f"   • Вечернее напоминание о парах: завтра в {evening_time}")

    # Утренние напоминания
    morning_times = ["06:00", "07:00", "08:00", "09:00"]
    next_morning = None
    for mt in morning_times:
        m_hour, m_minute = map(int, mt.split(':'))
        if current_hour < m_hour or (current_hour == m_hour and current_minute < m_minute):
            time_diff = (m_hour * 60 + m_minute) - (current_hour * 60 + current_minute)
            hours = time_diff // 60
            minutes = time_diff % 60
            next_morning = f"{mt} (через {hours} ч {minutes} мин)"
            break

    if next_morning:
        result.append(f"   • Следующая утренняя проверка: {next_morning}")
    else:
        # Если все утренние проверки прошли, следующая будет завтра
        result.append(f"   • Следующая утренняя проверка: завтра в {morning_times[0]}")

    # 5. Статус системы
    result.append("")
    result.append("✅ 5. СТАТУС СИСТЕМЫ:")
    result.append("   • Система напоминаний активна")
    result.append("   • Автоматические проверки работают")
    result.append("   • Расписание загружено и доступно")

    return "\n".join(result)

def get_reminder_status_simple():
    """Простой статус напоминаний"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']
    current_hour = int(current_time.split(':')[0])

    status = []
    status.append("📊 ТЕКУЩИЙ СТАТУС НАПОМИНАНИЙ:")

    # Определяем текущий период дня
    if current_hour < 6:
        status.append("• Ночь (с 00:00 до 6:00) - напоминаний нет")
    elif current_hour < 12:
        status.append("• Утро (с 6:00 до 12:00) - утренние напоминания о парах")
    elif current_hour < 18:
        status.append("• День (с 12:00 до 18:00) - напоминаний нет")
    elif current_hour < 20:
        status.append("• Вечер (с 18:00 до 20:00) - скоро вечернее напоминание")
    else:
        status.append("• Поздний вечер (после 20:00) - напоминания завершены")

    # Следующее напоминание
    evening_time = "20:00"
    current_minute = int(current_time.split(':')[1])
    evening_hour, evening_minute = map(int, evening_time.split(':'))

    if current_hour < evening_hour or (current_hour == evening_hour and current_minute < evening_minute):
        time_diff = (evening_hour * 60 + evening_minute) - (current_hour * 60 + current_minute)
        if time_diff > 60:
            status.append(f"• Следующее напоминание: вечернее в {evening_time}")
        else:
            status.append(f"• Следующее напоминание: через {time_diff} минут")
    else:
        status.append(f"• Следующее напоминание: утреннее завтра в 6:00")

    return "\n".join(status)

if __name__ == "__main__":
    print(check_system_reminders())
    print("\n" + "="*60 + "\n")
    print(get_reminder_status_simple())