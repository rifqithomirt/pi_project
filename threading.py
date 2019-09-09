import time

hdur = 5.0
adur = 11.0

def hello():
    print("hello, Timer")
    t = threading.Timer(hdur, hello)
    t.start()

def ates():
    print("hello, ates")
    t2 = threading.Timer(adur, ates)
    t2.start()

if __name__ == '__main__':
    t = threading.Timer(hdur, hello)
    t.start()
    t2 = threading.Timer(adur, ates)
    t2.start()
