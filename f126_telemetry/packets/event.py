import ctypes

from ..constants import EVENT_STRING_CODE_LEN
from ..header import PacketHeader


class _FastestLap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8), ("lapTime", ctypes.c_float)]


class _Retirement(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8), ("reason", ctypes.c_uint8)]


class _DRSDisabled(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("reason", ctypes.c_uint8)]


class _TeamMateInPits(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]


class _RaceWinner(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]


class _Penalty(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("penaltyType", ctypes.c_uint8),
        ("infringementType", ctypes.c_uint8),
        ("vehicleIdx", ctypes.c_uint8),
        ("otherVehicleIdx", ctypes.c_uint8),
        ("time", ctypes.c_uint8),
        ("lapNum", ctypes.c_uint8),
        ("placesGained", ctypes.c_uint8),
    ]


class _SpeedTrap(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("vehicleIdx", ctypes.c_uint8),
        ("speed", ctypes.c_float),
        ("isOverallFastestInSession", ctypes.c_uint8),
        ("isDriverFastestInSession", ctypes.c_uint8),
        ("fastestVehicleIdxInSession", ctypes.c_uint8),
        ("fastestSpeedInSession", ctypes.c_float),
    ]


class _StartLights(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("numLights", ctypes.c_uint8)]


class _DriveThroughPenaltyServed(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8)]


class _StopGoPenaltyServed(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("vehicleIdx", ctypes.c_uint8), ("stopTime", ctypes.c_float)]


class _Flashback(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("flashbackFrameIdentifier", ctypes.c_uint32),
        ("flashbackSessionTime", ctypes.c_float),
    ]


class _Buttons(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("buttonStatus", ctypes.c_uint32)]


class _Overtake(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("overtakingVehicleIdx", ctypes.c_uint8), ("beingOvertakenVehicleIdx", ctypes.c_uint8)]


class _SafetyCar(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [("safetyCarType", ctypes.c_uint8), ("eventType", ctypes.c_uint8)]


class _Collision(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("vehicle1Idx", ctypes.c_uint8),
        ("vehicle2Idx", ctypes.c_uint8),
        ("severity", ctypes.c_uint8),
    ]


class EventDataDetails(ctypes.Union):
    """Interpret only the member matching the packet's m_eventStringCode."""

    _pack_ = 1
    _fields_ = [
        ("FastestLap", _FastestLap),
        ("Retirement", _Retirement),
        ("DRSDisabled", _DRSDisabled),
        ("TeamMateInPits", _TeamMateInPits),
        ("RaceWinner", _RaceWinner),
        ("Penalty", _Penalty),
        ("SpeedTrap", _SpeedTrap),
        ("StartLights", _StartLights),
        ("DriveThroughPenaltyServed", _DriveThroughPenaltyServed),
        ("StopGoPenaltyServed", _StopGoPenaltyServed),
        ("Flashback", _Flashback),
        ("Buttons", _Buttons),
        ("Overtake", _Overtake),
        ("SafetyCar", _SafetyCar),
        ("Collision", _Collision),
    ]


class PacketEventData(ctypes.LittleEndianStructure):
    """45 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_eventStringCode", ctypes.c_uint8 * EVENT_STRING_CODE_LEN),
        ("m_eventDetails", EventDataDetails),
    ]


# Maps the 4-byte event string code to (union member name, human label).
# member name is None for events that carry no payload in m_eventDetails.
EVENT_CODES = {
    b"SSTA": (None, "Session Started"),
    b"SEND": (None, "Session Ended"),
    b"FTLP": ("FastestLap", "Fastest Lap"),
    b"RTMT": ("Retirement", "Retirement"),
    b"DRSE": (None, "DRS Enabled"),
    b"DRSD": ("DRSDisabled", "DRS Disabled"),
    b"TMPT": ("TeamMateInPits", "Team Mate In Pits"),
    b"CHQF": (None, "Chequered Flag"),
    b"RCWN": ("RaceWinner", "Race Winner"),
    b"PENA": ("Penalty", "Penalty"),
    b"SPTP": ("SpeedTrap", "Speed Trap"),
    b"STLG": ("StartLights", "Start Lights"),
    b"LGOT": (None, "Lights Out"),
    b"DTSV": ("DriveThroughPenaltyServed", "Drive Through Served"),
    b"SGSV": ("StopGoPenaltyServed", "Stop Go Served"),
    b"FLBK": ("Flashback", "Flashback"),
    b"BUTN": ("Buttons", "Button Status"),
    b"RDFL": (None, "Red Flag"),
    b"OVTK": ("Overtake", "Overtake"),
    b"SCAR": ("SafetyCar", "Safety Car"),
    b"COLL": ("Collision", "Collision"),
}


def describe_event(packet: PacketEventData) -> dict:
    """Decode m_eventStringCode + pick the right union member. Returns {} for unknown codes."""

    code = bytes(packet.m_eventStringCode)
    entry = EVENT_CODES.get(code)
    if entry is None:
        return {}
    member_name, label = entry
    details = {}
    if member_name is not None:
        member = getattr(packet.m_eventDetails, member_name)
        details = {name: getattr(member, name) for name, *_ in member._fields_}
    return {"code": code.decode("ascii"), "label": label, "details": details}
