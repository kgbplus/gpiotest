#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import curses 
import random
import time

def termOn():
    curses.nocbreak()
    curses.echo()

def termOff():
    curses.cbreak()
    curses.noecho()

def MainScreen():
    coords = [[6,15],[7,15],[8,15],[9,15],[10,15],[11,15],[12,15],[13,15],[14,15],
            [6,42],[7,42],[8,42],[9,42],[10,42],[11,42],[12,42],[13,42],[14,42],
            [6,69],[7,69],[8,69],[9,69],[10,69],[11,69],[12,69],[13,69]]

    myscreen.erase()
    myscreen.addstr(1,0, "--------------------------------------------------------------------------------")
    myscreen.addstr(2,0, "|                          * Raspberry Pi GPIO test *                          |")
    myscreen.addstr(3,0, "--------------------------------------------------------------------------------")
    myscreen.addstr(4,0, "|                                                      *   Debounce            |")
    myscreen.addstr(4,2, RaspiModel + " detected (" + str(gpio_num) + " lines)")
    myscreen.addstr(4,68, str(debounce) + " ms")
    myscreen.addstr(5,0, "--------------------------------------------------------------------------------")
    if (gpio_num == 17):
        myscreen.addstr(6,0, "|      GPIO1 =           |      GPIO10  =            |                         |")
        myscreen.addstr(7,0, "|      GPIO2 =           |      GPIO11  =            |                         |")
        myscreen.addstr(8,0, "|      GPIO3 =           |      GPIO12  =            |                         |")
        myscreen.addstr(9,0, "|      GPIO4 =           |      GPIO13  =            |                         |")
        myscreen.addstr(10,0, "|      GPIO5 =           |      GPIO14  =            |                         |")
        myscreen.addstr(11,0, "|      GPIO6 =           |      GPIO15  =            |                         |")
        myscreen.addstr(12,0, "|      GPIO7 =           |      GPIO16  =            |                         |")
        myscreen.addstr(13,0, "|      GPIO8 =           |      GPIO17  =            |                         |")
        myscreen.addstr(14,0, "|      GPIO9 =           |                           |                         |")
    else:
        myscreen.addstr(6,0, "|      GPIO1 =           |      GPIO10  =            |      GPIO19 =           |")
        myscreen.addstr(7,0, "|      GPIO2 =           |      GPIO11  =            |      GPIO20 =           |")
        myscreen.addstr(8,0, "|      GPIO3 =           |      GPIO12  =            |      GPIO21 =           |")
        myscreen.addstr(9,0, "|      GPIO4 =           |      GPIO13  =            |      GPIO22 =           |")
        myscreen.addstr(10,0, "|      GPIO5 =           |      GPIO14  =            |      GPIO23 =           |")
        myscreen.addstr(11,0, "|      GPIO6 =           |      GPIO15  =            |      GPIO24 =           |")
        myscreen.addstr(12,0, "|      GPIO7 =           |      GPIO16  =            |      GPIO25 =           |")
        myscreen.addstr(13,0, "|      GPIO8 =           |      GPIO17  =            |      GPIO26 =           |")
        myscreen.addstr(14,0, "|      GPIO9 =           |      GPIO18  =            |                         |")
    myscreen.addstr(15,0,  "--------------------------------------------------------------------------------")
    myscreen.addstr(23,0,  "Q = Quit  P = Pause  D = Debounce  U = pullUp  1 = output_True 0 = output_False")

    for i in range(gpio_num):
        state_text = "True" if gpio_state[i] else "False"
        state_text = state_text + ("(1)" if gpio_pud[i] else "(0)")
        myscreen.addstr(coords[i][0], coords[i][1], state_text, 
                        curses.A_REVERSE if gpio_inout[i] else curses.A_NORMAL)

    myscreen.addstr(0,0, chr(int(random.random()*32) + 32))

    logwindow.erase()
    for i in range(0,5):
        logwindow.addstr(log[i])

    myscreen.move(21,0)
    myscreen.refresh()
    
def SendToLog(LogMessage):
    global log
    
    logwindow.erase()
    for i in range(0,4):
        log[i] = log[i+1]
        logwindow.addstr(log[i])
    
    log[4] = LogMessage
    logwindow.addstr(log[4])

def CheckKeys():
    global debounce
    global on_pause
    
    myscreen.nodelay(1)
    key = myscreen.getch()
    myscreen.nodelay(0)
    
    if key == ord('q') | ord('Q'):
        raise KeyboardInterrupt
    elif key == ord('p') | ord('P'):
        myscreen.addstr(21,0,"Paused. Press P again to continue")
        on_pause = 1
        while on_pause:
            key = myscreen.getch()
            if key == ord('p') | ord('P'):
                on_pause = 0
    elif key == ord('d') | ord('D'):
        try:
            termOn()
            myscreen.addstr(21,0,"Enter debounce value (ms): ")
            debounce_ = debounce
            debounce = int(myscreen.getstr())
            if (debounce < 0 or debounce > 5000):
                debounce = debounce_
                raise ValueError
            if (debounce_ != debounce):
                initGpio()
            termOff()
        except ValueError:
            myscreen.addstr(22,0,"Value not in range")
            termOff()
            myscreen.getch()
    elif key == ord('u') | ord('U'):
        try:
            termOn()
            myscreen.addstr(21,0,"Enter GPIO line number: ")
            num = int(myscreen.getstr())
            if (num < 1 or num > gpio_num):
                raise ValueError
            if (gpio_inout[num-1]):
                raise IOError
            myscreen.addstr(21,0,"Enter 0 for GPIO.PUD_DOWN or 1 GPIO.PUD_UP: ")
            pud = int(myscreen.getstr())
            if (pud != 1 and pud != 0):
                raise ValueError
            gpio_pud[num-1] = pud
            initGpio()
            termOff()
        except ValueError:
            myscreen.addstr(22,0,"Value not in range")
            termOff()
            myscreen.getch()
        except IOError:
            myscreen.addstr(22,0,"Output line cannot be pulled up")
            termOff()
            myscreen.getch()

def getPinFunctionName(pin):
    functions = {GPIO.IN:'Input',
                 GPIO.OUT:'Output',
                 GPIO.I2C:'I2C',
                 GPIO.SPI:'SPI',
                 GPIO.HARD_PWM:'HARD_PWM',
                 GPIO.SERIAL:'Serial',
                 GPIO.UNKNOWN:'Unknown'}
                 
    return functions[GPIO.gpio_function(pin)]
    
def getRaspiModel(argument):
    switcher = {
        "0002": "Model B Revision 1.0 256Mb",
        "0003": "Model B Revision 1.0 + ECN0001 256Mb",
        "0004": "Model B Revision 2.0 256Mb",
        "0005": "Model B Revision 2.0 256Mb",
        "0006": "Model B Revision 2.0 256Mb",
        "0007": "Model A 256Mb",
        "0008": "Model A 256Mb",
        "0009": "Model A 256Mb",
        "000d": "Model B Revision 2.0 512Mb",
        "000e": "Model B Revision 2.0 512Mb",
        "000f": "Model B Revision 2.0 512Mb",
        "0010": "Model B+ 512Mb",
        "0012": "Model A+ 256Mb",
        "a01041": "2 Model B 1Gb",
        "a21041": "2 Model B 1Gb",
        "900092": "Zero 512Mb",
        "a02082": "3 Model B 1Gb"
    }
    return switcher.get(argument, "not supported")
    
def getGpioNum(argument):
    switcher = {
        "0002": 17,
        "0003": 17,
        "0004": 17,
        "0005": 17,
        "0006": 17,
        "0007": 17,
        "0008": 17,
        "0009": 17,
        "000d": 17,
        "000e": 17,
        "000f": 17,
        "0010": 26,
        "0012": 26,
        "a01041": 26,
        "a21041": 26,
        "900092": 26,
        "a02082": 26
    }
    return switcher.get(argument, 17)

def initGpio():
    curses.savetty()
    #Init GPIO
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(0)
    for i in range(gpio_num):
        if (not gpio_inout[i]):
            GPIO.setup(gpio_ch[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN if gpio_pud[i] == 0 else GPIO.PUD_UP)
            GPIO.add_event_detect(gpio_ch[i], GPIO.BOTH, callback = gpio_callback, bouncetime = debounce) 
    curses.resetty()
    
def gpio_callback(channel):
    global gpio_state
    if ((not gpio_inout[gpio_ch.index(channel)]) and (not on_pause)):
        gpio_state[gpio_ch.index(channel)] = GPIO.input(channel)
	SendToLog("Channel " + str(channel) + "changed\n")

try:
    #Init curses
    myscreen = curses.initscr()
    logwindow = myscreen.subwin(6,80,17,0)
    termOff()

    #Detect Raspberry Pi model
    RaspiModel = getRaspiModel(GPIO.RPI_INFO['REVISION'])
    if (RaspiModel == "not supported"):
        raise NameError('hardware not supported')

    #Tune GPIO parameters
    gpio_num = getGpioNum(GPIO.RPI_INFO['REVISION'])
    if (gpio_num == 17):
        gpio_ch = [0,1,4,7,8,9,10,11,14,15,17,18,21,22,23,24,25]
    else:
        gpio_ch = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]
    debounce = 200

    #Init vars
    gpio_state = [0 for _ in range(gpio_num)]
    gpio_inout = [0 for _ in range(gpio_num)]
    gpio_pud = [0 for _ in range(gpio_num)]
    on_pause = 0
    log = ['' for _ in range(5)]

    #Init GPIO
    initGpio()

    #Main loop
    while True:
        MainScreen()
        CheckKeys()
        time.sleep(0.1)
    
except KeyboardInterrupt:
    myscreen.addstr(21,0,"Ctrl-C pressed")
    time.sleep(0.5)
    GPIO.cleanup()
    
finally: 
    termOn()
    curses.endwin()
    
