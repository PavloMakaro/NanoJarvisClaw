import datetime
import os
import sys
sys.path.append('modules')

from irkutsk_time import get_irkutsk_time
from auto_diary_reminder_fixed import setup_diary_reminder, check_diary_reminder_status, get_diary_stats
from check_reminders import check_all_reminders

def initialize_diary():
    """Инициализирует файл дневника, если он не существует"""
    diary_file = "data/diary.txt"

    # Создаем папку data, если её нет
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(diary_file):
        # Создаем шаблон дневника
        template = """# 📓 МОЙ ДНЕВНИК

## Как пользоваться:
1. Каждый день добавляйте новую запись с датой: ## ГГГГ-ММ-ДД
2. Пишите о событиях дня, мыслях, планах
3. Используйте маркеры для структуры

## Пример записи:
## 2026-02-16
• Утром была пара по МДК ТОРА
• Днем работал над проектом
• Вечером занимался спортом
• Завтра нужно подготовиться к экзамену

---

"""

        with open(diary_file, 'w', encoding='utf-8') as f:
            f.write(template)

        return {
            "status": "created",
            "message": "Файл дневника создан с шаблоном",
            "filepath": diary_file
        }
    else:
        return {
            "status": "exists",
            "message": "Файл дневника уже существует",
            "filepath": diary_file
        }

def add_diary_entry_manual(text):
    """Добавляет запись в дневник вручную"""
    diary_file = "data/diary.txt"

    # Создаем папку и файл, если не существует
    initialize_diary()

    # Получаем текущую дату
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Форматируем запись
    entry = f"\n## {current_date}\n{text}\n"

    # Добавляем запись в файл
    with open(diary_file, 'a', encoding='utf-8') as f:
        f.write(entry)

    return {
        "status": "success",
        "message": f"Запись добавлена за {current_date}",
        "date": current_date
    }

def get_reminder_schedule():
    """Получает полное расписание всех напоминаний"""
    irkutsk_time = get_irkutsk_time()
    current_time = irkutsk_time['time']

    schedule = []
    schedule.append("📅 ПОЛНОЕ РАСПИСАНИЕ НАПОМИНАНИЙ")
    schedule.append(f"• Текущее время: {current_time}")
    schedule.append(f"• Дата: {irkutsk_time['date']}")
    schedule.append(f"• День недели: {irkutsk_time['day_of_week']}")
    schedule.append("")

    # Утренние напоминания
    schedule.append("🌅 УТРЕННИЕ НАПОМИНАНИЯ (06:00-09:00):")
    schedule.append("   06:00 - Первая проверка расписания")
    schedule.append("   07:00 - Вторая проверка расписания")
    schedule.append("   08:00 - Третья проверка расписания")
    schedule.append("   09:00 - Последняя проверка расписания")
    schedule.append("   → О парах на сегодня")

    # Дневные напоминания
    schedule.append("")
    schedule.append("☀️  ДНЕВНЫЕ НАПОМИНАНИЯ (12:00-18:00):")
    schedule.append("   • Нет автоматических напоминаний")
    schedule.append("   • Можно установить одноразовые")

    # Вечерние напоминания
    schedule.append("")
    schedule.append("🌙 ВЕЧЕРНИЕ НАПОМИНАНИЯ (20:00):")
    schedule.append("   20:00 - Напоминание о дневнике")
    schedule.append("   20:00 - Напоминание о расписании на завтра")
    schedule.append("   → Два напоминания одновременно")

    # Время до следующего напоминания
    schedule.append("")
    schedule.append("⏰ СЛЕДУЮЩИЕ НАПОМИНАНИЯ:")

    current_hour = int(current_time.split(':')[0])
    current_minute = int(current_time.split(':')[1])

    if current_hour < 20:
        time_to_evening = (20 * 60) - (current_hour * 60 + current_minute)
        hours = time_to_evening // 60
        minutes = time_to_evening % 60
        schedule.append(f"   • Вечерние: через {hours} ч {minutes} мин (в 20:00)")
    else:
        schedule.append("   • Вечерние: завтра в 20:00")

    if current_hour < 6:
        time_to_morning = (6 * 60) - (current_hour * 60 + current_minute)
        hours = time_to_morning // 60
        minutes = time_to_morning % 60
        schedule.append(f"   • Утренние: через {hours} ч {minutes} мин (в 06:00)")
    elif current_hour < 9:
        # Находим следующее утреннее напоминание
        morning_times = [6, 7, 8, 9]
        next_morning = None
        for mt in morning_times:
            if current_hour < mt or (current_hour == mt and current_minute < 0):
                time_diff = (mt * 60) - (current_hour * 60 + current_minute)
                hours = time_diff // 60
                minutes = time_diff % 60
                schedule.append(f"   • Следующее утреннее: через {hours} ч {minutes} мин (в {mt:02d}:00)")
                break
    else:
        schedule.append("   • Утренние: завтра в 06:00")

    return "\n".join(schedule)

def setup_all_reminders():
    """Настраивает все напоминания"""
    results = []

    # 1. Инициализируем дневник
    diary_init = initialize_diary()
    results.append(f"📓 Дневник: {diary_init['message']}")

    # 2. Настраиваем напоминание для дневника
    diary_reminder = setup_diary_reminder()
    results.append(f"🔔 Напоминание для дневника: {diary_reminder['message']}")

    # 3. Проверяем статус
    diary_status = check_diary_reminder_status()
    results.append(f"⏰ Следующее напоминание: {diary_status['next_reminder_in']}")

    return "\n".join(results)

if __name__ == "__main__":
    print("🔄 НАСТРОЙКА ВСЕХ НАПОМИНАНИЙ\n")
    print(setup_all_reminders())
    print("\n" + "="*60 + "\n")
    print(get_reminder_schedule())