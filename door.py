import time
import RPi.GPIO as GPIO
#GPIO Setup
GPIO.setmode(GPIO.BCM)
#Pins Setup
StepPins = [25,24,23,18]
# Set all pins as output
for pin in StepPins:
  print "Setup pins"
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

#Variables
StepCounter=0
WaitTime=0.007
#WaitTime=0.00000000005
StepsPerRev=48
#RevCount=2083 #From one end to another
#TempVariables
LowLimit=28
HighLimit=35
#MaxSteps divided by 4
MaxState=100000


#Calculations
#CountPerRev=StepsPerRev/4
MaxStateDividByFour=MaxState/4

#Function for 4 steps clockwise
def spincw(steps):
  count=0
  while (count<steps):
    for pin in range(0, 4):
      xpin=StepPins[pin]
      GPIO.output(xpin, 1)
      time.sleep(WaitTime)
      GPIO.output(xpin, 0)
      print "Count",count,"Steps:",steps
      count=count+1

#Function for 4 steps counterclockwise
def spinccw(steps):
  count=0
  while (count<steps):
    for pin in range(0, 4):
      xpin=StepPins[3-pin]
      GPIO.output(xpin, 1)
      time.sleep(WaitTime)
      GPIO.output(xpin, 0)
      print "Count -",count,"Steps: -",steps
      count=count+1

#Read temperature from sensor
def readtemp():
  with open('/mnt/1wire/28.D59BA7040000/temperature') as f:
      for line in f:
          numbers_float = map(float, line.split())
          #work with numbers_float here
          #print numbers_float[0]
  return (numbers_float[0])

#Write state
def writestate(state):
  f = open("State.txt", "w");
  f.write(str(state))
  print f

#Read state
def readstate():
  f = open("State.txt", "r");
  print f
  for line in f.readlines():
    print line
  return line 

#READING TEMPERATURE
TempInside=readtemp()
#TempInside=29.00
print "Temperatuur sees:",TempInside

#Arvutused
if TempInside<LowLimit:
  print "Kinni"
  NewPercentage=0
elif TempInside>HighLimit:
  print "Lahti"
  NewPercentage=MaxState
else:
  print "Vahepealne"
  NewPercentage=round(((float(TempInside)-float(LowLimit))/(float(HighLimit)-float(LowLimit))),2)*MaxState
print "NewPercentage:",NewPercentage

print "Read:"
OldPercentage=readstate()
print "OldPercentage",OldPercentage

LastState=readstate()
print "Laststate was:",LastState

DoorDifference=float(NewPercentage)-float(LastState)
print DoorDifference

if DoorDifference<0:
  print "spinccw"
  #spinccw(abs((MaxState*DoorDifference/100)))
  spinccw(abs(DoorDifference))  
elif DoorDifference>0:
  print "spincw"
  #spincw(abs((MaxState*DoorDifference/100)))
  spincw(abs(DoorDifference))
else:
  print "do nothing"

#spincw(MaxState)

#spinccw(MaxState)



#WRITE STATE TO FILE
print "Write:"
writestate(NewPercentage)
