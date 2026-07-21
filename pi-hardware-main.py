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
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import os
import threading

# Simple test for NeoPixels on Raspberry Pi
import time

import board

import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 16

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGBW

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in {neopixel.RGB, neopixel.GRB} else (r, g, b, 0)

pixels[0] = (0, 255, 0, 0)

listener = TelemetryListener(port=20777)

DEFAULT_NOTE_DURATION = 0.15

# Named tone sequences for different telemetry events. Each entry is a list of
# notes played in order; a note is either "C5" (plays for DEFAULT_NOTE_DURATION)
# or ("C5", 0.3) to give it its own duration. Add a new key here, then trigger
# it from any handler with hardware.play("your_key").
TONES = {
    "s_mode_available": ["C5"],
    "s_mode_active": ["G5"],
}


class AvailableHardware():
    def __init__(self, tones=TONES):
        self.s_mode_available = LED(17)
        self.buzzer = TonalBuzzer(18)
        self.tones = tones
        self._tone_lock = threading.Lock()

    def _play_sequence(self, notes):
        try:
            for note in notes:
                name, duration = note if isinstance(note, tuple) else (note, DEFAULT_NOTE_DURATION)
                self.buzzer.play(Tone(name))
                sleep(duration)
            self.buzzer.stop()
        finally:
            self._tone_lock.release()

    def play(self, event):
        # Non-blocking: runs the tone sequence on a background thread so the
        # UDP receive loop never waits on it. No-ops if `event` isn't in
        # self.tones, or if a tone is already playing.
        notes = self.tones.get(event)
        if not notes:
            return
        if self._tone_lock.acquire(blocking=False):
            threading.Thread(target=self._play_sequence, args=(notes,), daemon=True).start()



hardware = AvailableHardware()
_prev_s_mode_available = 0


# shift=0b10000 00000 00000
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
    global _prev_s_mode_available
    car = packet.m_carTelemetry2Data[packet.m_header.m_playerCarIndex]
    # os.system('cls' if os.name == 'nt' else 'clear')
    print(
        f"S Mode Available: {car.m_activeAeroAvailable}     S Mode Active: {car.m_activeAeroMode}"
    )
    if car.m_activeAeroAvailable == 1:
        hardware.s_mode_available.on()
        if _prev_s_mode_available == 0:
            hardware.play("s_mode_available")
    else:
        hardware.s_mode_available.off()

    if car.m_activeAeroMode == 1:
        if _prev_s_mode_available == 1:
            hardware.play("s_mode_available")
    _prev_s_mode_available = car.m_activeAeroAvailable


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
