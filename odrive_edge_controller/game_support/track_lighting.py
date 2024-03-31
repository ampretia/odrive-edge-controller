from gpiozero import LED
from enum import Enum


class TrackLighting:

    class Control:

        def all_on():
            TrackLighting.BridgeLeds.GREEN_A.value.on()
            TrackLighting.BridgeLeds.GREEN_B.value.on()
            TrackLighting.BridgeLeds.BLUE_A.value.on()
            TrackLighting.BridgeLeds.BLUE_B.value.on()
            TrackLighting.BridgeLeds.WHITE.value.on()

        def all_off():
            TrackLighting.BridgeLeds.GREEN_A.value.off()
            TrackLighting.BridgeLeds.GREEN_B.value.off()
            TrackLighting.BridgeLeds.BLUE_A.value.off()
            TrackLighting.BridgeLeds.BLUE_B.value.off()
            TrackLighting.BridgeLeds.WHITE.value.off()


    class BridgeLeds(Enum):
        GREEN_A = LED(5)
        BLUE_A = LED(6)
        BLUE_B = LED(13)
        GREEN_B = LED(19)
        WHITE = LED(26)
