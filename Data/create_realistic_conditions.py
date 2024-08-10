import random
import csv

# Define crop types for different regions
crops_by_region = {
    "Punjab": ["Wheat", "Gram", "Cotton"],
    "Karnataka": ["Soybean", "Jowar", "Sugarcane"],
    "West Bengal": ["Rice", "Maize", "Mustard"],
    "Haryana": ["Wheat", "Gram", "Bajra"],
    "Rajasthan": ["Bajra", "Barley", "Turmeric"],
    "Maharashtra": ["Grapes", "Cotton", "Sugarcane"],
    "Tamil Nadu": ["Cotton", "Groundnut", "Tea"],
    "Andhra Pradesh": ["Groundnut", "Mango", "Paddy"],
    "Uttar Pradesh": ["Mustard", "Maize", "Sugarcane"],
    "Gujarat": ["Tobacco", "Cotton", "Groundnut"],
    "Madhya Pradesh": ["Jowar", "Soybean", "Wheat"],
    "Kerala": ["Rubber", "Coconut", "Tea"],
    "Bihar": ["Maize", "Wheat", "Pulses"],
    "Odisha": ["Sugarcane", "Rice", "Pulses"],
    "Chhattisgarh": ["Turmeric", "Rice", "Maize"],
    "Jharkhand": ["Forest", "Rice", "Pulses"],
    "Assam": ["Tea", "Rice", "Sugarcane"],
    "Telangana": ["Mango", "Cotton", "Paddy"],
    "Arunachal Pradesh": ["Rice", "Tea", "Oilseeds"],
    "Sikkim": ["Cardamom", "Ginger", "Barley"],
    "Mizoram": ["Bamboo", "Rice", "Pulses"],
    "Nagaland": ["Ginger", "Rice", "Oilseeds"],
    "Meghalaya": ["Apple", "Potato", "Rice"],
    "Manipur": ["Pineapple", "Rice", "Pulses"],
    "Tripura": ["Rubber", "Rice", "Pulses"]
}

# Define temperature ranges for different seasons
temp_ranges = {
    "Summer": (25, 35),
    "Autumn": (20, 30),
    "Winter": (12, 25),
    "Spring": (28, 42),
    "Monsoon": (22, 32)
}

# Define states in India
states = [
    "Punjab", "Karnataka", "West Bengal", "Haryana", "Rajasthan",
    "Maharashtra", "Tamil Nadu", "Andhra Pradesh", "Uttar Pradesh", "Gujarat",
    "Madhya Pradesh", "Kerala", "Bihar", "Odisha", "Chhattisgarh", "Jharkhand",
    "Assam", "Telangana", "Arunachal Pradesh", "Sikkim", "Mizoram", "Nagaland",
    "Meghalaya", "Manipur", "Tripura"
]

# Generate random data
data = []
with open('realistic_relational_generated_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Soil Moisture", "Temperature", "Location", "Previous Yield", "Weather", "Season", "Previous Harvested Crop"])
    for i in range(1000):
        state = random.choice(states)
        location = (state)  
        season = random.choice(list(temp_ranges.keys()))
        temp_range = temp_ranges[season]
        temperature = random.randint(temp_range[0], temp_range[1])

        # Select random crop based on region
        crops = crops_by_region.get(state, [])
        previous_crop = None
        if crops:
            previous_crop = random.choice(crops)

        # Generate soil moisture with some null values
        soil_moisture = random.randint(40, 80) if random.random() > 0.2 else None

        # Generate previous yield with some null values
        previous_yield = random.randint(30, 70) if random.random() > 0.1 else None

        weather = random.choice(["Sunny", "Rainy", "Cloudy", "Stormy"])

        writer.writerow([soil_moisture, temperature, location, previous_yield, weather, season, previous_crop])

# # Print the data as CSV
# print("Soil Moisture,Temperature,Location,Previous Yield,Weather,Season,Previous Harvested Crop")
# for row in data:
#     print(",".join([str(x) for x in row]))