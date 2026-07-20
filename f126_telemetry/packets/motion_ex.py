import ctypes

from ..header import PacketHeader


class PacketMotionExData(ctypes.LittleEndianStructure):
    """273 bytes. Extra player-car-only data. Wheel arrays are ordered RL, RR, FL, FR."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_suspensionPosition", ctypes.c_float * 4),
        ("m_suspensionVelocity", ctypes.c_float * 4),
        ("m_suspensionAcceleration", ctypes.c_float * 4),
        ("m_wheelSpeed", ctypes.c_float * 4),
        ("m_wheelSlipRatio", ctypes.c_float * 4),
        ("m_wheelSlipAngle", ctypes.c_float * 4),
        ("m_wheelLatForce", ctypes.c_float * 4),
        ("m_wheelLongForce", ctypes.c_float * 4),
        ("m_heightOfCOGAboveGround", ctypes.c_float),
        ("m_localVelocityX", ctypes.c_float),
        ("m_localVelocityY", ctypes.c_float),
        ("m_localVelocityZ", ctypes.c_float),
        ("m_angularVelocityX", ctypes.c_float),
        ("m_angularVelocityY", ctypes.c_float),
        ("m_angularVelocityZ", ctypes.c_float),
        ("m_angularAccelerationX", ctypes.c_float),
        ("m_angularAccelerationY", ctypes.c_float),
        ("m_angularAccelerationZ", ctypes.c_float),
        ("m_frontWheelsAngle", ctypes.c_float),
        ("m_wheelVertForce", ctypes.c_float * 4),
        ("m_frontAeroHeight", ctypes.c_float),
        ("m_rearAeroHeight", ctypes.c_float),
        ("m_frontRollAngle", ctypes.c_float),
        ("m_rearRollAngle", ctypes.c_float),
        ("m_chassisYaw", ctypes.c_float),
        ("m_chassisPitch", ctypes.c_float),
        ("m_wheelCamber", ctypes.c_float * 4),
        ("m_wheelCamberGain", ctypes.c_float * 4),
    ]
