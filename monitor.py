import psutil as util
import time

class SystemMonitor:
    def __init__(self):
        self.row = 2

    def increment(self):
        self.row += 1

rowNumber = SystemMonitor()

def sys_output(scheduler, start_time, duration, wb, sheet, excel_path):

    current_time = time.time()

    if current_time - start_time >= duration:
        wb.save(excel_path)
        return

    # capture metrics
    cpu_percent = util.cpu_percent(interval=1)
    memory_percent = util.virtual_memory().percent
    disk_percent = util.disk_usage('C:\\').percent

    # write one sample per row
    sheet.cell(row=rowNumber.row, column=1, value=round(current_time - start_time))
    sheet.cell(row=rowNumber.row, column=2, value=cpu_percent)
    sheet.cell(row=rowNumber.row, column=3, value=memory_percent)
    sheet.cell(row=rowNumber.row, column=4, value=disk_percent)

    rowNumber.increment()

    wb.save(excel_path)

    scheduler.enter(
        5, 
        1, 
        sys_output,
        (scheduler, start_time, duration, wb, sheet, excel_path)
    )