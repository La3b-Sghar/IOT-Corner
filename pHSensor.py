import RPi.GPIO as GPIO
import spidev  # To communicate with the MCP3008
import time

# Setup for pH sensor using MCP3008 ADC
PH_SENSOR_CHANNEL = 0  # MCP3008 channel for the pH sensor
SPI_BUS = 0  # SPI bus 0 (CS0)
SPI_DEVICE = 0  # SPI device 0 (CS0)

# Setup SPI interface
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 1350000

def read_adc(channel):
    """Read data from the MCP3008 ADC"""
    if channel < 0 or channel > 7:
        return -1  # Invalid channel
    adc_data = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc_data[1] & 3) << 8) + adc_data[2]

def read_ph_sensor():
    """Read the pH sensor value (analog)"""
    adc_value = read_adc(PH_SENSOR_CHANNEL)
    # Assuming the ADC value ranges from 0 to 1023 and maps to pH levels 0 to 14
    ph_value = (adc_value / 1023) * 14  # You can calibrate this as needed
    return ph_value

try:
    while True:
        ph_value = read_ph_sensor()
        print(f"pH Value: {ph_value:.2f}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    spi.close()
    GPIO.cleanup()
