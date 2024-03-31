from .abstractevent import Event
import struct

# anki_vehicle_msg_battery_level_response {
#     uint8_t     size;
#     uint8_t     msg_id;
#     uint16_t    battery_level;
# }
class BatteryResponse(Event):

    def build(self):
        pack_format = "<H"

        (self.battery_level) = struct.unpack(pack_format, self.payload)

        return self

    def get_level(self):
        return self.battery_level[0]
    
    def __str__(self):
        return f"[{self.name}] battery=={self.battery_level[0]}"
    
    def __repr__(self):
        return self.__str__()