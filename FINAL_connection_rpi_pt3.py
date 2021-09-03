import tkinter as tk
from tkinter import * 
from tkinter import messagebox as mb

import smbus
from time import sleep


i2c = smbus.SMBus(1)
I2C_ADD = 0x07 # Arduino I2C address

def callfunc():
    x = 4
    writeI2C(x)

def listenfunc(): 
    #show label please wait
    waiting_label.pack()
    #check i2c data updated
    counter = int(0)
    prevI2CData = 0
    while True: 
        I2Cdata = readI2C()
        if I2Cdata != prevI2CData:
            prevI2CData = I2Cdata
            if I2Cdata == 5: 
                print('5: data from arduino received')
                print('do nothing')
                #inputdata()
            elif I2Cdata == 6:
                counter= counter +1
                print('6: data from arduino received')
                print("take pic")
                callfunc()
                if counter == 10:
                    #hide label please wait
                    waiting_label.pack_forget()
                    #show dialogbox say cleaning completed
                    mb.showinfo('Alert', 'Cleaning completed')
                    counter = 0
                    restart()
                    
                #writeI2C(4)                
            else:
                print("recieved a diff number")
                print(I2Cdata)
                #take pic + ml
                #inputdata()
            sleep(0.1)

def functionone():
	b1.config(state = DISABLED)
	b2.config(state = DISABLED)
	b3.config(state = DISABLED)
	print('perform wash, dry, and sterilise')
	writeI2C(1)
	listenfunc()
	#1GPIO.cleanup()
	
def functiontwo():
    b1.config(state = DISABLED)
    b2.config(state = DISABLED)
    b3.config(state = DISABLED)
    print('perform wash and dry')
    writeI2C(2)
    listenfunc()
	#GPIO.cleanup()

# function three: sanitise
def functionthree():
	b1.config(state = DISABLED)
	b2.config(state = DISABLED)
	b3.config(state = DISABLED)
	print('perform sterilise')
	writeI2C(3)
	listenfunc()
	#GPIO.cleanup()	

def writeI2C(data):
  i2c.write_byte(I2C_ADD, data)


def readI2C():
    inData = i2c.read_byte(I2C_ADD)
    x = int(inData)
    return x


#def inputdata():
#    print("pls input, 1/2/3")
#    x = input()
#    x = int(x)
#

#    if x == 1:
#        functionone(x)
#        listenfunc()
#    elif x == 2:
#        functiontwo(x)
#        listenfunc()
#    elif x == 3:
#        functionthree(x)
#        listenfunc()
#    else:
#        print("invalid")

# function one: wash, dry, and sanitise


# function two: wash and dry root = Tk()

# creates the main window
root = Tk()
root.geometry('510x300')
root.configure(background='#F0F8FF')
root.title('Cleaner')

# label to select option to perform
Label(root, text='Select which cleaning mode to perform', bg='#F0F8FF', font=('arial', 15, 'normal')).place(x=20, y=23)

# creates a button wash dry sterilise
b1 = tk.Button(root, text='Wash, Dry, Sterilise', bg='#F0F8FF', font=('arial', 15, 'normal'), command=functionone, width = 30)
b1.place(x=90, y=73)

# creates a button wash dry
b2 = Button(root, text='Wash, Dry', bg='#F0F8FF', font=('arial', 15, 'normal'), command=functiontwo, width = 30)
b2.place(x=90, y=133)


# creates a button sterilise 
b3 = Button(root, text='Sterilise', bg='#F0F8FF', font=('arial', 15, 'normal'), command=functionthree, width = 30)
b3.place(x=90, y=193)

#create label please wait
waiting_label = tk.Label(root, text="Waiting for task to finish.", font=('arial', 15, 'normal'))

def restart():
	b1.config(state=NORMAL)
	b2.config(state=NORMAL)
	b3.config(state=NORMAL)

root.mainloop()