import csv
from datetime import datetime, timedelta, date
import json
from collections import defaultdict

CSV_FILE = "/home/dmytro/fireOverlay/timeRecords.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Load all sessions from CSV ---
sessions = []
with open(CSV_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = datetime.strptime(row["timestamp"], DATE_FORMAT)
        sessions.append((ts, row["startOrFinish"]))

sessions.sort(key=lambda x: x[0])

# --- Calculate work durations per day ---
work_time_by_day = defaultdict(timedelta)
i = 0
while i < len(sessions) - 1:
    if sessions[i][1] == "start" and sessions[i+1][1] == "finish":
        start, end = sessions[i][0], sessions[i+1][0]
        if end > start:
            work_time_by_day[start.date()] += end - start
        i += 2
    else:
        i += 1

work_time_by_day_hours = defaultdict(float)
# Convert to hours for per-day records
for d, td in work_time_by_day.items():
    work_time_by_day_hours[d.isoformat()] = round(td.total_seconds()/3600, 2)
                          

# --- Save last 7-day summary as before ---
today = date.today()
seven_days_ago = today - timedelta(days=6)
last_7_days = {
    (today - timedelta(days=i)).isoformat(): 0.0
    for i in range(6, -1, -1)
}


for d_str in last_7_days.keys():
    last_7_days[d_str] = work_time_by_day_hours[d_str]


with open('work_summary.json', 'w') as f:
    json.dump(last_7_days, f, indent=2)

# --- Compute full week (Mon–Sun) averages for the entire dataset ---
weekly_hours = defaultdict(float)
for day_str, hours in work_time_by_day_hours.items():
    # Convert back to date object
    day = datetime.strptime(day_str, "%Y-%m-%d").date()
    # Determine Monday of the week this day belongs to
    monday = day - timedelta(days=day.weekday())  # Monday=0
    week_label = f"{monday.isoformat()}_to_{(monday + timedelta(days=6)).isoformat()}"
    weekly_hours[week_label] += hours

# Compute average hours per day per week (over 7 days always)
weekly_stats = {}
for week, total in sorted(weekly_hours.items()):
    weekly_stats[week] = {
        "total_hours": round(total, 2),
        "average_hours_per_day": round(total / 7, 2)
    }

# Save full-week stats
with open('weekly_summary.json', 'w') as f:
    json.dump(weekly_stats, f, indent=2)
