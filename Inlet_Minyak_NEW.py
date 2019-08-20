from guizero import App, Window, Text, TextBox, PushButton
from gpiozero import Button, LED
from time import sleep

# Port Initialization #
pulse_signal = Button(8, pull_up=False)

# Variable Initialization #
old_signal=1


def pulseVal():
    pulse_value.value=pulse_signal.value
def pengisian():
    window.show()
    window.full_screen = True
def monitoring():
    window.hide()
    
def normalCounting():
    global old_signal
    if pulse_signal.value ==1 and old_signal == 0:
        cumulative_counting.value= int(cumulative_counting.value)+ 1
    old_signal = pulse_signal.value
    
def set_totalizer():
    pengisianVal.value = int(0.047 * int (cumulative_counting.value))
    #pengisianVal.value = round(0.049 * int (cumulative_counting.value),0)

# Calling Count Function
#pulse_signal.when_pressed = normalCounting

app=App(title="Inlet Weighing Golden Rubber Indonesia", bg=(255,255,255))
space1 =Text(app, text=" xxx", size=10, grid = [0,0])
space1.text_color = "white"
#title=Text(app, text=" Inlet Solar Weighing Golden Rubber Indonesia", size=20)
#title.bg = (255,255,255)
space2 =Text(app, text=" xxx", size=5)
space2.text_color = "white"
text_totalizer=Text(app, text="Jumlah Minyak Didalam Tangki (liter)", size=30, grid=(1,0,1,1))
totalizerVal =Text(app,text="0", size=140)
button_pengisian = PushButton(app, text=">>", command=pengisian, align = "bottom")
#button_pengisian.bg="green"
#button_pengisian.text_color="white"
button_pengisian.width=5
button_pengisian.height=2

window=Window(app, title="Inlet Weighing Golden Rubber Indonesia", bg=(255,255,255))
space1 =Text(window, text=" xxx", size=10)
space1.text_color = "white"
space2 =Text(window, text=" xxx", size=5)
space2.text_color = "white"
text_pengisian=Text(window, text="Jumlah Total Pengisian Minyak (liter)", size=30, grid=(1,0,1,1))
pengisianVal=Text(window,text="0", size=140)
pengisianVal.repeat (100, set_totalizer)
pulse_value =Text(window, text= pulse_signal.value, size=14)
pulse_value.text_color= "black"
pulse_value.repeat(100,pulseVal)
cumulative_counting =Text(window, text="0", size=14)
cumulative_counting.text_color= "black"
cumulative_counting.repeat (10,normalCounting)
button_send = PushButton(window, text="Send Data", command=monitoring)
button_send.bg="blue"
button_send.text_color="white"
button_send.width=12
button_send.height=2
button_monitoring = PushButton(window, text="<<", command=monitoring, align = "bottom")
#button_monitoring.bg="green"
#button_monitoring.text_color="white"
button_monitoring.width=5
button_monitoring.height=2
window.hide()

#button_reset = PushButton(app, text="Reset")
#button_reset.bg="white"
#button_reset.text_color="Black"
#button_reset.width=8

app.full_screen = True
app.display()