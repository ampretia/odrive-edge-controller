from .abstractevent import Event
import struct

# anki_vehicle_msg_battery_level_response {
#     uint8_t     size;
#     uint8_t     msg_id;
#     uint16_t    battery_level;
# }
class VersionResponse(Event):

    def build(self):
        pack_format = "<HH"

        (self.version, self.version2) = struct.unpack(pack_format, self.payload)

        return self

    def get_version(self):
        return f"{self.version} :: {self.version2}"
    
    def __str__(self):
        return f"[{self.name}] Version=={self.version} : {self.version2}"
    
    def __repr__(self):
        return self.__str__()