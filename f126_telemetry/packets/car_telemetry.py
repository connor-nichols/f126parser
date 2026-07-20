import ctypes

from ..constants import MAX_CARS
from ..header import PacketHeader


class CarTelemetryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_speed", ctypes.c_uint16),                       # km/h
        ("m_throttle", ctypes.c_float),                     # 0.0 to 1.0
        ("m_steer", ctypes.c_float),                        # -1.0 (full left) to 1.0 (full right)
        ("m_brake", ctypes.c_float),                        # 0.0 to 1.0
        ("m_clutch", ctypes.c_uint8),                       # 0 to 100
        ("m_gear", ctypes.c_int8),                          # 1-8, N=0, R=-1
        ("m_engineRPM", ctypes.c_uint16),
        ("m_drs", ctypes.c_uint8),                          # 0 = off, 1 = on
        ("m_revLightsPercent", ctypes.c_uint8),
        ("m_revLightsBitValue", ctypes.c_uint16),
        ("m_brakesTemperature", ctypes.c_uint16 * 4),
        ("m_tyresSurfaceTemperature", ctypes.c_uint8 * 4),
        ("m_tyresInnerTemperature", ctypes.c_uint8 * 4),
        ("m_engineTemperature", ctypes.c_uint8),
        ("m_tyresPressure", ctypes.c_float * 4),
        ("m_surfaceType", ctypes.c_uint8 * 4),
    ]


class PacketCarTelemetryData(ctypes.LittleEndianStructure):
    """1448 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carTelemetryData", CarTelemetryData * MAX_CARS),
        ("m_mfdPanelIndex", ctypes.c_uint8),                # 255 = MFD closed
        ("m_mfdPanelIndexSecondaryPlayer", ctypes.c_uint8),
        ("m_suggestedGear", ctypes.c_int8),                 # 0 if no gear suggested
    ]
