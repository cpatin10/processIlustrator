import datetime

#this method printes the infortation of the processes int ahuman undestandable way
#it takes the dictionary of the processes and print them to standard output
def cutePrint(info,keys):
    print "actual time:",datetime.datetime.time(datetime.datetime.now())
    keysFormated = []
    for key in xrange(len(keys)):
        keysFormated.append('{0: <20}'.format(keys[key]))
    print ''.join(map(str, keysFormated))
    print ''
    
    for process in info:
        res = []
        for key in keys:
            res.append('{0: <20}'.format(info[process][key] if (key in info[process]) else '~~~~~~~~~~~~'))
        print ''.join(map(str, res))

    print ""

#this method prints the information of the processes in a csv
#it takes the dictionary of the processes and print them to standard output
def csvPrint(info,keys):
    print "actual time:",datetime.datetime.time(datetime.datetime.now())
    keysFormated = []
    for key in xrange(len(keys)):
        keysFormated.append(keys[key])
    print ', '.join(map(str, keysFormated))
    
    for process in info:
        res = []
        for key in keys:
            res.append(info[process][key] if (key in info[process]) else '~~~~~~~~~~~~')
        print ', '.join(map(str,res))
