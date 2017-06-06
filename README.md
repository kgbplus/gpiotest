# gpiotest.py

Small console utility to do gpio pin monitor & Raspberry Pi DYI projects debugging

![screenshot](https://github.com/kgbplus/gpiotest/blob/master/gpiotest.png)

To start, enter ```sudo python gpiotest.py``` from console

## Keyboard commands:

Q - Quit program

P - Pause program, to continue press 'P' again

D - Set debounce value (ms)

U - Configure pullup resistors for input pins. Enter GPIO line number (not pin number on the plug), then enter value for pullup (0 for GPIO.PUD_DOWN or 1 GPIO.PUD_UP)

O - Press to output something. Enter GPIO line number and value. Pin became 'output' and program stop monitoring it's state.

I - Return pin to 'input' state. Program will show it's state.

## Pin indication:
1. Input pin not inversed, output inversed
2. After equal sign - pin state True/False (1/0)
3. In the brackets - pullup resistor state (^) - High or (v) - Low

## Command line options:
You can use ```-g``` or ```--gpio_num``` switch with ```17``` or ```26``` parameter to override automatic hardware detection.

## Questions
Feel free to contact me on [Raspberry Pi forum](https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=167609) or by [e-mail](roman@mindlin.ru)
