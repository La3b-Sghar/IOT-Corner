import RPi.GPIO as GPIO
import time

# Setup for flow rate sensor
FLOW_SENSOR_PIN = 27  # GPIO pin for the sensor
pulse_count = 0  # To count pulses

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Callback function to count pulses
def pulse_callback(channel):
    global pulse_count
    pulse_count += 1

# Attach the callback function to the pin
GPIO.add_event_detect(FLOW_SENSOR_PIN, GPIO.FALLING, callback=pulse_callback)

def read_flow_rate():
    global pulse_count
    pulse_count = 0  # Reset pulse count
    time.sleep(1)  # Wait for 1 second to collect pulses
    flow_rate = pulse_count  # You can adjust this to calculate the flow rate
    return flow_rate

try:
    while True:
        flow_rate = read_flow_rate()
        print(f"Flow Rate (pulses in 1 second): {flow_rate}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()
