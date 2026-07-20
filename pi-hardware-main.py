
"""Example usage of the f126_telemetry package.

Run this while F1 25 (2026 Season Pack) is sending UDP telemetry to this
machine (Settings > Telemetry Settings > UDP Telemetry: On, port 20777,
format 2026) to see live data printed.

This file also doubles as the reference for extending the receiver:
  - To handle a packet type that isn't wired up yet, add another
    `@listener.on(PacketID.X)`-decorated function below.
  - To add support for a packet type this package doesn't parse yet
    (e.g. a brand new one added in a future patch), write a ctypes
    Structure for it under f126_telemetry/packets/ and register it in
    f126_telemetry/packets/__init__.py's PACKET_REGISTRY - nothing else
    needs to change.
"""

from f126_telemetry import PacketID, TelemetryListener
from f126_telemetry.packets.event import describe_event
from gpiozero import LED
import os
listener = TelemetryListener(port=20777)

class AvailableHardware():
    def __init__(self):
        self.s_mode_available = LED(17)

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

buzzer = TonalBuzzer(18)

# Bb major scale (one octave, starting at Bb4)
notes = ["A#4", "C5", "D5", "D#5", "F5", "G5", "A5"]

for note in notes:
    buzzer.play(Tone(note))
    print(f"Playing {note}")
    sleep(0.5)

buzzer.stop()

hardware = AvailableHardware()


#shift=0b10000 00000 00000
# @listener.on(PacketID.CAR_TELEMETRY)
# def on_car_telemetry(packet, addr):
#     car = packet.m_carTelemetryData[packet.m_header.m_playerCarIndex]
#     os.system('cls' if os.name == 'nt' else 'clear')
#     formatted_shift = str(bin(car.m_revLightsBitValue))[2:]
#     formatted_shift = formatted_shift[::-1]
#     formatted_shift = formatted_shift.replace("0", " ").replace("1", "*")
#     print(
#         f"[Telemetry] speed={car.m_speed:>3} km/h  gear={car.m_gear:>2}  "
#         f"rpm={car.m_engineRPM:>5}  throttle={car.m_throttle:.2f}  brake={car.m_brake:.2f}  shift={formatted_shift}"
#     )

@listener.on(PacketID.CAR_TELEMETRY_2)
def on_car_telemetry2(packet, addr):
    car = packet.m_carTelemetry2Data[packet.m_header.m_playerCarIndex]
    #os.system('cls' if os.name == 'nt' else 'clear')
    print(
        f"S Mode Available: {car.m_activeAeroAvailable}     S Mode Active: {car.m_activeAeroMode}"
    )
    if car.m_activeAeroAvailable == 1:
        hardware.s_mode_available.on()
    else:
        hardware.s_mode_available.off()


# @listener.on(PacketID.LAP_DATA)
# def on_lap_data(packet, addr):
#     lap = packet.m_lapData[packet.m_header.m_playerCarIndex]
#     #print(f"[Lap] lap={lap.m_currentLapNum}  position={lap.m_carPosition}")
#
#
# @listener.on(PacketID.EVENT)
# def on_event(packet, addr):
#     event = describe_event(packet)
#     if event:
#         print(f"[Event] {event['label']}: {event['details']}")


if __name__ == "__main__":
    listener.run()
