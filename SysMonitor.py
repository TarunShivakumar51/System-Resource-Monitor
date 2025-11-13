import psutil as util
import sched
import time
import os

def sys_output(scheduler, f, start_time):

    current_time = time.time()

    # stop after 60 seconds
    if current_time - start_time >= 60:
        return

    # do your system logging
    cpu_percent = str(util.cpu_percent(1))
    memory_percent = str(util.virtual_memory()[2])
    disk_percent = str(util.disk_usage('/')[3])
    f.write(cpu_percent + ", " + memory_percent + ", " + disk_percent + "\n")

    f.flush()
    os.fsync(f.fileno())

    # schedule next run in 5 seconds
    scheduler.enter(5, 1, sys_output, (scheduler, f, start_time))

if __name__ == '__main__':
    path = 'C:/Users/tarun/OneDrive/Desktop/Projects/System Resource Monitor/Output Data.txt'

    f = open(path, 'w')

    f.write('CPU Percentage, Memory Percentage, Disk Percentage\n')


    s = sched.scheduler(time.time, time.sleep)

    start_time = time.time()   # when the logging began
    # first run happens immediately
    s.enter(0, 1, sys_output, (s, f, start_time))
    s.run()

    f.close()
