from guizero import App, Text, TextBox, PushButton
from gpiozero import Button, LED
from time import sleep

# Port Initialization #
pump_motor = LED(23)
pump_motor.on()
selenoid_valve = LED(24)
selenoid_valve.on()
selector_auto = Button(14)
selector_manual = Button(15)
flowswitch = Button(18)
pulse_signal = Button(8, pull_up=False)
old_signal=1
tot=0

# Keypad Instruction #
def Keypad_0():
    input_target.append('0')
def Keypad_1():
    input_target.append('1')
def Keypad_2():
    input_target.append('2')
def Keypad_3():
    input_target.append('3')
def Keypad_4():
    input_target.append('4')
def Keypad_5():
    input_target.append('5')
def Keypad_6():
    input_target.append('6')
def Keypad_7():
    input_target.append('7')
def Keypad_8():
    input_target.append('8')
def Keypad_9():
    input_target.append('9')
def Clearapp():
    input_target.clear()
    
def start_button_enable():
    if (input_target.value!="" and pump_motor.value==1) and selector_auto.is_pressed:
        button_start.enable()
    else:
        button_start.disable()
        
def stop_button_enable():
    if selector_auto.is_pressed :
        button_stop.enable()
    else:
        button_stop.disable()
        
def operation_status():
    if selector_auto.is_pressed:
        text_status.set("Auto Mode")
    elif selector_manual.is_pressed:
        text_status.set("Manual Mode")
    else:
        text_status.set("OFF")

def pulseVal():
    pulse_value.value=pulse_signal.value
    
def totalizer_count():
    global tot
    tot = tot + 1
    totalizerVal.value = round(5.882 * tot +111.76 ,1)
    # round(6.593 * tot -24.521 ,1)      
    
def normalCounting():
    global old_signal
    if pulse_signal.value ==1 and old_signal == 0:
        cumulative_counting.value= int(cumulative_counting.value)+ 1
    old_signal = pulse_signal.value
    
#def set_totalizer():
    #totalizerVal.value = round(9.16 * int (cumulative_counting.value),0)
        
def start():
    global tot
    global a
    pump_motor.off()
    selenoid_valve.off()
    totalizerVal.value = 0
    tot=0
    totalizerVal.repeat(100,totalizer_count)
    a= int((int(input_target.value)*0.9-95)*19)
    #a= int((int(input_target.value)*0.8 + 24)*19)
    input_target.after(a, stop)
    
def stop():
    pump_motor.on()
    selenoid_valve.on()
    totalizerVal.cancel (totalizer_count)
    input_target.value = ""
    
    
# Calling Count Function
#pulse_signal.when_pressed = normalCounting

# Title #  
app=App(title="Outlet Minyak Weigher Golden Rubber Indonesia", layout="grid", bg=(255,255,255))
app.full_screen = True
textspace_up =Text(app, text="", size=14, grid=[0,1,2,1], align="left")
textspace_left =Text(app, text="xxx", size=14, grid=[0,4,1,1], align="left")
textspace_left.text_color=(255,255,255)
text_input =Text(app, text="Masukkan Nilai:", size=15, grid=[1,2,2,1], align="left")
textspace_center =Text(app, text="xxxxx", size=14, grid=[4,5,1,1], align="left")
textspace_center.text_color= "white"
#pulse_value =Text(app, text= pulse_signal.value, size=14, grid=[4,6,1,1], align="left")
#pulse_value.text_color= "black"
#pulse_value.repeat(10,pulseVal)
#cumulative_counting =Text(app, text="0", size=14, grid=[4,7,1,1], align="left")
#cumulative_counting.text_color= "black"
#cumulative_counting.repeat (10,normalCounting)

# Text Box #
input_target =TextBox(app, text="", grid=[1,3,3,1])
input_target.text_size = 30
input_target.bg="white"

# Keypad #
button1 = PushButton(app, Keypad_1, text="1", grid=[1,4,1,1])
button1.bg="black"
button1.text_color="white"
button1.width=5
button1.height=2
button1.text_size = 15
button2 = PushButton(app, Keypad_2, text="2", grid=[2,4,1,1])
button2.bg="black"
button2.text_color="white"
button2.width=5
button2.height=2
button2.text_size = 15
button3 = PushButton(app, Keypad_3, text="3", grid=[3,4,1,1])
button3.bg="black"
button3.text_color="white"
button3.width=5
button3.height=2
button3.text_size = 15
button4 = PushButton(app, Keypad_4, text="4", grid=[1,5,1,1])
button4.bg="black"
button4.text_color="white"
button4.width=5
button4.height=2
button4.text_size = 15
button5 = PushButton(app, Keypad_5, text="5", grid=[2,5,1,1])
button5.bg="black"
button5.text_color="white"
button5.width=5
button5.height=2
button5.text_size = 15
button6 = PushButton(app, Keypad_6, text="6", grid=[3,5,1,1])
button6.bg="black"
button6.text_color="white"
button6.width=5
button6.height=2
button6.text_size = 15
button7 = PushButton(app, Keypad_7, text="7", grid=[1,6,1,1])
button7.bg="black"
button7.text_color="white"
button7.width=5
button7.height=2
button7.text_size = 15
button8 = PushButton(app, Keypad_8, text="8", grid=[2,6,1,1])
button8.bg="black"
button8.text_color="white"
button8.width=5
button8.height=2
button8.text_size = 15
button9 = PushButton(app, Keypad_9, text="9", grid=[3,6,1,1])
button9.bg="black"
button9.text_color="white"
button9.width=5
button9.height=2
button9.text_size = 15
button = PushButton(app,text="", grid=[1,7,1,1])
button.bg="black"
button.text_color="white"
button.width=5
button.height=2
button.text_size = 15
button0 = PushButton(app, Keypad_0, text="0", grid=[2,7,1,1])
button0.bg="black"
button0.text_color="white"
button0.width=5
button0.height=2
button0.text_size = 15
clear = PushButton(app, Clearapp, text="CLEAR", grid=[3,7,1,1])
clear.bg="black"
clear.text_color="white"
clear.width=5
clear.height=2
clear.text_size = 15
# Displaying Flow Meter Value #
text_totalizer=Text(app, text=" Nilai Totalizer", grid=[5,3,2,1], align="left", size=40)
text_totalizer.bg=(255,255,255)
text_totalizer.text_color="black"
totalizerVal =Text(app, text="", grid=[5,4,2,1], align="right", size=30)
totalizerVal.bg=(255,255,255)
totalizerVal.text_color="black"
#totalizerVal.repeat(100,totalizer_count)
totalizer_unit =Text(app, text=" gram", grid=[7,4,1,1], align="left", size=20)
# Text Status #
text_status =Text(app, text="", size=20, grid=[5,1,2,1], align="right")
text_status.text_color="black"
text_status.bg="white"
text_status.repeat(1000,operation_status)
# Start-Stop Button #
button_start = PushButton(app, command=start, text="Start", grid=[5,5,1,3], align = "right")
button_start.bg="green"
button_start.text_color="White"
button_start.text_size=15
button_start.width=9
button_start.height=4
button_start.repeat(1000, start_button_enable)
button_stop = PushButton(app, command=stop, text="Stop", grid=[6,5,1,3])
button_stop.bg="red"
button_stop.text_color="White"
button_stop.text_size=15
button_stop.width=9
button_stop.height=4
#button_stop.repeat(1000, stop_button_enable)
       
app.display()


