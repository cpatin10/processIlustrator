def cutePrint(info,keys):
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

def csvPrint(info,keys):
    
    for process in info:
        res = []
        for key in keys:
            res.append(info[process][key] if (key in info[process]) else '~~~~~~~~~~~~')
        print ''.join(mat(str,res))
