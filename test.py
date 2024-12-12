import RPi.GPIO as GPIO
import time
import random

# Set the GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin connected to the LED as an output
# GPIO_LED = 4  # Replace with your GPIO pin number
# GPIO.setup(GPIO_LED, GPIO.OUT)

leds = [4,18,17,23]

for led in leds:
    GPIO.setup(led, GPIO.OUT)


try:
    while True:
        # Randomly decide how many LEDs to turn on (1 to 4)
        num_leds = random.randint(1, 4)
        # Randomly select LEDs without repetition
        selected_leds = random.sample(leds, num_leds)
        
        # Turn on the selected LEDs
        for led in selected_leds:
            GPIO.output(led, GPIO.HIGH)
        print(f"LEDs {selected_leds} ON")
        time.sleep(0.2)

        # Turn off the selected LEDs
        for led in selected_leds:
            GPIO.output(led, GPIO.LOW)
        print(f"LEDs {selected_leds} OFF")
        time.sleep(0.2)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    GPIO.cleanup()
