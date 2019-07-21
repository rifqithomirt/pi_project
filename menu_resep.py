from guizero import App, Box, Text, TextBox, ListBox, PushButton
app = App( width=800, height=480, layout="grid" )
import requests
import json
load_produk_cycle = 10 * 1000
value_selected = "None"

def get_produk():
  global value_selected
  url_request = "http://36.89.152.19:8008/produksi-pi/produksi/index.php/tampilmerk"
  data = {'api_key': '2114d9d47905e856521b5fdfb8faecd5d16c8928'}
  headers = {'api_auth_key': '2114d9d47905e856521b5fdfb8faecd5d16c8928'}
  r = requests.post(url = url_request, data = data, headers=headers)
  obj_reseps = r.json()
  list_box.clear()
  index_list = 0
  for obj_resep in obj_reseps:
    index_list = index_list + 1
    list_box.insert( index_list, obj_resep['nama_merk'] )
  if value_selected in list_box.items:
    list_box.value = value_selected
    
def on_select( nama ):
  global value_selected
  val_list = list_box.value
  label_Produk.clear()
  label_Produk.append(val_list)
  value_selected = val_list
  print(val_list)
  
def get_resep():
  url_resep = "http://36.89.152.19:8008/produksi-pi/produksi/index.php/tampilmerk"
  
def load_value():
  print(list_box.value)

title_box = Box(app, width=800, height=50, grid=[0,0], border=True)
Text(title_box, text="PT. PERDAMAIAN INDONESIA")
Text(title_box, text="Penimbangan Minyak")

box = Box(app, width=800, height=430, align="left", grid=[0,1], border=True)
list_box = ListBox(box, items=[], width=400, height=430, grid=[0,1], align="left", command = on_select, scrollbar=True)
list_box.text_size = 20
get_produk()

label_Box    = Box(box, height=100, width=100, align="top", grid=[1,1])
label_Box    = Box(box, height=100, width=350, align="top", grid=[1,2], border=True)
label_Produk = Text(label_Box, text="Nama Produk", size=22)
label_Kg     = Text(label_Box, text="XXX g", size=24)

label_Box = Box(box, height=40, width=50, align="top", grid=[1,3])
button = PushButton(box, align="top", padx=40, grid=[1,4], text="Start", command=load_value)

list_box.repeat( load_produk_cycle , get_produk)

app.display()
