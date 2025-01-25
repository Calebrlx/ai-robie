import serial
import time

# List of likely serial ports to check
ports_to_check = [
    "/dev/ttyUSB0",  # Common for USB serial
    "/dev/ttyUSB1",
    "/dev/ttyACM0",  # Common for Arduino-based boards
    "/dev/ttyACM1",
    "/dev/ttyS0",    # Onboard serial
    "/dev/ttyS1",
    "/dev/ttyS2",
    "/dev/ttyS3"
]

# Baud rate for Marlin boards (default is 115200 or 250000)
baud_rate = 115200

# G-code command to send
gcode_command = "M119"  # Endstop status

def try_port(port):
    try:
        print(f"Trying port: {port}")
        with serial.Serial(port, baud_rate, timeout=2) as ser:
            # Send the G-code command
            ser.write((gcode_command + "\n").encode())
            print(f"Sent: {gcode_command}")
            
            # Wait for a response
            time.sleep(2)
            response = ser.read(ser.in_waiting or 1).decode().strip()
            
            if response:
                print(f"Response from {port}: {response}")
                return True
            else:
                print(f"No response from {port}")
    except Exception as e:
        print(f"Error on port {port}: {e}")
    return False

def main():
    for port in ports_to_check:
        if try_port(port):
            print(f"Connection successful on {port}!")
            break
        time.sleep(5)  # Wait 5 seconds between attempts
    else:
        print("Could not find a working port.")

if __name__ == "__main__":
    main()