from datetime import datetime, timedelta

async def check_time_and_get_date():
    """
    Проверяет, больше ли текущее время 1:59 сегодня или меньше 1:59 завтра.
    Если условие выполняется, возвращает текущую дату (день, месяц, год).
    """
    now = datetime.now()
    target_time_today = now.replace(hour=1, minute=59, second=0, microsecond=0)
    target_time_tomorrow = target_time_today + timedelta(days=1)

    if now > target_time_today or now < target_time_tomorrow:
        return now.strftime("%d-%m-%Y")  # Форматируем дату как ДД-ММ-ГГГГ
    else:
        return None