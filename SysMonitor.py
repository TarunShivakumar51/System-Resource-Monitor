import psutil as util
import sched
import time
import os
import xlwt
from xlwt import Workbook

row = 1  # next Excel row to write

def sys_output(scheduler, start_time):
    global row, sheet1, wb, excel_path

    current_time = time.time()

    # stop after 60 seconds
    if current_time - start_time >= 60:
        wb.save(excel_path)
        return

    # capture metrics
    cpu_percent = util.cpu_percent(interval=1)
    memory_percent = util.virtual_memory().percent
    disk_percent = util.disk_usage('C:\\').percent

    # write one sample per row: (CPU, Memory, Disk)
    sheet1.write(row, 0, cpu_percent)
    sheet1.write(row, 1, memory_percent)
    sheet1.write(row, 2, disk_percent)

    row += 1

    # save workbook so data is visible while running
    wb.save(excel_path)

    # schedule next run in 5 seconds
    scheduler.enter(5, 1, sys_output, (scheduler, start_time))


if __name__ == '__main__':

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    # header row
    sheet1.write(0, 0, 'CPU Percentage')
    sheet1.write(0, 1, 'Memory Percentage')
    sheet1.write(0, 2, 'Disk Percentage')

    excel_path = 'C:/Users/tarun/OneDrive/Desktop/Projects/System Resource Monitor/system_output.xls'

    s = sched.scheduler(time.time, time.sleep)

    start_time = time.time()   # when the logging began
    # first run happens immediately
    s.enter(0, 1, sys_output, (s, start_time))
    s.run()

    wb.save(excel_path)