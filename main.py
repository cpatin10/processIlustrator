from retriever import *
from printer import *
from time import sleep
from threading import Timer
import signal
import sys

#Handler to finish execution when Ctrl-c is detected
def handler(signum, frame):
    sys.exit(0)

#Program for showing every second the status information (PID, Name, %CPU used, Virtual, physical and shared memory size, numbero of I/O operations and semaphores of each process running at the moment.
def main():
    keys = ['Process ID','Process Name','%CPU start %','%CPU last second %','%CPU not idle %','Virt Mem Size B','Real Mem Used B','Shared Mem Size B','Input oper','Output oper','time last second ms', 'Semaphores']
    lastSecondInfo = {'uptime working':-1,'uptime idle': -1}
    signal.signal(signal.SIGINT, handler)
    while True:
        processInfo, lastSecondInfo = retrieveAllProcesses(lastSecondInfo, keys)
        csvPrint(processInfo, keys)
        print 
        sleep(1)
main()
