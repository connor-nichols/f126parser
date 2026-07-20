import ctypes

from ..header import PacketHeader


class TimeTrialDataSet(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_carIdx", ctypes.c_uint8),
        ("m_teamId", ctypes.c_uint16),
        ("m_lapTimeInMS", ctypes.c_uint32),
        ("m_sector1TimeInMS", ctypes.c_uint32),
        ("m_sector2TimeInMS", ctypes.c_uint32),
        ("m_sector3TimeInMS", ctypes.c_uint32),
        ("m_tractionControl", ctypes.c_uint8),
        ("m_gearboxAssist", ctypes.c_uint8),
        ("m_antiLockBrakes", ctypes.c_uint8),
        ("m_equalCarPerformance", ctypes.c_uint8),
        ("m_customSetup", ctypes.c_uint8),
        ("m_valid", ctypes.c_uint8),
    ]


class PacketTimeTrialData(ctypes.LittleEndianStructure):
    """104 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_playerSessionBestDataSet", TimeTrialDataSet),
        ("m_personalBestDataSet", TimeTrialDataSet),
        ("m_rivalDataSet", TimeTrialDataSet),
    ]
