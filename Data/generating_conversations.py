import os
import random
import json
import csv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import pandas as pd

# I have hidden the api key below
genai.configure(api_key="API_KEY")

# The model configurations
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1024,  
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# Initialize the files to store the data
def initialize_files(csv_file, json_file):
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Prompt", "Response", "Soil Moisture", "Temperature", "Location", "Previous Yield", "Weather", "Season"])
    
    if not os.path.exists(json_file):
        with open(json_file, mode='w', encoding='utf-8') as file:
            json.dump([], file)

# Masking the data prompt as required and needed.
def mask_question(prompt):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text.strip()

# Saving the conversations to the csv and json file
def save_conversation(prompt, response, conversation_data, csv_file, json_file):
    if response is None:  
        return
    
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([prompt, response] + list(conversation_data.values()))

    with open(json_file, mode='r+', encoding='utf-8') as file:
        data = json.load(file)
        data.append({
            "Prompt": prompt,
            "Response": response,
            **conversation_data
        })
        file.seek(0)
        json.dump(data, file, indent=4)
        

# Function to import and return conversation data from the CSV file
def get_conversation_data(df, index):
    row = df.iloc[index]
    return {
        "Soil Moisture": int(row['Soil Moisture']) if pd.notnull(row['Soil Moisture']) else None,
        "Temperature": int(row['Temperature']) if pd.notnull(row['Temperature']) else None,
        "Location": row['Location'],
        "Previous Yield": row['Previous Yield'],
        "Weather": row['Weather'],
        "Season": row['Season'],
        "Previous Harvested Crop": row['Previous Harvested Crop']
    }

    
# main function to run all the commands and a loop 
def main():
    csv_file = 'concise_conversation_data.csv'
    json_file = 'concise_conversation_data.json'
    
    initialize_files(csv_file, json_file)
    
    df = pd.read_csv('realistic_relational_generated_data.csv')
    
    query_list = [
        "What crops should I plant based on current soil moisture and temperature?",
        "How will the weather affect my crops?",
        "What's the best time to plant mustard?",
        "Given the current season and soil moisture, what should I grow?",
        "Can I plant wheat after rice in this season?",
        "How will the temperature affect my yield?",
        "Is the current weather suitable for corn planting?",
        "Should I worry about the soil moisture for planting this season?",
        "What are the best crops for this location?",
        "What effect will the current weather have on wheat yield?",
        "What crops should I plant based on current soil moisture of 65%, and temperature of 32°C?",
        "Given the current season of summer and soil moisture of 40%, what should I grow?",
        "What are the best crops for this location with sandy loam soil and average rainfall of 800mm?",
        "Can I plant wheat after rice in the autumn season?",
        "What is the best time to plant maize in a region with a frost-free period of 150 days?",
        "How much seed should I use for soybean per acre on clay soil?",
        "What are the nutrient requirements for tomato in a greenhouse environment?",
        "Can you suggest a crop rotation plan for a field with a history of corn and soybean cultivation?",
        "What are the most profitable crops for a region with high water availability?",
        "How can I improve my soil fertility, which is currently low in organic matter?",
        "What kind of fertilizer should I use for a wheat crop on acidic soil?",
        "How much water does a cotton crop require in a semi-arid climate?",
        "How can I prevent soil erosion on a sloping field?",
        "What are the signs of nitrogen deficiency in rice plants?",
        "How will a sudden drop in temperature affect my tomato crop?",
        "How will the temperature of 38°C affect my wheat yield?",
        "Is the current weather with cloudy skies and 25°C suitable for planting corn?",
        "Should I worry about the soil moisture of 30%, for planting sugarcane this season?",
        "What is the long-term weather forecast for a region prone to droughts?",
        "How will climate change with increased rainfall affect apple cultivation?",
        "What can I do to protect my grape vines from frost?"
    ]
    
    # Define the number of conversations you want to create, set 300 here
    for i in range(300):  
        prompt = random.choice(query_list)

        response = mask_question(prompt)
        
        conversation_data = get_conversation_data(df, i % len(df))
        
        save_conversation(prompt, response, conversation_data, csv_file, json_file)
        
        prompt = ""
        response = ""
        conversation_data = {}

    print("Generated 2,000 concise conversations successfully.")

if __name__ == "__main__":
    main()
