import requests
import time
import RPi.GPIO as GPIO
import board
from digitalio import DigitalInOut
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

lcd_columns = 16
lcd_rows = 2

lcd_rs = DigitalInOut(board.D25)
lcd_en = DigitalInOut(board.D24)
lcd_d4 = DigitalInOut(board.D23)
lcd_d5 = DigitalInOut(board.D17)
lcd_d6 = DigitalInOut(board.D27)
lcd_d7 = DigitalInOut(board.D22)

# Initialise the LCD class
lcd = Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

def call_api(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Assuming the response is JSON
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def main():
    try:
        while True:
            endpoint = "https://server.duinocoin.com/users/nanomachine"  # Replace this with your actual endpoint
            data = call_api(endpoint)
            if data:
                # Display balance without decimal
                balance = data['result']['balance']['balance']
                balance_str = "Balance:" + str(int(balance))
                print(balance_str)

                # Sum all miners' hashrate
                miners_hashrate_sum = int(sum(miner['hashrate'] for miner in data['result']['miners']) / 1000)
                hashrate_str = "Hashrate:" + str(miners_hashrate_sum) + "kH/s"
                print(hashrate_str)

                lcd.message = balance_str + "\n" + hashrate_str

            time.sleep(30)

    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()


if __name__ == "__main__":
    main()
