import pandas as pd


PAIR_TIMES = {
    1: "08:00 - 09:30",
    2: "09:40 - 11:10",
    3: "11:20 - 12:50",
    4: "13:15 - 14:45",
    5: "15:00 - 16:30",
    6: "16:40 - 18:10",
    7: "18:20 - 19:50",
    8: "19:55 - 21:25"
}


def load_schedule(file_path):
    df = pd.read_excel(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

def get_groups(df):
    return sorted(df['группа'].unique())

def get_days(df):
    # берем уникальные значения, убираем пустые и приводим к строкам
    days = [str(d) for d in df['день'].dropna().unique()]
    # сортируем в нормальном порядке недели
    week_order = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    # оставляем только дни, которые есть в данных
    return [d for d in week_order if d in days]


def get_schedule(df, group, day):
    subset = df[(df['группа'] == group) & (df['день'].str.lower() == day.lower())]

    if subset.empty:
        return f"Нет пар в день: {day}"

    schedule_text = f"📅 Расписание для {group} — {day}:\n\n"
    for pair_number in sorted(subset['пара'].dropna().unique(), key=int):
        pair_rows = subset[subset['пара'] == pair_number]
        time = PAIR_TIMES.get(int(pair_number), "—")  # добавляем время пары
        for _, row in pair_rows.iterrows():
            subgrp = f"[{row['подгруппа']}]" if str(row['подгруппа']) != "-" else ""
            subject = row['предмет'] if str(row['предмет']) != "-" else "—"
            auditorium = row['аудитория'] if str(row['аудитория']) != "-" else "—"
            teacher = row['преподаватель'] if str(row['преподаватель']) != "-" else "—"
            schedule_text += f"Пара {pair_number} {subgrp} {subject}\n"
            schedule_text += f"Время: {time}\n"
            schedule_text += f"Аудитория: {auditorium}\n"
            schedule_text += f"Преподаватель: {teacher}\n\n"
    return schedule_text.strip()

