
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent

class Game:

    def setup_gamepads():
        devices = [InputDevice(path) for path in list_devices()]
        gamepads = []
        for device in devices:
            if device.name.strip() == "USB Gamepad":
                gamepads.append(InputDevice(device.path))

        return gamepads