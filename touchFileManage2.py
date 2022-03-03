from time import strftime

def storeEvent(data): #receive padNum in string format
    #padNum = "Pad1"
    
    timestr = strftime("%Y%m%d_%H:%M:%S")
    #timestr = 'Now'

    #data = [time,',', event, ',', eventDetails, '\n']

    file1 = open(r"/home/pi/Documents/Data/" + timestr + ".txt","a")
    file1.writelines(data)
    file1.close()

    #file1 = open(r"/home/pi/Documents/Data/"+ timestr +".txt","r") 
    #print(file1.read())
    #file1.close()

#storeEvent(100, "Pad1", 1)