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
    parser.add_argument("--location", type=str)
    args = parser.parse_args()

    wb = Workbook()
    sheet1 = wb.active
    sheet1.title = "Sheet 1"

    # header row
    sheet1.cell(row=1, column=1, value="Time (sec)")
    sheet1.cell(row=1, column=2, value="CPU Percentage")
    sheet1.cell(row=1, column=3, value="Memory Percentage")
    sheet1.cell(row=1, column=4, value="Disk Percentage")

    excel_path = args.location

    s = sched.scheduler(time.time, time.sleep)

    start_time = time.time()
    
    s.enter(
        0,
        1,
        monitor.sys_output,
        (s, start_time, args.duration, wb, sheet1, excel_path) 
    )
    s.run()

    wb.save(excel_path)

    df = pd.read_excel(excel_path)

    plotting.cpu_percent_graph(df)
    plotting.memory_percent_graph(df)
    plotting.disk_percent_graph(df)
