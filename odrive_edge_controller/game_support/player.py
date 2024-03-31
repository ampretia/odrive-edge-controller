from loguru import logger
from evdev import InputDevice, categorize, ecodes, list_devices, KeyEvent
from threading import Timer
from ..anki_sdk import Controller
from ..anki_sdk.events import IObserver, Event, OffTrack,LocalizationPosition, LocalizationTransition
from enum import Enum
import asyncio

class CntrlKeys(Enum):
    L = 292
    R = 293
    A = 289
    B = 290
    X = 288
    Y = 291


class Player(IObserver):
    def __init__(self, name, device, car):
        self.name = name
        self.device = device
        self.car = car
        self.boosting = False

    def __str__(self):
        return f"{self.name} | {self.device} | {self.car}"

    def __repr__(self) -> str:
        return self.__str__()

    def disconnect(self):
        self.car.disconnect()

    async def connect(self):
        self.car_name = await self.car.connect()
        logger.info(f"Connected to {self.car_name}")

        self.controller = Controller(self.car)
        await self.car.start_notify(self)

    async def update(self, event) -> None:

        if type(event) is OffTrack:
            logger.info(f"{self.name} {self.car_name}:: Off Track Event")
        elif type(event) is LocalizationPosition:
            # logger.info(f"{self.name} {self.car_name}:: Speed {event.get_speed()}")
            logger.info(f"{self.car_name} {event}")
        elif type(event) is LocalizationTransition:
            # logger.info(f"{self.name} {self.car_name}:: Speed {event.get_speed()}")
            logger.info(f"{self.car_name} {event}")
        # else:
        #     logger.info(f"{self.car_name} {event}")
            
            

    async def off_track(self) -> None:
        await self.controller.set_speed(0, 2000)
                            

    async def handle_events(self):
      
        async def boost_cancel():
            await asyncio.sleep(0.5)
            if self.boosting:                
                await self.controller.set_speed(
                                0, 450, limit=False
                            )
                logger.info("Boost cancelled")
            else:
                logger.info("Boost already cancelled")

        async for event in self.device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                keyevent = categorize(event)
                if keyevent.keystate == KeyEvent.key_down:
                    match keyevent.scancode:
                        case CntrlKeys.R.value:
                            await self.controller.right_lane(1.0)
                        case CntrlKeys.L.value:
                            await self.controller.left_lane(1.0)
                        case CntrlKeys.A.value:  # Accelerate
                            self.boosting = False
                            await self.controller.set_speed(1400, 700, limit=False)                            
                        case CntrlKeys.B.value:  # BRAKE
                            self.boosting = False
                            await self.controller.set_speed(0, 1000, limit=False)
                        case CntrlKeys.X.value:  # Boast
                            self.boosting = True
                            await self.controller.set_speed(2500, 2500, limit=False)
                            asyncio.create_task(boost_cancel())
                        case _:
                            logger.info(f"{self.name} {keyevent}")
                elif keyevent.keystate == KeyEvent.key_up:
                    match keyevent.scancode:
                        case CntrlKeys.A.value:
                            await self.controller.set_speed(
                                0, 450, limit=False
                            )  # coast
                        case CntrlKeys.B.value:
                            await self.controller.set_speed(
                                0, 450, limit=False
                            )  # coast
                        case CntrlKeys.X.value:
                            pass
                            # await self.controller.set_speed(
                            #     0, 450, limit=False
                            # )  # coast
                        case CntrlKeys.L.value:
                            pass
                        case CntrlKeys.R.value:
                            pass
                        case _:
                            logger.info(f"{self.name} {keyevent}")
