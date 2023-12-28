
from loguru import logger
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent

from ..anki_sdk import Controller

from ..anki_sdk.events import IObserver

class Player(IObserver):
    def __init__(self, name, device, car):
        self.name = name
        self.device = device
        self.car = car

    def __str__(self):
        return f"{self.name} | {self.device} | {self.car}"

    def __repr__(self) -> str:
        return self.__str__()

    def disconnect(self):
        self.car.disconnect()

    async def connect(self):
        car_name = await self.car.connect()
        print(f"Connected to {car_name}")

        self.controller = Controller(self.car)
        await self.car.start_notify(self)
        logger.info("pinging...")
        # await self.car.ping()

    async def update(self,  event) -> None:
        logger.info(f"Event {self.name}:: {event}")

    async def handle_events(self):
        async for event in self.device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                if keyevent.keystate == KeyEvent.key_down:
                    match keyevent.scancode:
                        case 293:
                            await self.controller.right_lane(1.0)
                        case 292:
                            await self.controller.left_lane(1.0)
                        case 289:
                            await self.controller.set_speed(1000, 500)
                        case _:
                            logger.info(f"{self.name} {keyevent}")
                elif keyevent.keystate == KeyEvent.key_up:
                    match keyevent.scancode:
                        case 289:
                            await self.controller.set_speed(0, 1000)
                        case _:
                            logger.info(f"{self.name} {keyevent}")
