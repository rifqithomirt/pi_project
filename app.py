from guizero import App, Window, Text, TextBox, PushButton, yesno
from gpiozero import LED, Button
from time import sleep
from signal import pause

selector_auto = Button (15)
selector_manual = Button (14)
pump_motor = LED (18)
pump_motor.on()
pulse_signal = Button(8, pull_up=False)

# Variable Initialization #
old_signal=1

def pulseVal():
    pulse_value.value=pulse_signal.value

def normalCounting():
    global old_signal
    if pulse_signal.value ==1 and old_signal == 0:
        cumulative_counting.value= int(cumulative_counting.value)+ 1
    old_signal = pulse_signal.value
    
def set_totalizer():
    totalizerVal.value = round(0.064 * int (cumulative_counting.value)-1.1064,1)
    
#def auto_state_StartButton():
#    if selector_auto.is_pressed and pump_motor.value==1:
 #       button_start.enable()
  #  else:
   #     button_start.disable()
        
#def auto_state_StopButton():
  #  if selector_auto.is_pressed:
  #      button_stop.enable()
   # else:
    #    button_stop.disable()
        
def operation_status():
    if selector_auto.is_pressed:
        text_status.set("Auto Mode")
        pump_motor.off()
    elif selector_manual.is_pressed:
        text_status.set("Manual Mode")
        pump_motor.on()
    else:
        text_status.set("OFF")
        pump_motor.on()
        
#def start_confirmation():
 #   start = yesno("Konfirmasi Start", "Apakah anda yakin memulai mode auto?")
  #  if start==True:
   #     sleep(1)
    #    pump_motor.off()


#def stop():
    #sleep(1)
    #pump_motor.on()  
    
app=App(title="Solar Outlet Weighing Golden Rubber Indonesia", layout="grid", bg=(255,255,255))

# Text Flowrate #
cumulative_counting =Text(app, text="0", size=14, grid=[0,0,1,1], align="left")
cumulative_counting.text_color= "black"
cumulative_counting.repeat (10,normalCounting)
#text_flowrate=Text(app, text=" Nilai Flowrate (liter/menit)", size=24, grid=[1,0,1,1])
pulse_value  =Text(app, text=pulse_signal.value, size=14, grid=[0,1,1,1], align="left")
pulse_value.text_color= "black"
pulse_value.repeat(100,pulseVal)

textspace =Text(app, text="xxxxxx", size=14, grid=[2,1,1,1], align="left")
textspace.text_color=(255,255,255)

# Start-Stop Button #
#button_start = PushButton(app, start_confirmation, text="Start", grid=[3,3,1,1])
#button_start.bg="green"
#button_start.text_color="White"
#button_start.width=8
#button_start.height=8
#button_start.repeat(1000, auto_state_StartButton)
#button_stop = PushButton(app, stop, text="Stop", grid=[4,3,1,1])
#button_stop.bg="red"
#button_stop.text_color="black"
#button_stop.width=8
#button_stop.height=8
#button_stop.repeat(1000, auto_state_StopButton)

text_totalizer=Text(app, text=" Jumlah Konsumsi Solar (liter)", size=30, grid=[1,2,1,1])
textspace =Text(app, text="xxxxxxxxxxxx", size=14, grid=[0,3,1,1], align="left")
textspace.text_color=(255,255,255)
textspace2 =Text(app, text="xx", size=14, grid=[3,3,1,1], align="left")
textspace2.text_color=(255,255,255)
totalizerVal =Text(app,text="0", size= 150, grid=[1,3,1,1])
totalizerVal.repeat(1000,set_totalizer)

# Text Status #
text_status =Text(app, text="", size=18, grid=[2,0,2,1], align="right")
text_status.text_color="white"
text_status.bg="green"
text_status.repeat(1000,operation_status)


app.full_screen = True
app.display()
