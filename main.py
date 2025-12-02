import sched
import time
from openpyxl import Workbook
import pandas as pd
import argparse
import monitor
import plotting

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="System Resource Monitor")
    parser.add_argument("--duration", type=int)
    # parser.add_argument("--excel_location", type=str)
    parser.add_argument("--json_location", type=str)
    parser.add_argument("--database_location", type=str)
    args = parser.parse_args()

    # wb = Workbook()
    # sheet1 = wb.active
    # sheet1.title = "Sheet 1"

    # # header row
    # sheet1.cell(row=1, column=1, value="Time (sec)")
    # sheet1.cell(row=1, column=2, value="CPU Percentage")
    # sheet1.cell(row=1, column=3, value="Memory Percentage")
    # sheet1.cell(row=1, column=4, value="Disk Percentage")

    # excel_path = args.excel_location
    json_path = args.json_location
    db_path = args.database_location


    open(json_path, 'w').close()
    
    s = sched.scheduler(time.time, time.sleep)

    start_time = time.time()
    
    s.enter(
        0,
        1,
        monitor.sys_output,
        # (s, start_time, args.duration, wb, sheet1, excel_path)
        (s, start_time, args.duration, json_path)  
    )
    s.run()

    monitor.write_to_db(json_path, db_path)

    # wb.save(excel_path)

    # df = pd.read_excel(excel_path)

    # plotting.cpu_percent_graph(df)
    # plotting.memory_percent_graph(df)
    # plotting.disk_percent_graph(df)
