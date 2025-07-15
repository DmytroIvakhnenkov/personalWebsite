import csv
from datetime import datetime, timedelta, date

# get last info for last 7 days, if less days then get that much


CSV_FILE = "/home/dmytro/fireOverlay/timeRecords.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
today = datetime.now().date()
sevenDaysAgo = today - timedelta(days=6)
sessionsForSevenDays = []

# read the data for the last 7 days
with open(CSV_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ts = datetime.strptime(row["timestamp"], DATE_FORMAT)
        if sevenDaysAgo <= ts.date():
            sessionsForSevenDays.append((ts, row["startOrFinish"]))

workTimeByDays = {(date.today() - (timedelta(days = i))).isoformat():timedelta()
                  for i in range(6, -1, -1)}

sessionsForSevenDays.sort()
work_time = timedelta()
i = 0
while i < len(sessionsForSevenDays) - 1:
    if sessionsForSevenDays[i][1] == "start" and sessionsForSevenDays[i + 1][1] == "finish":
        start, end = sessionsForSevenDays[i][0], sessionsForSevenDays[i + 1][0]
        if end > start:
            workTimeByDays[sessionsForSevenDays[i][0].date().isoformat()] += end - start
        i += 2
    else:
        i += 1

for key in workTimeByDays.keys():
    workTimeByDays[key] = round(workTimeByDays[key].total_seconds() / 3600, 2)

with open('work_summary.json', 'w') as f:
    import json
    json.dump(workTimeByDays, f)
