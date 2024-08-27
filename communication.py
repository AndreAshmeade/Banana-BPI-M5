import RPi.GPIO as GPIO
import time

# Pin map based on the provided from pin_map.py
pin_map = {
    "CON1-P01": {"Type": "Power"},
    "CON1-P02": {"Type": "Power"},
    "CON1-P03": {"Type": "Digital I/O, I2C SDA"},
    "CON1-P04": {"Type": "Power"},
    "CON1-P05": {"Type": "Digital I/O, I2C SCL"},
    "CON1-P06": {"Type": "Ground"},
    "CON1-P07": {"Type": "Digital I/O, SDIO CMD"},
    "CON1-P08": {"Type": "Digital I/O, UART TX"},
    "CON1-P09": {"Type": "Ground"},
    "CON1-P10": {"Type": "Digital I/O, UART RX"},
    "CON1-P11": {"Type": "Digital I/O, SDIO D3"},
    "CON1-P12": {"Type": "Digital I/O, TDMB SCLK"},
    "CON1-P13": {"Type": "Digital I/O, SDIO CLK"},
    "CON1-P14": {"Type": "Ground"},
    "CON1-P15": {"Type": "Digital I/O, PWM F"},
    "CON1-P16": {"Type": "Digital I/O, SDIO D0"},
    "CON1-P17": {"Type": "Power"},
    "CON1-P18": {"Type": "Digital I/O, SDIO D1"},
    "CON1-P19": {"Type": "Digital I/O, PCM DIN"},
    "CON1-P20": {"Type": "Ground"},
    "CON1-P21": {"Type": "Digital I/O, PCM DOUT"},
    "CON1-P22": {"Type": "Digital I/O, SDIO D2"},
    "CON1-P23": {"Type": "Digital I/O, PCM CLK"},
    "CON1-P24": {"Type": "Digital I/O, PCM SYNC"},
    "CON1-P25": {"Type": "Ground"},
    "CON1-P26": {"Type": "Digital I/O, PWM E"},
    "CON1-P27": {"Type": "Digital I/O, I2C M3 SDA"},
    "CON1-P28": {"Type": "Digital I/O, I2C M3 SCL"},
    "CON1-P29": {"Type": "Digital I/O, UART CTS"},
    "CON1-P30": {"Type": "Ground"},
    "CON1-P31": {"Type": "Digital I/O, UART RTS"},
    "CON1-P32": {"Type": "Digital I/O, PWM B"},
    "CON1-P33": {"Type": "Digital I/O, PWM A"},
    "CON1-P34": {"Type": "Ground"},
    "CON1-P35": {"Type": "Digital I/O, TDMB FS"},
    "CON1-P36": {"Type": "Digital I/O, SPDIF IN"},
    "CON1-P37": {"Type": "Digital I/O, I2S MCLK"},
    "CON1-P38": {"Type": "Digital I/O, TDMB DIN"},
    "CON1-P39": {"Type": "Ground"},
    "CON1-P40": {"Type": "Digital I/O, TDMB DOUT"},
    "CON2-P1": {"Type": "Ground"},
    "CON2-P2": {"Type": "Digital I/O, UART RX"},
    "CON2-P3": {"Type": "Digital I/O, UART TX"},
}

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up pin configurations
def setup_pins():
    for pin in pin_map:
        pin_type = pin_map[pin]["Type"]
        if "Digital I/O" in pin_type:
            GPIO.setup(pin, GPIO.OUT)
        # Add more configurations based on pin capabilities if necessary

# Function to perform a digital write operation
def digital_write(pin, value):
    GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)

# Function to perform a digital read operation
def digital_read(pin):
    return GPIO.input(pin)

# Function to set up PWM
def setup_pwm(pin, frequency=1000):
    pwm = GPIO.PWM(pin, frequency)
    pwm.start(0)
    return pwm

# Function to cleanup GPIO
def cleanup():
    GPIO.cleanup()

# Example usage
def main():
    setup_pins()

    try:
        # Digital write example
        pin = "CON1-P07"  # Example pin for digital write
        print(f"Setting {pin} HIGH")
        digital_write(pin, True)
        time.sleep(2)
        print(f"Setting {pin} LOW")
        digital_write(pin, False)

        # PWM example
        pwm_pin = "CON1-P15"  # Example pin for PWM
        pwm = setup_pwm(pwm_pin, 1000)
        for duty_cycle in range(0, 101, 10):
            print(f"Setting PWM duty cycle to {duty_cycle}%")
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program interrupted")

    finally:
        cleanup()

if __name__ == "__main__":
    main()

