import time
import Adafruit_DHT
import requests
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# Sensor setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin for DHT22 sensor
PH_SENSOR_PIN = 17  # GPIO pin for pH sensor (example pin)
FLOW_SENSOR_PIN = 27  # GPIO pin for flow rate sensor (example pin)
MQTT_BROKER = "mqtt.eclipse.org"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/sensors"

# Initialize MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PH_SENSOR_PIN, GPIO.IN)
GPIO.setup(FLOW_SENSOR_PIN, GPIO.IN)

def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print("Failed to retrieve data from DHT sensor")
        return None, None

def read_ph_sensor():
    # Placeholder: Assume you have code to read from pH sensor
    ph_value = GPIO.input(PH_SENSOR_PIN)  # Replace with actual sensor reading
    return ph_value

def read_flow_sensor():
    # Placeholder: Assume you have code to calculate flow rate
    flow_rate = GPIO.input(FLOW_SENSOR_PIN)  # Replace with actual sensor reading
    return flow_rate

def send_data_to_api(temperature, humidity, ph_value, flow_rate):
    data = {
        "temperature": temperature,
        "humidity": humidity,
        "ph_value": ph_value,
        "flow_rate": flow_rate
    }
    try:
        response = requests.post("http://your-api-endpoint.com/sensor-data", json=data)
        print("Data sent to API:", response.status_code)
    except Exception as e:
        print("Error sending data to API:", e)

def send_data_to_mqtt(temperature, humidity, ph_value, flow_rate):
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "ph_value": ph_value,
        "flow_rate": flow_rate
    }
    client.publish(MQTT_TOPIC, str(payload))
    print("Data sent to MQTT Broker:", payload)

def main():
    while True:
        # Read sensors
        temperature, humidity = read_dht22()
        ph_value = read_ph_sensor()
        flow_rate = read_flow_sensor()

        if temperature is not None and humidity is not None:
            # Send data to API or MQTT
            send_data_to_api(temperature, humidity, ph_value, flow_rate)
            send_data_to_mqtt(temperature, humidity, ph_value, flow_rate)

        # Wait before collecting the next data point
        time.sleep(60)  # Collect every 60 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        GPIO.cleanup()  # Cleanup GPIO on exit
