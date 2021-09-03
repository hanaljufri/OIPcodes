import tkinter as tk
#from tkinter import ttk
from tkinter import * 

import smbus
from time import sleep

i2c = smbus.SMBus(1)
I2C_ADD = 0x08 # Arduino I2C address

def writeI2C(data):
  i2c.write_byte(I2C_ADD, data)

def readI2C():
  inData = i2c.read_byte(I2C_ADD)
  return inData

def listenfunc(): 
	#check i2c data updated
	prevI2CData = 0
	while True: 
		I2Cdata = readI2C()
     	if I2Cdata != prevI2CData:
       		prevI2CData = I2Cdata
       		if I2Cdata == 4: 	
				print('4: data from arduino received')
			elif I2Cdata == 5:
				print('4: data from arduino received')
			sleep(0.1)

# function one: wash, dry, and sanitise
def functionone():
	b1.config(state = DISABLED)
	b2.config(state = DISABLED)
	b3.config(state = DISABLED)
	print('perform wash, dry, and sanitise')
	#writeI2C(1)
	#GPIO.cleanup()

# function two: wash and dry 
def functiontwo():
	b1.config(state = DISABLED)
	b2.config(state = DISABLED)
	b3.config(state = DISABLED)
	print('perform wash and dry')
	#writeI2C(2)
	#GPIO.cleanup()

# function three: sanitise
def functionthree():
	b1.config(state = DISABLED)
	b2.config(state = DISABLED)
	b3.config(state = DISABLED)
	print('perform sanitise')
	#writeI2C(3)
	#GPIO.cleanup()

root = Tk()

# creates the main window
root.geometry('310x178')
root.configure(background='#F0F8FF')
root.title('Cleaner')

# label to select option to perform
Label(root, text='Select option to perform', bg='#F0F8FF', font=('arial', 10, 'normal')).place(x=15, y=2)

# creates a button one
b1 = tk.Button(root, text='Wash, Dry, Sanitise', bg='#F0F8FF', font=('arial', 10, 'normal'), command=functionone, width = 20)
b1.place(x=75, y=33)

# creates a button two
b2 = Button(root, text='Wash, Dry', bg='#F0F8FF', font=('arial', 10, 'normal'), command=functiontwo, width = 20)
b2.place(x=75, y=73)


# creates a button three
b3 = Button(root, text='Sanitise', bg='#F0F8FF', font=('arial', 10, 'normal'), command=functionthree, width = 20)
b3.place(x=75, y=113)


root.mainloop()
