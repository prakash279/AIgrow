import requests
import time

# Define your bot token and API URL
TOKEN = "Token_for_bot"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# Function to get updates from the bot
def get_updates(offset=None):
    url = URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message
def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=data)
    return response.json()

# Define a simple function to handle responses, this is dummy chatbot for now we will integrate fine tuned microsofts phi-2 language model with this so it can responsd better.
def handle_message(message):
    if "hello" in message.lower():
        return "Hi there! How can I help you today?"
    elif "weather" in message.lower():
        return "Please provide your location for weather updates."
    elif "bye" in message.lower():
        return "Goodbye! Have a great day!"
    else:
        return "I'm not sure how to respond to that."

# Main function to handle updates and respond
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"]["text"]

            bot_response = handle_message(message_text)
            send_message(chat_id, bot_response)

            # Update the offset to avoid processing the same message again
            offset = update["update_id"] + 1

        # Sleep for a short while to avoid hitting API rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
