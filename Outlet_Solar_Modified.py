from guizero import App, Window, Text, TextBox, PushButton, yesno
from gpiozero import LED, Button
from time import sleep
from signal import pause
from datetime import datetime
import sqlite3
conn = sqlite3.connect('flowmeter.db')
jenis= "solar"
posisi= "outlet"

selector_auto = Button (15)
selector_manual = Button (14)
pump_motor = LED (18)
pump_motor.on()
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

def normalCounting():
    global old_signal
    if pulse_signal.value ==1 and old_signal == 0:
        cumulative_counting.value= int(cumulative_counting.value)+ 1
    old_signal = pulse_signal.value
    
def set_totalizer():
    totalizerVal.value = getTodayTotalizer() + round(0.064 * int (cumulative_counting.value)-1.1064,1)
    setByDay( totalizerVal.value )
        
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
