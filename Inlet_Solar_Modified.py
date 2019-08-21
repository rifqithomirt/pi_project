from guizero import App, Window, Text, TextBox, PushButton
from gpiozero import Button, LED
from time import sleep
from datetime import datetime
import sqlite3
conn = sqlite3.connect('flowmeter.db')
jenis= "solar"
posisi= "inlet"

# Port Initialization #
pulse_signal = Button(8, pull_up=False)

# Variable Initialization #
old_signal=1


def createTable( ):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS flowmeter ( jenis text, posisi text, nilai double, produk text, jam datetime, status text)")
    conn.commit()

def insertValue( jenis, posisi, nilai, produk , jam):
    c = conn.cursor()
    c.execute("INSERT INTO flowmeter ( jenis, posisi, nilai, produk, jam ) VALUES(?,?,?,?,?)", [ jenis, posisi, nilai, produk, jam ])
    conn.commit()

def updateValue( nilai, jam ):
    c = conn.cursor()
    c.execute("UPDATE flowmeter SET nilai='"+ str(nilai) +"' WHERE jam='" + jam + "'")
    conn.commit()

def getTodayTotalizer():
    now = datetime.now();
    dateOnly = now.strftime("%Y-%m-%d")
    c = conn.cursor()
    arrayResult = c.execute('SELECT * FROM flowmeter WHERE jam = "' + dateOnly + '"')
    conn.commit()
    old_nilai = 0
    for row in arrayResult:
        old_nilai = row[2]
    return old_nilai
        
def setByDay( nilai ):
    now = datetime.now();
    dateOnly = now.strftime("%Y-%m-%d")
    c = conn.cursor()
    arrayResult = c.execute('SELECT * FROM flowmeter WHERE jam = "' + dateOnly + '"')
    old_nilai = 0
    count = 0
    for row in arrayResult:
        old_nilai = row[2]
        count = count + 1
    if( old_nilai != nilai ):
        print('tidaksama')
        if( count == 1 ):
            updateValue( nilai, dateOnly )
            conn.commit()
        elif( count == 0 ): 
            insertValue(jenis, posisi, nilai, jenis, dateOnly)
            conn.commit()
    else: 
        print('sama')

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
    pengisianVal.value = getTodayTotalizer() + round(0.24 * int (cumulative_counting.value),2)
    setByDay( pengisianVal.value )

# Calling Count Function
#pulse_signal.when_pressed = normalCounting

app=App(title="Inlet Weighing Golden Rubber Indonesia", bg=(255,255,255))
space1 =Text(app, text=" xxx", size=10, grid = [0,0])
space1.text_color = "white"
#title=Text(app, text=" Inlet Solar Weighing Golden Rubber Indonesia", size=20)
#title.bg = (255,255,255)
space2 =Text(app, text=" xxx", size=5)
space2.text_color = "white"
text_totalizer=Text(app, text="Jumlah Solar Didalam Tangki (liter)", size=30, grid=(1,0,1,1))
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
text_pengisian=Text(window, text="Jumlah Total Pengisian Solar (liter)", size=30, grid=(1,0,1,1))
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
