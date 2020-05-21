
from visual.controls import *
import serial
import string



# Define constants
# comp filter bandwidth (rad/s)
k = 4. #was 0.25

#pushpak timeframe (sec)
T = 1/160.

# define integrator class for use in comp filter(rectangular for now)
class Integrator:
    def __init__(self, SamplePeriod = 1., InitialCondition = 0.):
        self.T = SamplePeriod
        self.State = InitialCondition
    def __call__(self, Input=0.):
        self.State += self.T * Input
        return self.State
        
       
class Process_MPU_Data:
    previous_input = "0,0,0\n"
    
    def Read_Data(self):
        try:
            line = self.ser.readline()   
            input1 = line.split(',')
            angle_x = string.atof(input1[0])
            angle_y = string.atof(input1[1])
            angle_z = string.atof(input1[2])

        except: # if anything goes wrong, re- use the previous input
            print("Error reading line, using previous data")
            line = self.previous_input  
            input1 = string.split(line, ',')
            angle_x = string.atof(input1[0])
            angle_y = string.atof(input1[1])
            angle_z = string.atof(input1[2])

        self.previous_input = line
        return angle_x, angle_y, angle_z 
        
    def __init__(self,Com_Port,Baud):
        #open serial port
        self.ser = serial.Serial(Com_Port -1 ,Baud) #to open COM4, use value 3.
        self.ser.setTimeout(1) # time out after 1 second
        # clear data buffer to prevent spurious data when arduino is first plugged into PC
        self.ser.flushInput()
        self.x_degr =0  
        self.y_degr =0
        self.z_degr =0

    
    def __call__(self):
        angle_x, angle_y, angle_z = self.Read_Data()
        # extra steps
        x_degr= angle_x 
        y_degr= angle_y 
        z_degr= angle_z 
        
        return x_degr, y_degr, z_degr
          
        

mybox =box(pos = vector (0,0,0),color = color.orange, axis=(1.,0.,0.))
label (pos=(0,0), text = 'Sensor Motion')
freezelabel = label(pos=(0,-1.,0), 
    text = "Reset Arduino code or re-plug your power source.")
mypointerx = arrow(pos= vector (0,0,0), axis=(0,0,-2), shaftwidth=0.1,color = color.red)    
mypointery = arrow(pos= vector (0,0,0), axis=(-2,0,0), shaftwidth=0.1,color = color.blue)
mypointerz = arrow(pos= vector (0,0,0), axis=(0,2,0), shaftwidth=0.1,color = color.green)
label( pos=(0,2,0), text='+z' )
label( pos=(-2,0,0), text='+y' )
label( pos=(0,0,-2), text='+x' )
#mypointerz = arrow(pos=(0,2,1), axis=(5,0,0), shaftwidth=1,color = color.green)

# file to debug code
###file = open("C:\\data.csv",'w')
###file.write("(-xgyrodeg),(-ygyrodeg),zgyrodeg,\
###x_comp_filter,y_comp_filter,xacc,yacc,(-zacc),anglez\n")


# open serial port input and initialize sensors
input_data = Process_MPU_Data(Com_Port = 14,Baud = 9600)

x_degr,y_degr,z_degr = input_data.Read_Data()





# turn off "don't move board" message
freezelabel.visible = 0



# initialize cube 
up_copy = mybox.up
mybox.rotate(angle=y_degr, axis = cross(mybox.axis,mybox.up))
up_copy.rotate(angle=y_degr, axis = cross(mybox.axis,mybox.up))
mybox.rotate(angle=x_degr, axis = mybox.axis)
up_copy.rotate(angle=x_degr, axis = mybox.axis)



# spin cubes based on integrating 
x0,y0,z0=0,0,0
while 1:
    
    x_new, y_new, z_new = input_data.Read_Data()
    x_degr=x_new-x0
    y_degr=y_new-y0
    z_degr=z_new-z0
   # print(x_degr,y_degr,z_degr)      
    dtx = radians(x_degr )
    dty = radians(y_degr)
    dtz = radians(z_degr)
    # using raw rates to drive cube
    # for any vector V, dV/dt = omega x V, so V = V + dV = V + (omega x V) dt
    mybox.axis = norm(mybox.axis + cross((-dtx,dtz,-dty),mybox.axis))
    # then rotate about the x-axis
    mybox.rotate(angle = dtx, axis = mybox.axis)
    x0=x_new
    y0=y_new
    z0=z_new
    
   

