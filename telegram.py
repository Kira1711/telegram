import requests
import RPi.GPIO as GPIO
TOKEN = "7823417489:AAHRKVbATMBKE7LOb4_cZ4z29_60uxRSQ3o"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.OUT)  

def send_message(chat_id, text):
    requests.get(BASE_URL + "sendMessage", params={"chat_id": chat_id, "text": text})

def handle_commands():
    offset = None
    while True:
        updates = requests.get(BASE_URL + "getUpdates", params={"offset": offset, "timeout": 60}).json()

        for update in updates.get("result", []):
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"].get("text", "").lower()

            
            if message_text == "/ledon":
                GPIO.output(27, GPIO.HIGH)
                send_message(chat_id, "LED ON")
            elif message_text == "/ledoff":
                GPIO.output(27, GPIO.LOW)
                send_message(chat_id, "LED OFF")

            
            offset = update["update_id"] + 1

if __name__ == "__main__":
    try:
        handle_commands()
    except KeyboardInterrupt:
        GPIO.cleanup()  

