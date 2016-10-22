while True:
    print 'a'
    break
mssg = 'Visittor'
print len(mssg)
d = ''
i = 0
while len(d)<8:
    d +=  mssg[i]
    i+=1

print d[:8],'     ',d[8:]