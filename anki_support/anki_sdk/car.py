import time as t

import struct
import bleak
from loguru import logger

from typing import List

from .exceptions import NotConnected
from .protocol import Protocol
from .localization_transition import LocalalizationTransition
from .localization_position import LocalalizationPosition
from .abstractevent import Event
from .events.observer import IObserver

SERVICE_UUID: str = "BE15BEEF-6186-407E-8381-0BD89C4D8DF4"
READ_UUID: str = "BE15BEE0-6186-407E-8381-0BD89C4D8DF4"
WRITE_UUID: str = "BE15BEE1-6186-407E-8381-0BD89C4D8DF4"

def buffer_str(buffer):
        text = "["
        for v in list(buffer):
            text += f"{v:02X} "
        
        text = text.strip()

        text += "]"
        return text


class CommandList:
    """All found BLE commands

    Commands:
        BLE Connection:
            DISCONNECT (bytes): Command for disconnect.\n
            PING_REQUEST (bytes): Command to send a ping request.\n
            PING_RESPONSE (bytes): Response from the vehicle to ping.\n
            VERSION_REQUEST (bytes): Command to send a version request\n
            VERSION_RESPONSE (bytes): Response from the vehicle to version.\n
        -------------------------------------------------------------------\n
        Lights:
            SET_LIGHTS (bytes): Set vehicle lights.\n
            LIGHTS_PATTERN (bytes): Set light pattern.\n
        -------------------------------------------------------------------\n
        Driving Commands:
            SET_SPEED (bytes): Set vehicle speed and accel.\n
            CHANGE_LANE (bytes): Change vehicle lane.\n
            CANCEL_LANE_CHANGE (bytes): Cancel lane change.\n
            TURN_180 (bytes): Turn 180.\n
        -------------------------------------------------------------------\n
        Misc commands:
            SDK_MODE (bytes): Enable SDK Mode.\n
            RESET_LANE (bytes): Enable SDK Mode.\n
        -------------------------------------------------------------------\n
    """

    # BLE Connections
    DISCONNECT: bytes = 0xD
    # Ping request / response
    PING_REQUEST: bytes = 0x16
    PING_RESPONSE: bytes = 0x17
    # Messages for checking vehicle version info
    VERSION_REQUEST: bytes = 0x18
    VERSION_RESPONSE: bytes = 0x19
    # Lights
    SET_LIGHTS: bytes = 0x1D
    LIGHTS_PATTERN: bytes = 0x33
    # Driving Commands
    SET_SPEED: bytes = 0x24
    CHANGE_LANE: bytes = 0x25
    CANCEL_LANE_CHANGE: bytes = 0x26
    TURN_180: bytes = 0x32
    # SDK Mode
    SDK_MODE: bytes = 0x90
    RESET_LANE: bytes = 0x2C

    def sdk(self):
        """Get byte command

        Returns:
            bytes: SDK Mode byte command
        """
        return self.SDK_MODE

    def __str__(self):
        """str

        Returns:
            String: Command list to send to car
        """
        return "Command list to send to car"


class Receive:
    """@notifyCallback types

    Commands:
        Connection:
            PING_RESPONSE (tuple): Response from the vehicle to ping.\n
        -------------------------------------------------------------------\n
        Track:
            TRACK_CHANGE (tuple): A new Track
            FINISHLINE: (tuple): Drive over finishline.\n
            SPECIAL_TRACK: (tuple): Drive over special track\n
            STRAIGHT_TRACK: (tuple): Drive over straight track.\n
    """

    class Connection:
        """Connection notify events

        Connection:
            PING_RESPONSE (tuple): Response from the vehicle to ping.\n
        """

        PING_RESPONSE: int = (23, 1) #  0x17 0x01

    class Track:
        """Track notify events

        Track:
            TRACK_CHANGE (tuple): A new Track. \n
            FINISHLINE: (tuple): Drive over finishline.\n
            SPECIAL_TRACK: (tuple): Drive over special track\n
            STRAIGHT_TRACK: (tuple): Drive over straight track.\n
        """

        TRACK_CHANGE: int = (17, 0)  # 0x11 0x00
        FINISHLINE: int = (34, 16)   # 0x22 0x10
        SPECIAL_TRACK: int = (6, 0)   # 0x06 0x00
        STRAIGHT_TRACK: int = (38, 16)  # 0x26 0x10

    # UNKNOWN: int = (23, 13)
    # UNKNOWN: int = (22, 13)
    # UNKNOWN: int = 16


class Car:
    
    # Args:
    #    car_address (str): vehicle MAC-address
    #    cat_name (str): name
    def __init__(self, car_address: str, car_name: str, debug: bool = False):
        self.address: str = car_address
        self.name = car_name

        self.client: bleak.BleakClient = bleak.BleakClient(self.address)

        # connection status
        self.connected: bool = False
        self.wait_ping: bool = False
        self.notify_events: dict = {}

        # tmp var
        self.debug = debug
        self.before = ""
        self.start_ping_time = None

    # Get object as string
    def __str__(self):
        return f"Anki Overdrive car {self.name} | {self.address}"

    def __repr__(self) -> str:
        return self.__str__()

    # # Register the notifycallback type
    # def notifycallback(
    #     self,
    #     event: tuple[int, int] | Receive | Receive.Track | Receive.Connection = (17, 0),
    # ):
    #     """@decorator

    #     Args:
    #         event (tuple[int, int]): Code when it should get triggered. Defaults to (17, 0).
    #     """

    #     def wrapper(func):
    #         if event in self.notify_events:
    #             self.notify_events[event].append(func)
    #         else:
    #             self.notify_events[event] = []
    #             self.notify_events[event].append(func)
    #         return func

    #     return wrapper

    # Send BLE command to car
    async def send_command(self, command: bytes):
        """Send BLE command to car

        Args:
            command (bytes): Command that should get send.
        """
        if self.connected:
            command = struct.pack("B", len(command)) + command
            await self.client.write_gatt_char(WRITE_UUID, command)
        else:
            raise NotConnected("Not connected to vehicle")

    async def connect(self):
        """Connect with car

        Returns:
            bool: Connected
        """
        await self.client.connect()
        self.connected: bool = True
        await self.send_command(b"\x90\x01\x01")
        return self.name

    async def ping(self):
        """Get the ping to vehicle

        Returns:
            ping (int): Ping in ms.
        """
        command = struct.pack("<BBB", CommandList.PING_REQUEST, 0x01, 0x01)
        await self.send_command(command)
        self.start_ping_time: int = t.time_ns()
        self.wait_ping: bool = True
        while self.wait_ping:
            t.sleep(0)
        return self.start_ping_time

    # disconnect and slow down the car
    async def disconnect(self, stop_car: bool = True):
        """Disconnect from vehicle

        Args:
            stop_car (bool): Forcestop car.

        Returns:
            worked (bool): Disconnect worked.
        """
        try:
            if self.client.is_connected:
                if stop_car:
                    command = struct.pack("<BHHB", CommandList.SET_SPEED, 0, 1000, 0x01)
                    await self.send_command(command)

                t.sleep(0.5)
                await self.send_command(
                    struct.pack("<BB", CommandList.DISCONNECT, 0x01)
                )
                self.connected = False
                await self.client.disconnect()
                return True
            else:
                raise NotConnected("Car not connected")
        except KeyboardInterrupt:
            return False

    def build_message(self, data):

        match data[1]:
            case 0x29:
                return LocalalizationTransition(data[0], data[1],data[2:],"").build()
            case 0x27:
                return LocalalizationPosition(data[0], data[1],data[2:],"").build()
            case _:
                return Event(data[0],data[1],data[2:],"")

    

    # Start to receive notify
    async def start_notify(self, observer):
        """Starts the notification callback"""

        async def notify(sender, data: bytearray):
            if data == self.before:
                return
            self.before = data

            # if self.wait_ping and data[1] == Receive.Connection.PING_RESPONSE:
            #     logger.info("ping response...")
            #     self.start_ping_time = t.time_ns() - self.start_ping_time
            #     self.start_ping_time /= 1000000
            #     self.wait_ping = False

            msg = self.build_message(data)    
            if msg:
                await self._notify(msg)

        self._attach(observer)

        logger.info("Starting event loop")
        await self.client.start_notify(READ_UUID, notify)

    async def stop_notify(self, observer):
        """Stops the notification callback"""
        if self.connected:
            await self.client.stop_notify(READ_UUID)
            self._detach(observer)

    def _get_car_name(advertised):
        data_table: list = advertised.manufacturer_data[61374]
        value = bytearray(data_table)
        car_name = Car._decodeCarname(value)
        return car_name

    def _decodeCarname(manufacturerData):
        carId = manufacturerData[1]
        carnames = {
            0: "x52",
            8: "Groundshock",
            9: "Skull",
            10: "Thermo",
            11: "Nuke",
            12: "Guardian",
            14: "Bigbang",
            15: "Free Wheel",
            16: "x52",
            17: "x52 Ice",
            18: "MXT",
            19: "Ice Charger",
        }

        if carId in carnames:
            return carnames[carId]
        else:
            return "Unknown"

    async def scanner(active: bool = True):
        device_list = await bleak.BleakScanner.discover(return_adv=True)
        result: list = []
        if len(device_list) == 0:
            return list

        for n, data in device_list.items():
            address = n
            (device, advertised) = data

            if device.name is not None:
                if "Drive" in device.name:
                    if active:
                        if "P" not in device.name:
                            c = Car(address, Car._get_car_name(advertised))
                            result.append(c)
                    else:
                        c = Car(address, Car._get_car_name(advertised))
                        result.append(c)

        return result

    
    _observers: List[IObserver] = []

    def _attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _detach(self, observer: IObserver) -> None:
        self._observers.remove(observer)

    async def _notify(self, event) -> None:
        for observer in self._observers:
            await observer.update(event)