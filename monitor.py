import psutil as util
import time
import json
import sqlite3

class SystemMonitor:
    def __init__(self):
        self.row = 2

    def increment(self):
        self.row += 1

rowNumber = SystemMonitor()

def sys_output(scheduler, start_time, duration, json_path):

    current_time = time.time()
    elapsed = current_time - start_time
    log = {}

    if elapsed >= duration:
        return
    
    # capture metrics
    # cpu_percent = util.cpu_percent(interval=1)
    # memory_percent = util.virtual_memory().percent
    # disk_percent = util.disk_usage('C:\\').percent

    log["time"] = round(current_time - start_time, 2)
    log["CPU Percent"] = util.cpu_percent(interval=1)
    log["Memory Percent"] = util.virtual_memory().percent
    log["Disk Percent"] = util.disk_usage('C:\\').percent

    with open(json_path, 'a') as f:
        f.write(json.dumps(log) + '\n')
        
    # write one sample per row
    # sheet.cell(row=rowNumber.row, column=1, value=round(current_time - start_time))
    # sheet.cell(row=rowNumber.row, column=2, value=cpu_percent)
    # sheet.cell(row=rowNumber.row, column=3, value=memory_percent)
    # sheet.cell(row=rowNumber.row, column=4, value=disk_percent)

    # rowNumber.increment()

    # wb.save(excel_path)

    scheduler.enter(
        5, 
        1, 
        sys_output,
        (scheduler, start_time, duration, json_path)
    )

def write_to_db(json_path, db_path):

    data_list = []

    with open(json_path, 'r') as f:
        for line in f:
            dic = json.loads(line)
            data_list.append(list(dic.values()))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            time REAL,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )
    """)

    cursor.executemany("INSERT INTO data VALUES (?,?,?,?)", data_list)
    
    conn.close()