"""
Kishan Kavach - Crop Intelligence Database
100+ crops with complete profiles
"""

CROP_DATABASE = {
    # ===== VEGETABLES =====
    "tomato": {
        "name": "Tomato", "temp_min": 10, "temp_max": 21, "humidity_min": 85, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "potato": {
        "name": "Potato", "temp_min": 4, "temp_max": 10, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 120, "category": "vegetable"
    },
    "onion": {
        "name": "Onion", "temp_min": 0, "temp_max": 5, "humidity_min": 65, "humidity_max": 70,
        "harmful_gas": "Ethylene", "shelf_life": 180, "category": "vegetable"
    },
    "carrot": {
        "name": "Carrot", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 120, "category": "vegetable"
    },
    "cabbage": {
        "name": "Cabbage", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 90, "category": "vegetable"
    },
    "cauliflower": {
        "name": "Cauliflower", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 98,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "spinach": {
        "name": "Spinach", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "brinjal": {
        "name": "Brinjal/Eggplant", "temp_min": 10, "temp_max": 12, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "capsicum": {
        "name": "Capsicum/Bell Pepper", "temp_min": 7, "temp_max": 13, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "cucumber": {
        "name": "Cucumber", "temp_min": 10, "temp_max": 13, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "peas": {
        "name": "Green Peas", "temp_min": 0, "temp_max": 2, "humidity_min": 90, "humidity_max": 98,
        "harmful_gas": "CO2", "shelf_life": 14, "category": "vegetable"
    },
    "beans": {
        "name": "Green Beans", "temp_min": 4, "temp_max": 7, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 10, "category": "vegetable"
    },
    "okra": {
        "name": "Okra/Lady Finger", "temp_min": 7, "temp_max": 10, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 10, "category": "vegetable"
    },
    "radish": {
        "name": "Radish", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "CO2", "shelf_life": 30, "category": "vegetable"
    },
    "turnip": {
        "name": "Turnip", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 120, "category": "vegetable"
    },
    "beetroot": {
        "name": "Beetroot", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "CO2", "shelf_life": 120, "category": "vegetable"
    },
    "bitter_gourd": {
        "name": "Bitter Gourd", "temp_min": 10, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "bottle_gourd": {
        "name": "Bottle Gourd", "temp_min": 10, "temp_max": 15, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "ridge_gourd": {
        "name": "Ridge Gourd", "temp_min": 10, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 10, "category": "vegetable"
    },
    "pumpkin": {
        "name": "Pumpkin", "temp_min": 10, "temp_max": 15, "humidity_min": 50, "humidity_max": 70,
        "harmful_gas": "Ethylene", "shelf_life": 90, "category": "vegetable"
    },
    "sweet_potato": {
        "name": "Sweet Potato", "temp_min": 13, "temp_max": 16, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "CO2", "shelf_life": 120, "category": "vegetable"
    },
    "garlic": {
        "name": "Garlic", "temp_min": 0, "temp_max": 4, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 180, "category": "vegetable"
    },
    "ginger": {
        "name": "Ginger", "temp_min": 12, "temp_max": 14, "humidity_min": 65, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 150, "category": "vegetable"
    },
    "mushroom": {
        "name": "Mushroom", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 7, "category": "vegetable"
    },
    "lettuce": {
        "name": "Lettuce", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "broccoli": {
        "name": "Broccoli", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "celery": {
        "name": "Celery", "temp_min": 0, "temp_max": 4, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "asparagus": {
        "name": "Asparagus", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "vegetable"
    },
    "corn": {
        "name": "Sweet Corn", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 98,
        "harmful_gas": "CO2", "shelf_life": 7, "category": "vegetable"
    },
    "zucchini": {
        "name": "Zucchini", "temp_min": 5, "temp_max": 10, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "artichoke": {
        "name": "Artichoke", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "CO2", "shelf_life": 14, "category": "vegetable"
    },
    "leek": {
        "name": "Leek", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 60, "category": "vegetable"
    },
    "parsnip": {
        "name": "Parsnip", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "CO2", "shelf_life": 120, "category": "vegetable"
    },
    "kale": {
        "name": "Kale", "temp_min": 0, "temp_max": 2, "humidity_min": 95, "humidity_max": 100,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "green_chili": {
        "name": "Green Chili", "temp_min": 5, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "CO2", "shelf_life": 21, "category": "vegetable"
    },
    "drumstick": {
        "name": "Drumstick/Moringa", "temp_min": 7, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 12, "category": "vegetable"
    },
    "fenugreek": {
        "name": "Fenugreek Leaves", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ammonia", "shelf_life": 7, "category": "vegetable"
    },
    "coriander": {
        "name": "Coriander/Cilantro", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "mint": {
        "name": "Mint", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },
    "spring_onion": {
        "name": "Spring Onion", "temp_min": 0, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "vegetable"
    },

    # ===== FRUITS =====
    "apple": {
        "name": "Apple", "temp_min": -1, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 120, "category": "fruit"
    },
    "banana": {
        "name": "Banana", "temp_min": 13, "temp_max": 15, "humidity_min": 85, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "fruit"
    },
    "mango": {
        "name": "Mango", "temp_min": 10, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "grape": {
        "name": "Grape", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "SO2", "shelf_life": 56, "category": "fruit"
    },
    "orange": {
        "name": "Orange", "temp_min": 3, "temp_max": 9, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 56, "category": "fruit"
    },
    "watermelon": {
        "name": "Watermelon", "temp_min": 10, "temp_max": 15, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "papaya": {
        "name": "Papaya", "temp_min": 7, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "guava": {
        "name": "Guava", "temp_min": 5, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "pomegranate": {
        "name": "Pomegranate", "temp_min": 5, "temp_max": 7, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "CO2", "shelf_life": 60, "category": "fruit"
    },
    "pineapple": {
        "name": "Pineapple", "temp_min": 7, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 28, "category": "fruit"
    },
    "strawberry": {
        "name": "Strawberry", "temp_min": 0, "temp_max": 2, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "fruit"
    },
    "lemon": {
        "name": "Lemon", "temp_min": 10, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 30, "category": "fruit"
    },
    "coconut": {
        "name": "Coconut", "temp_min": 0, "temp_max": 4, "humidity_min": 75, "humidity_max": 80,
        "harmful_gas": "CO2", "shelf_life": 60, "category": "fruit"
    },
    "litchi": {
        "name": "Litchi/Lychee", "temp_min": 1, "temp_max": 5, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "SO2", "shelf_life": 28, "category": "fruit"
    },
    "jackfruit": {
        "name": "Jackfruit", "temp_min": 11, "temp_max": 13, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 42, "category": "fruit"
    },
    "custard_apple": {
        "name": "Custard Apple", "temp_min": 5, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "fruit"
    },
    "sapodilla": {
        "name": "Sapodilla/Chikoo", "temp_min": 15, "temp_max": 20, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "fig": {
        "name": "Fig", "temp_min": -1, "temp_max": 0, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "fruit"
    },
    "dates": {
        "name": "Dates", "temp_min": 0, "temp_max": 4, "humidity_min": 70, "humidity_max": 75,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "fruit"
    },
    "kiwi": {
        "name": "Kiwi", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 90, "category": "fruit"
    },
    "avocado": {
        "name": "Avocado", "temp_min": 3, "temp_max": 7, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 28, "category": "fruit"
    },
    "peach": {
        "name": "Peach", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 28, "category": "fruit"
    },
    "plum": {
        "name": "Plum", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 35, "category": "fruit"
    },
    "cherry": {
        "name": "Cherry", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 21, "category": "fruit"
    },
    "pear": {
        "name": "Pear", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 90, "category": "fruit"
    },
    "dragon_fruit": {
        "name": "Dragon Fruit", "temp_min": 7, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "passion_fruit": {
        "name": "Passion Fruit", "temp_min": 7, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 30, "category": "fruit"
    },
    "star_fruit": {
        "name": "Star Fruit", "temp_min": 5, "temp_max": 10, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "blueberry": {
        "name": "Blueberry", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 14, "category": "fruit"
    },
    "raspberry": {
        "name": "Raspberry", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 5, "category": "fruit"
    },
    "cranberry": {
        "name": "Cranberry", "temp_min": 2, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "CO2", "shelf_life": 60, "category": "fruit"
    },
    "apricot": {
        "name": "Apricot", "temp_min": -1, "temp_max": 0, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "melon": {
        "name": "Muskmelon", "temp_min": 2, "temp_max": 5, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 21, "category": "fruit"
    },
    "jamun": {
        "name": "Jamun/Java Plum", "temp_min": 2, "temp_max": 5, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "fruit"
    },
    "amla": {
        "name": "Amla/Indian Gooseberry", "temp_min": 4, "temp_max": 8, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "CO2", "shelf_life": 21, "category": "fruit"
    },
    "tamarind": {
        "name": "Tamarind", "temp_min": 18, "temp_max": 22, "humidity_min": 60, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "fruit"
    },

    # ===== GRAINS & CEREALS =====
    "wheat": {
        "name": "Wheat", "temp_min": 10, "temp_max": 20, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "rice": {
        "name": "Rice", "temp_min": 10, "temp_max": 20, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "maize": {
        "name": "Maize/Corn", "temp_min": 5, "temp_max": 15, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 180, "category": "grain"
    },
    "barley": {
        "name": "Barley", "temp_min": 5, "temp_max": 15, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "millet": {
        "name": "Millet", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "sorghum": {
        "name": "Sorghum/Jowar", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "oats": {
        "name": "Oats", "temp_min": 5, "temp_max": 15, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "ragi": {
        "name": "Ragi/Finger Millet", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "bajra": {
        "name": "Bajra/Pearl Millet", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },
    "quinoa": {
        "name": "Quinoa", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "grain"
    },

    # ===== PULSES & LEGUMES =====
    "chickpea": {
        "name": "Chickpea/Chana", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "lentil": {
        "name": "Lentil/Masoor", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "moong": {
        "name": "Moong Dal", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "urad": {
        "name": "Urad Dal", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "toor": {
        "name": "Toor/Arhar Dal", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "kidney_bean": {
        "name": "Kidney Bean/Rajma", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "soybean": {
        "name": "Soybean", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "groundnut": {
        "name": "Groundnut/Peanut", "temp_min": 5, "temp_max": 10, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "Ammonia", "shelf_life": 270, "category": "pulse"
    },
    "black_gram": {
        "name": "Black Gram", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },
    "cowpea": {
        "name": "Cowpea/Lobia", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "pulse"
    },

    # ===== SPICES =====
    "turmeric": {
        "name": "Turmeric", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },
    "cumin": {
        "name": "Cumin/Jeera", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "coriander_seed": {
        "name": "Coriander Seed", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "red_chili": {
        "name": "Red Chili", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "black_pepper": {
        "name": "Black Pepper", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },
    "cardamom": {
        "name": "Cardamom", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "clove": {
        "name": "Clove", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },
    "cinnamon": {
        "name": "Cinnamon", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },
    "mustard": {
        "name": "Mustard Seed", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "fennel": {
        "name": "Fennel/Saunf", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "fenugreek_seed": {
        "name": "Fenugreek Seed", "temp_min": 15, "temp_max": 25, "humidity_min": 50, "humidity_max": 60,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "spice"
    },
    "nutmeg": {
        "name": "Nutmeg", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },
    "saffron": {
        "name": "Saffron", "temp_min": 5, "temp_max": 15, "humidity_min": 40, "humidity_max": 50,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "spice"
    },

    # ===== OILSEEDS =====
    "sunflower": {
        "name": "Sunflower Seed", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "oilseed"
    },
    "sesame": {
        "name": "Sesame/Til", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "oilseed"
    },
    "linseed": {
        "name": "Linseed/Flax", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "oilseed"
    },
    "castor": {
        "name": "Castor Seed", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "oilseed"
    },
    "rapeseed": {
        "name": "Rapeseed/Canola", "temp_min": 5, "temp_max": 15, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "oilseed"
    },

    # ===== CASH CROPS =====
    "sugarcane": {
        "name": "Sugarcane", "temp_min": 20, "temp_max": 30, "humidity_min": 70, "humidity_max": 80,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "cash_crop"
    },
    "cotton": {
        "name": "Cotton", "temp_min": 10, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "cash_crop"
    },
    "jute": {
        "name": "Jute", "temp_min": 15, "temp_max": 25, "humidity_min": 60, "humidity_max": 70,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "cash_crop"
    },
    "tobacco": {
        "name": "Tobacco", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "Ammonia", "shelf_life": 365, "category": "cash_crop"
    },
    "tea": {
        "name": "Tea", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "cash_crop"
    },
    "coffee": {
        "name": "Coffee", "temp_min": 10, "temp_max": 20, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "cash_crop"
    },
    "rubber": {
        "name": "Rubber", "temp_min": 20, "temp_max": 30, "humidity_min": 70, "humidity_max": 80,
        "harmful_gas": "Ammonia", "shelf_life": 365, "category": "cash_crop"
    },

    # ===== FLOWERS =====
    "rose": {
        "name": "Rose", "temp_min": 1, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "flower"
    },
    "marigold": {
        "name": "Marigold", "temp_min": 2, "temp_max": 5, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 5, "category": "flower"
    },
    "jasmine": {
        "name": "Jasmine", "temp_min": 2, "temp_max": 5, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 3, "category": "flower"
    },
    "tuberose": {
        "name": "Tuberose", "temp_min": 2, "temp_max": 5, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 5, "category": "flower"
    },
    "chrysanthemum": {
        "name": "Chrysanthemum", "temp_min": 1, "temp_max": 4, "humidity_min": 90, "humidity_max": 95,
        "harmful_gas": "Ethylene", "shelf_life": 14, "category": "flower"
    },
    "gladiolus": {
        "name": "Gladiolus", "temp_min": 2, "temp_max": 5, "humidity_min": 85, "humidity_max": 90,
        "harmful_gas": "Ethylene", "shelf_life": 7, "category": "flower"
    },

    # ===== DAIRY & OTHERS =====
    "milk": {
        "name": "Milk", "temp_min": 1, "temp_max": 4, "humidity_min": 80, "humidity_max": 85,
        "harmful_gas": "Ammonia", "shelf_life": 7, "category": "dairy"
    },
    "curd": {
        "name": "Curd/Yogurt", "temp_min": 1, "temp_max": 4, "humidity_min": 80, "humidity_max": 85,
        "harmful_gas": "CO2", "shelf_life": 14, "category": "dairy"
    },
    "butter": {
        "name": "Butter", "temp_min": -1, "temp_max": 4, "humidity_min": 70, "humidity_max": 80,
        "harmful_gas": "CO2", "shelf_life": 60, "category": "dairy"
    },
    "cheese": {
        "name": "Cheese", "temp_min": 1, "temp_max": 7, "humidity_min": 75, "humidity_max": 85,
        "harmful_gas": "Ammonia", "shelf_life": 90, "category": "dairy"
    },
    "honey": {
        "name": "Honey", "temp_min": 18, "temp_max": 24, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 730, "category": "other"
    },
    "jaggery": {
        "name": "Jaggery/Gud", "temp_min": 15, "temp_max": 25, "humidity_min": 55, "humidity_max": 65,
        "harmful_gas": "CO2", "shelf_life": 365, "category": "other"
    },
}


def get_crop_info(crop_key):
    """Get crop information by key"""
    crop_key = crop_key.lower().strip().replace(' ', '_')
    return CROP_DATABASE.get(crop_key, None)


def get_all_crops():
    """Get all crops grouped by category"""
    categories = {}
    for key, crop in CROP_DATABASE.items():
        cat = crop['category']
        if cat not in categories:
            categories[cat] = []
        crop_with_key = crop.copy()
        crop_with_key['key'] = key
        categories[cat].append(crop_with_key)
    return categories


def get_crop_list():
    """Get flat list of all crops"""
    result = []
    for key, crop in CROP_DATABASE.items():
        crop_with_key = crop.copy()
        crop_with_key['key'] = key
        result.append(crop_with_key)
    return result


def search_crops(query):
    """Search crops by name"""
    query = query.lower()
    results = []
    for key, crop in CROP_DATABASE.items():
        if query in key or query in crop['name'].lower():
            crop_with_key = crop.copy()
            crop_with_key['key'] = key
            results.append(crop_with_key)
    return results
