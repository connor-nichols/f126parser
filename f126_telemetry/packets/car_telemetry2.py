import ctypes

from ..constants import MAX_CARS
from ..header import PacketHeader


class CarTelemetry2Data(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_activeAeroMode", ctypes.c_uint8),                    # 0 = Corner mode, 1 = Straight mode
        ("m_activeAeroAvailable", ctypes.c_uint8),
        ("m_activeAeroActivationDistance", ctypes.c_uint16),
        ("m_overtakeAvailable", ctypes.c_uint8),
        ("m_overtakeActive", ctypes.c_uint8),
        ("m_overtakeActivationDistance", ctypes.c_uint16),
        ("m_regulations2026", ctypes.c_uint8),                   # 0 = pre-2026, 1 = 2026 regs applicable (spec: m_2026Regulations)
        ("m_drivingWrongWay", ctypes.c_uint8),
    ]


class PacketCarTelemetry2Data(ctypes.LittleEndianStructure):
    """269 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carTelemetry2Data", CarTelemetry2Data * MAX_CARS),
    ]
