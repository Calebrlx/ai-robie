import serial
import time

# Serial setup for Marlin board
SERIAL_PORT = "/dev/ttyUSB0"  # Replace with the correct port
BAUD_RATE = 115200

# Initialize serial connection
def init_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)  # Allow time for the connection to establish
        print("Connected to Marlin board")
        return ser
    except Exception as e:
        print(f"Failed to connect to Marlin board: {e}")
        return None

# Send G-code command to Marlin board
def send_gcode(ser, gcode):
    if ser:
        ser.write((gcode + "\n").encode())
        print(f"Sent: {gcode}")
        time.sleep(0.1)  # Delay to ensure Marlin processes the command
    else:
        print("Serial connection not established")

# Map Vim motions to G-code commands
def motion_to_gcode(motion):
    commands = {
        "h": "G91\nG1 X-1 F1000",  # Move left
        "l": "G91\nG1 X1 F1000",   # Move right
        "j": "G91\nG1 Y-1 F1000",  # Move down
        "k": "G91\nG1 Y1 F1000",   # Move up
    }
    return commands.get(motion, None)

# Main function for reading Vim motions and controlling motors
def main():
    ser = init_serial()
    if not ser:
        return
    
    print("Enter Vim motions (h, j, k, l) to control motors. Type 'q' to quit.")
    while True:
        motion = input("Motion: ").strip()  # Read input
        if motion == "q":
            print("Exiting...")
            break
        gcode = motion_to_gcode(motion)
        if gcode:
            send_gcode(ser, gcode)
        else:
            print("Invalid motion. Use h, j, k, l.")

    if ser:
        ser.close()

if __name__ == "__main__":
    main()