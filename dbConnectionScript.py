#import RPi.GPIO as GPIO

import pymssql as db
import datetime as time

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#GPIO.setup(21, GPIO.OUT)
#GPIO.output(21, GPIO.LOW)

dbContext = db.connect(host='192.168.0.19:1433\SQLSERVER', user='sa', password='ulamek12', database='WebAppDb')
cursor = dbContext.cursor()

class Controller:
    def __init__(self, Id, Name, Type):
        self.Id = Id
        self.Name = Name
        self.Type = Type
    def __repr__(self):
        return "\n Controller - Id: %s, Name: %s, Type: %s" % (self.Id, self.Name, self.Type)

def AddControllerToDataBase(Controller):
    startTime = time.datetime.now()
        
    query = "INSERT INTO dbo.Controllers (ControllerName, ControllerType) VALUES (%s, %s)"
    
    cursor.execute(query, (Controller.Name, Controller.Type))
    
    dbContext.commit()
    print('executing time: ', time.datetime.now() - startTime)
    
def GetAllCobtrollersFromDataBase():
    startTime = time.datetime.now()
    
    query = "Select * from dbo.Controllers"
        
    cursor.execute(query)
    readedData = cursor.fetchall()
    
    controllersList = []
    
    for row in readedData:
        controllersList.append(Controller(row[0], row[1], row[2]))
    
    print('executing time: ', time.datetime.now() - startTime)
    
    return controllersList

for x in range(5):
    if x == 4:
        controllers = GetAllCobtrollersFromDataBase()
        print(controllers)
    else:
        print(x)
    
dbContext.close()


