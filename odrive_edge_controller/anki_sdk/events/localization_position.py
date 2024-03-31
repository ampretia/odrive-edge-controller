from .abstractevent import Event
import struct

# typedef struct anki_vehicle_msg_localization_position_update {
#     uint8_t     size;
#     uint8_t     msg_id;
#     uint8_t     location_id;
#     uint8_t     road_piece_id;
#     float       offset_from_road_center_mm;
#     uint16_t    speed_mm_per_sec;
#     uint8_t     parsing_flags;

#     /* ACK commands received */
#     uint8_t     last_recv_lane_change_cmd_id;
#     uint8_t     last_exec_lane_change_cmd_id;
#     uint16_t    last_desired_lane_change_speed_mm_per_sec;
#     uint16_t    last_desired_speed_mm_per_sec;
# } ATTRIBUTE_PACKED anki_vehicle_msg_localization_position_update_t;


class LocalizationPosition(Event):

    MASK_NUM_BITS = 0x0f
    MASK_INVERTED_COLOR = 0x80
    MASK_REVERSE_PARSING = 0x40
    MASK_REVERSE_DRIVING = 0x20

    def build(self):
        pack_format = "<BBfHBBBHH"

        (
            self.locationId,           # uint8  2bytes
            self.roadPieceId,         # 3
            self.offsetFromRoadCenter,
            self.speed,
            self.parsingFlags,
            self.lastRecvLaneChangeCmdId,
            self.lastExecLaneChangeCmdId,
            self.lastDesiredLaneChangeSpeedMmPerSec,
            self.lastDesiredSpeedMmPerSec,
        ) = struct.unpack(pack_format, self.payload)

        return self

    def get_speed(self):
        return self.speed

    def get_road_piece_id(self):
        return self.roadPieceId

    def get_location_id(self):
        return self.locationId

    def __str__(self):
        return f"[P] PieceID={self.roadPieceId} Locn={self.locationId} Offset={self.offsetFromRoadCenter}mm  Speed={self.speed}mm/s Flags={self.parsingFlags:02X}"

    def __repr__(self):
        return self.__str__()