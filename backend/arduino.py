import serial
import time
from .config import get_arduino_config


def send_tea_command(command: str):
    print("--- Sending command to Arduino ---")
    print(command)
    #    arduino_config = get_arduino_config()
    #    port = arduino_config['port']
    #    baud_rate = arduino_config['baud_rate']
    #
    #    try:
    #        ser = serial.Serial(port, baud_rate, timeout=1)
    #        time.sleep(2)  # Wait for the connection to establish
    #        ser.write(command.encode())
    #        ser.close()
    #        print(f"Sent command to Arduino: {command}")
    #    except serial.SerialException as e:
    #        print(f"Error sending command to Arduino: {e}")
