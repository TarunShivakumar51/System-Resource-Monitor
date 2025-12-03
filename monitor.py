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

def monitor_loop(shared_dic):
    while True:
        shared_dic["time"] = time.time()
        shared_dic["CPU Percent"] = util.cpu_percent(interval=1)
        shared_dic["Memory Percent"] = util.virtual_memory().percent
        shared_dic["Disk Percent"] = util.disk_usage('C:\\').percent
        time.sleep(5)

def sys_output(scheduler, start_time, duration, json_path, wb, sheet, excel_path):

    current_time = time.time()
    elapsed = current_time - start_time
    log = {}

    if elapsed >= duration:
        return
    
    log["time"] = round(elapsed, 2)
    cpu = util.cpu_percent(interval=1)
    mem = util.virtual_memory().percent
    disk = util.disk_usage('C:\\').percent

    log["CPU Percent"] = cpu
    log["Memory Percent"] = mem
    log["Disk Percent"] = disk

    # JSON LOG
    with open(json_path, 'a') as f:
        f.write(json.dumps(log) + '\n')

    # EXCEL LOG
    sheet.cell(row=rowNumber.row, column=1, value=log["time"])
    sheet.cell(row=rowNumber.row, column=2, value=cpu)
    sheet.cell(row=rowNumber.row, column=3, value=mem)
    sheet.cell(row=rowNumber.row, column=4, value=disk)
    rowNumber.increment()

    wb.save(excel_path)

    scheduler.enter(
        5, 
        1, 
        sys_output,
        (scheduler, start_time, duration, json_path, wb, sheet, excel_path)
    )

def write_to_db(json_path, db_path):
    data_list = []

    with open(json_path, 'r') as f:
        for line in f:
            dic = json.loads(line)
            data_list.append([
                dic["time"],
                dic["CPU Percent"],
                dic["Memory Percent"],
                dic["Disk Percent"]
            ])

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
