
from retriever import *
from printer import *
from time import sleep
from threading import Timer
import argparse
import signal
import sys

def handler(signum, frame):
    sys.exit(0)

def processIlustrator(keys, lastSecondInfo):
    processInfo, lastSecondInfo = retrieveAllProcesses(lastSecondInfo, keys)
    cutePrint(processInfo, keys)
    Timer(1.0, processIlustrator, (keys, lastSecondInfo)).start()


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--semaphores',
                        action='store_true',
                        help='If given the program will show the semaphores of each process.')
    arguments = parser.parse_args()
    return arguments


def main():
    arguments = parseArgs()
    keys = ['Process ID','Process Name','%CPU start','%CPU last second','%CPU not idle','Virt Mem Size','Real Mem Used','Shared Mem Size','Input oper','Output oper','time last second']
    lastSecondInfo = {'uptime working':-1,'uptime idle': -1}
    signal.signal(signal.SIGINT, handler)

    boolSem = arguments.semaphores
    if boolSem:
        keys.append('Semaphores')
    while True:
        processInfo, lastSecondInfo = retrieveAllProcesses(lastSecondInfo, keys,boolSem)
        cutePrint(processInfo, keys)
        sleep(1)

main()
