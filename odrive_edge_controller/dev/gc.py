#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices



devices = [InputDevice(path) for path in list_devices()]
#creates object 'gamepad' to store the data
print([d.name for d in devices])
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event5')

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        print(event)

