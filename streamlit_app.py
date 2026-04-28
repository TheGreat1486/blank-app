import streamlit as st
import json
import os

# Database configuration
DB_FILE = "plant_progress.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# Keywords dictionary and their growth impact
# Positive: +10%, Neutral: +5%, Negative: 0%
KEYWORDS = {
    "happy": 10, "great": 10, "excited": 10, "good": 10, "awesome": 10,
    "tired": 5, "okay": 5, "normal": 5, "fine": 4,
    "sad": 0, "bad": 0, "angry": 0, "depressed": 0, "terrible": 0
}

st.title("🌱 CutePlantPal")

# 1. User Identification
user_name = st.text_input("Enter your name to load your plant:").lower().strip()

if user_name:
    data = load_data()
    
    # Initialize user if not found
    if user_name not in data:
        data[user_name] = 0
        save_data(data)
    
    current_growth = data[user_name]

    # 2. Daily Report Input
    st.subheader(f"Hello {user_name.capitalize()}, how are you feeling today?")
    report = st.text_area("Write your daily report here:").lower()
    
    if st.button("Submit Report"):
        growth_points = 0
        found_keywords = False
        
        # Search for keywords in the text
        for word, points in KEYWORDS.items():
            if word in report:
                growth_points = points
                found_keywords = True
                break # Take the first match
        
        if found_keywords:
            # Update growth (max 100%)
            current_growth = min(current_growth + growth_points, 100)
            data[user_name] = current_growth
            save_data(data)
            
            if growth_points > 0:
                st.success(f"Your plant grew by {growth_points}%!")
            else:
                st.warning("Your plant didn't grow today. Take heart, tomorrow is a new day! ❤️")
        else:
            st.info("No keywords detected, but thank you for sharing your thoughts.")

    # 3. Visualizing the Plant
    st.divider()
    st.write(f"### Plant Growth: {current_growth}%")
    
    # Progress bar and visual stages
    st.progress(current_growth / 100)
    
    if current_growth == 0:
        st.subheader("🌱 (Just a seed)")
    elif current_growth < 40:
        st.subheader("🌿 (It's sprouting)")
    elif current_growth < 80:
        st.subheader("🪴 (Getting stronger)")
    else:
        st.subheader("🌳 (A beautiful full-grown tree!)")
else:
    st.info("Please enter your name to get started.")
