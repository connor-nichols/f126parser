from ..constants import PacketID
from .car_damage import PacketCarDamageData
from .car_setups import PacketCarSetupData
from .car_status import PacketCarStatusData
from .car_telemetry import PacketCarTelemetryData
from .car_telemetry2 import PacketCarTelemetry2Data
from .event import PacketEventData
from .final_classification import PacketFinalClassificationData
from .lap_data import PacketLapData
from .lap_positions import PacketLapPositionsData
from .lobby_info import PacketLobbyInfoData
from .motion import PacketMotionData
from .motion_ex import PacketMotionExData
from .participants import PacketParticipantsData
from .session import PacketSessionData
from .session_history import PacketSessionHistoryData
from .time_trial import PacketTimeTrialData
from .tyre_sets import PacketTyreSetsData

# Single source of truth mapping each PacketID to its top-level struct.
# To support a new packet type: add a module above with its ctypes Structure(s),
# then register it here.
PACKET_REGISTRY = {
    PacketID.MOTION: PacketMotionData,
    PacketID.SESSION: PacketSessionData,
    PacketID.LAP_DATA: PacketLapData,
    PacketID.EVENT: PacketEventData,
    PacketID.PARTICIPANTS: PacketParticipantsData,
    PacketID.CAR_SETUPS: PacketCarSetupData,
    PacketID.CAR_TELEMETRY: PacketCarTelemetryData,
    PacketID.CAR_STATUS: PacketCarStatusData,
    PacketID.FINAL_CLASSIFICATION: PacketFinalClassificationData,
    PacketID.LOBBY_INFO: PacketLobbyInfoData,
    PacketID.CAR_DAMAGE: PacketCarDamageData,
    PacketID.SESSION_HISTORY: PacketSessionHistoryData,
    PacketID.TYRE_SETS: PacketTyreSetsData,
    PacketID.MOTION_EX: PacketMotionExData,
    PacketID.TIME_TRIAL: PacketTimeTrialData,
    PacketID.LAP_POSITIONS: PacketLapPositionsData,
    PacketID.CAR_TELEMETRY_2: PacketCarTelemetry2Data,
}
