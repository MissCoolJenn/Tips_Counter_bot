from datetime import datetime, timedelta
import sqlite3

def Connect():
    conn = sqlite3.connect('fuck_glovo.db')
    cursor = conn.cursor()
    return conn, cursor

def Disconnect(conn, cursor):
    cursor.close()
    conn.close()

async def Save_info(user_name, date, tips):
    conn, cursor = Connect()

    try:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS main (
                       id INTEGER PRIMARY KEY,
                       user_name TEXT NOT NULL,
                       date TEXT NOT NULL,
                       tips INTEGER NOT NULL
                       )""")
        cursor.execute("INSERT INTO main (user_name, date, tips) VALUES (?, ?, ?)", (user_name, date, tips))
        conn.commit()
    except:
        Disconnect(cursor)
        return ("DB Error")
    
    Disconnect(conn, cursor)
    
async def Get_info(user_name, date):
    conn, cursor = Connect()

    #cursor.execute("""
    #               SELECT * FROM main
    #               """)
    #user_name = str(user_name)

    #print(f'*******\n{type(user_name)}')
    cursor.execute("SELECT * FROM main WHERE user_name = ?", (user_name,))
    
    rows = cursor.fetchall()
    print('... ... ...')
    for row in rows:
        print(row)

    Disconnect(conn, cursor)

    day_tips = await get_day_tips(date, rows)
    week_tips = await get_week_tips(date, rows)
    return (day_tips, week_tips)

async def get_day_tips(date, rows):
    all_day = 0
    for row in rows:
        if row[2] == date:
            all_day += row[3]
    return str(all_day)

async def get_week_tips(date_str, rows):
    try:
        date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return 0  # Возвращаем 0, если формат даты некорректен

    # Получаем дату понедельника текущей недели
    monday = date - timedelta(days=date.weekday())

    # Получаем дату воскресенья текущей недели
    sunday = monday + timedelta(days=6)

    total_week_value = 0
    for row in rows:
        try:
            row_date = datetime.strptime(row[2], "%d-%m-%Y").date()
        except ValueError:
            continue  # Пропускаем строку, если формат даты некорректен

        if monday <= row_date <= sunday:
            total_week_value += row[3]

    return str(total_week_value)