import os

#Method for getting the % Of CPU used last second, it recieves the actial info of the processes (total time worked), the info of the last second, and the work percentage of the cpu over the last second
def getCPULastSecond(info,actualInfo,lastInfo,workPercentage):
    totalTime = 0.1
    for key in info:
        time =  (float(lastInfo[key]['total_time']) if (key in lastInfo) else 0)
        myTimeLastSecond = float(actualInfo[key]['total_time']) - time
        totalTime += myTimeLastSecond
    for key in info:
        myTimeLastSecond = float(actualInfo[key]['total_time']) - ( float(lastInfo[key]['total_time']) if (key in lastInfo) else 0)
        info[key]['time last second ms'] = myTimeLastSecond 
        info[key]['%CPU last second %'] = str(100*workPercentage*(myTimeLastSecond/totalTime))
        info[key]['%CPU not idle %'] = str(100*(myTimeLastSecond/totalTime))

#MEthod that does return a dictionary with different PIDs pointing to how many semaphores they have
def getSemaphoresPOXIS():
    dicSems = {}
    shm = os.listdir("/dev/shm")
    shm = [sems for sems in shm if len(sems) > 3 and sems[0:4] == "sem."]
    for sem in shm:
        lsofsem = os.popen("lsof /dev/shm/"+sem).read().split("\n")
        for ls in lsofsem[1:-1]:
            splitls = ls.split()
            pidSem = splitls[1] if splitls[1].isdigit() else -1
            if pidSem in dicSems:
                dicSems[pidSem] +=1
            else:
                dicSems[pidSem] = 1
    return dicSems

#Method that get some general information of a process, it takes the process to search as a string, the info of the information of the actual second, which it will actualize,
#the amount of ticks per second of the actual computer to convert the ticks to second, and the pageSize of the actual computer
# it returns its process ID, the process Name, the percentage of usage since the beginning, the Virtual memorry size, the real memory size, the Shared memory size, and finally the input and oput operations
#the information is returned as a dictionary in which the each type is pointing to its asociated value
def retrieveInfo(process,actualSecond, clockTicksEQ,pageSize):
    meRightNow = {}
    path = '/proc/'+ str(process)
    command = ''.join([path, '/stat'])
    f = open(command,'r') #opens file with name of "test.txt"
    myList = []
    stat = f.readline().split()
    f.close()    
    info = {}
    info['Process ID'] = process
    info['Process Name'] = stat[1][1:-1] if len(stat)>1 else '-'
    uptime = actualSecond['uptime working'] + actualSecond['uptime idle']
    utime = int(stat[13])
    stime = int(stat[14])
    startTime = int(stat[21])
    meRightNow['total_time'] = total_time_alone = utime + stime
    seconds = uptime - (startTime/clockTicksEQ)
    actualSecond[str(process)] = meRightNow
    cpu_usage = 100 * ((float(total_time_alone)/float(clockTicksEQ))/float(seconds))
    info['%CPU start %'] = str(cpu_usage)    
    statmPath = ''.join([path, "/statm"])    
    f = open(statmPath, 'r')
    statm = f.read().split()
    f.close()    
    info['Virt Mem Size B'] = str(int(statm[0])*pageSize)
    info['Real Mem Used B'] = str(int(statm[1])*pageSize)
    info['Shared Mem Size B'] = str(int(statm[2])*pageSize)
    iopath = ''.join([path + "/io"])
    if os.access(iopath, os.R_OK):
        command =''.join([iopath]) 
        f = open(iopath,"r") #opens file with name of "test.txt"
        myList = []
        for line in f:
            myList.append(line)
        statio = myList
        statio = [vals.split()[1] for vals in statio if len(vals.split()) == 2]
        info['Input oper'] = statio[2]
        info['Output oper'] = statio[3]
        f.close()
    else:
        info['Input oper'] = 'Perms Denied'
        info['Output oper'] = 'Perms Denied'
    return info


#its the method to return the information of all the values it receives a dictinary pointing to the information of the last second
#and the keys to each value
#it returns the information of all the processes as a dictionary and the information of the actual second
def retrieveAllProcesses(lastSecondInfo,keys):
    clockTicksEQ = int(os.sysconf(os.sysconf_names['SC_CLK_TCK']))
    pageSize = int(os.popen("getconf PAGESIZE").read())    
    f = open("/proc/uptime","r")
    uptimeInfo = f.readline().split()
    f.close()    
    uptimeWork = float(uptimeInfo[0])
    uptimeIdle = float(uptimeInfo[1])
    actualSecondInfo = {'uptime working':uptimeWork,'uptime idle':uptimeIdle}
    #Detecting process in /proc
    processesInfo = {}
    procDir = os.listdir("/proc")
    procDir = [processId for processId in procDir if processId.isdigit()]
    #Retrieving info of each process
    for process in procDir:
        info = retrieveInfo(process,actualSecondInfo,clockTicksEQ,pageSize)
        processesInfo[process] = info
    #Detecting number of semaphores per process
    dicSems = getSemaphoresPOXIS()
    for process in procDir:
        processesInfo[process]['Semaphores'] = (dicSems[process] if process in dicSems else 0)
    #Calculating CPU usage for the last second (this cannot be calculated in first medition)
    if (lastSecondInfo['uptime working']!= -1):
        getCPULastSecond(processesInfo,actualSecondInfo,lastSecondInfo,(uptimeWork)/(uptimeWork+uptimeIdle))
    return processesInfo, actualSecondInfo
