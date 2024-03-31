import struct
from enum import Enum



class CarLight:
    class Type(Enum):
        HEADLIGHTS = 0
        BRAKELIGHTS = 1
        FRONTLIGHTS = 2
        ENGINE = 3

    class Channel(Enum):
        RED = 0
        TAIL = 1
        BLUE = 2
        GREEN = 3
        FRONTL = 4
        FRONTR = 5
        COUNT = 6

    class Effect(Enum):
        STEADY = 0
        FADE = 1
        THROB = 2
        FLASH = 3
        RANDOM = 4

    class Config:
        def __init__(self, channel, effect, start, end, cycles_per_10_sec):
            self.channel = channel
            self.effect = effect
            self.start = start

            self.end = end
            self.cycles_per_10_sec = cycles_per_10_sec

        def pack(self):
            struct.pack(
                "<BBBBB",
                self.channel,
                self.effect,
                self.start,
                self.end,
                self.cycles_per_10_sec,
            )

    # class LightsPattern:
    #     def __init__(self, configs: List<CarLight.Config>):
    #         self.configs = configs

    #     def pack(self):
    #         format = "<BB15s"

    MAX_LIGHT_INTENSITY = 14
    MAX_LIGHT_TIME = 11
    MSG_C2V_SET_LIGHTS = 0x1D
    MSG_C2V_LIGHTS_PATTERN = 0x33

    def e(self) -> bytes:
        format = "<18s"
        return struct.pack(format,bytes([17,51,3,0,0,128,150,0,3,0,128,128,0,2,0,128,128,0]))

    def set_lights(self, mask: int) -> bytes:
        format = "<BB"
        buffer = struct.pack(format, CarLight.MSG_C2V_SET_LIGHTS, mask)
        return buffer
        # buffer= struct.pack(format,
        #     LIGHT_MSG,
        #     3,

        # )
