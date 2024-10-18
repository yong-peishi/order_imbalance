import imbalance_calc as imbalance
import requests

bot_token = '7365113257:AAHp4mWkKaBCs_YtrHhIHvcmK4Leek4uhw0'
chat_id = '-4577599177'

def run_app(alert_level):
    with open('tickers.csv', 'r') as file:
        tickers = [line.strip() for line in file.readlines()[1:-1]]
    
    message = ['Order Book Imbalance:']
    for ticker in tickers:
        result = imbalance.depth_info(ticker, minimum = 2)
        if result is not None and len(result) != 0:
            if result[1] >= alert_level:
                string = (f'🚨 <b>{ticker}</b> ' + str(result[0]) + ' ' + str(result[1]))
            else:
                string = (f'⚠️ <b>{ticker}</b> ' + str(result[0]) + ' ' + str(result[1]))
            message.append(string)
    return message
    
message_list = run_app(alert_level = 5)
message = "\n".join(message_list)

# Telegram API URL to send a message
url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

params = {
    "chat_id": chat_id,
    "text": message,
    "parse_mode": "HTML"
}

# Send the message via a POST request
response = requests.post(url, data=params)

# Check if the message was sent successfully
if response.status_code == 200:
    print("Message sent successfully!")
else:
    print(f"Failed to send message. Error: {response.status_code}")