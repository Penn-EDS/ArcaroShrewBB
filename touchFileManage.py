import time

def storeTouch(padNum): #receive padNum in string format
    #padNum = "Pad1"
    
    now = time.time()
    mlsec = repr(now).split('.')[1][:3]
    timestr = time.strftime("%Y%m%d_%H:%M:%S:{}".format(mlsec), time.localtime(now))
    timestrprt = time.strftime("%Y-%m-%dT%H:%M:%S:{}".format(mlsec))

    dt = [timestrprt,',',padNum]

    #print(os.getcwd())

    file1 = open(r"/home/pi/Documents/Data/" + timestr + ".txt","a")
    file1.writelines([timestrprt,',',padNum])
    file1.close()

    file1 = open(r"/home/pi/Documents/Data/"+ timestr +".txt","r") 
    print(file1.read())
    file1.close()