from enum import Enum


class Protocol:
    class UUID:
        SERVICE_UUID: str = "BE15BEEF-6186-407E-8381-0BD89C4D8DF4"
        READ_UUID: str = "BE15BEE0-6186-407E-8381-0BD89C4D8DF4"
        WRITE_UUID: str = "BE15BEE1-6186-407E-8381-0BD89C4D8DF4"

    class PositionUpdates:
        # Vehicle position updates
        LOCALIZATION_POSITION_UPDATE = 0x27
        LOCALIZATION_TRANSITION_UPDATE = 0x29
        LOCALIZATION_INTERSECTION_UPDATE = 0x2A
        VEHICLE_DELOCALIZED = 0x2B
        SET_OFFSET_FROM_ROAD_CENTER = 0x2C
        OFFSET_FROM_ROAD_CENTER_UPDATE = 0x2D

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

        BATTERY_REQUEST: bytes = 0x1a
        BATTERY_RESPONSE: bytes = 0x1b
        # Lights
        SET_LIGHTS: bytes = 0x1D
        LIGHTS_PATTERN: bytes = 0x33
        # Driving Commands
        SET_SPEED: bytes = 0x24
        CHANGE_LANE: bytes = 0x25
        CANCEL_LANE_CHANGE: bytes = 0x26
        TURN: bytes = 0x32
        # SDK Mode
        SDK_MODE: bytes = 0x90
        RESET_LANE: bytes = 0x2C

    class TurnType(Enum):
        VEHICLE_TURN_NONE = 0
        VEHICLE_TURN_LEFT = 1
        VEHICLE_TURN_RIGHT = 2
        VEHICLE_TURN_UTURN = 3
        VEHICLE_TURN_UTURN_JUMP = 4

    class TurnTrigger(Enum):
        VEHICLE_TURN_TRIGGER_IMMEDIATE = 0
        VEHICLE_TURN_TRIGGER_INTERSECTION = 1
