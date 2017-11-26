import os

def getCPULastSecond(info,actualInfo,lastInfo,workPercentage):
    totalTime = 0.1
    for key in info:
        time =  (float(lastInfo[key]['total_time']) if (key in lastInfo) else 0)
        myTimeLastSecond = 1.0*float(actualInfo[key]['total_time']) - time
        totalTime += myTimeLastSecond
    for key in info:
        myTimeLastSecond = 1.0*float(actualInfo[key]['total_time']) - ( float(lastInfo[key]['total_time']) if (key in lastInfo) else 0)
        info[key]['time last second'] = myTimeLastSecond 
        info[key]['%CPU last second'] = str(100*workPercentage*(myTimeLastSecond/totalTime)) + (' %')
        info[key]['%CPU not idle'] = str(100*(myTimeLastSecond/totalTime)) + (' %')

def getSemaphoresPOXIS():
    dicSems = {}
    shm = os.popen("ls /dev/shm/").read().split("\n")
    shm = [sems for sems in shm if len(sems) > 3 and sems[0:4] == "sem."]
    for sem in shm:
        lsofsem = os.popen("lsof /dev/shm/"+sem).read().split("\n")
        for ls in lsofsem[1:]:
            splitls = ls.split()
            pidSem = splitls[1] if len(splitls)>2 and splitls[1].isdigit() else -1
            if pidSem != -1:
                if pidSem in dicSems:
                    dicSems[pidSem] +=1
                else:
                    dicSems[pidSem] = 1
    return dicSems

    



def retrieveInfo(process,actualSecond, lastSecond, clockTicksEQ,pageSize):
    meRightNow = {}
    path = '/proc/'+str(process)
    stat = os.popen("cd " + path + "; cat stat").read().split(" ")
    info = {}
    info['Process ID'] = process
    info['Process Name'] = stat[1][1:-1]
    uptime = actualSecond['uptime working'] + actualSecond['uptime idle']
    utime = int(stat[13])
    stime = int(stat[14])
    startTime = int(stat[21])
    meRightNow['total_time'] = total_time_alone = utime + stime
    seconds = uptime - (startTime/clockTicksEQ)
    actualSecond[str(process)] = meRightNow
    cpu_usage = 100 * (((total_time_alone*1.0)/(clockTicksEQ*1.0))/(seconds*1.0))
    info['%CPU start'] = str(cpu_usage) + ' %'
    statm = os.popen("cd " + path + "; cat statm").read().split(" ")
    info['Virt Mem Size'] = str(int(statm[0])*pageSize) + (' B')
    info['Real Mem Used'] = str(int(statm[1])*pageSize) + (' B')
    info['Shared Mem Size'] = str(int(statm[2])*pageSize) + (' B')
    if os.access(path + "/io", os.R_OK):
        statio = os.popen("cd " + path + "; cat io").read().split("\n")
        statio = [vals.split()[1] for vals in statio if len(vals.split()) == 2]
        info['Input oper'] = statio[2]
        info['Output oper'] = statio[3]
    else:
        info['Input operations'] = 'Perms Denied'
        info['Output operations'] = 'Perms Denied'
    return info


def retrieveAllProcesses(lastSecondInfo,keys,boolSem):
    clockTicksEQ = int(os.sysconf(os.sysconf_names['SC_CLK_TCK']))
    pageSize = int(os.popen("getconf PAGESIZE").read())
    
    uptimeInfo = os.popen("cd /proc; cat uptime").read().split()
    uptimeWork = float(uptimeInfo[0])
    uptimeIdle = float(uptimeInfo[1])
    actualSecondInfo = {'uptime working':uptimeWork,'uptime idle':uptimeIdle}

    processesInfo = {}
    procDir = os.listdir("/proc")
    procDir = [processId for processId in procDir if processId.isdigit()]

    
    for process in procDir:
        info = retrieveInfo(process,actualSecondInfo,lastSecondInfo,clockTicksEQ,pageSize)
        processesInfo[process] = info
    if boolSem:
        dicSems = getSemaphoresPOXIS()
        for process in procDir:
            processesInfo[process]['Semaphores'] = (dicSems[process] if process in dicSems else 0)

    if (lastSecondInfo['uptime working']!= -1):
        getCPULastSecond(processesInfo,actualSecondInfo,lastSecondInfo,(uptimeWork)/(uptimeWork+uptimeIdle))
    return processesInfo, actualSecondInfo
