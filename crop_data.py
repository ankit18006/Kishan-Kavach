"""
Kishan Kavach - Crop Database
100+ Indian crops with ideal storage conditions
"""

CROP_DATABASE = {
    # === GRAINS & CEREALS ===
    "wheat": {
        "name": "Wheat (गेहूं)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (60, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "grain"
    },
    "rice": {
        "name": "Rice (चावल)",
        "ideal_temp": (12, 18),
        "ideal_humidity": (60, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "grain"
    },
    "maize": {
        "name": "Maize (मक्का)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 450,
        "shelf_life_days": 180,
        "category": "grain"
    },
    "barley": {
        "name": "Barley (जौ)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (55, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 240,
        "category": "grain"
    },
    "millet": {
        "name": "Millet (बाजरा)",
        "ideal_temp": (12, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 150,
        "category": "grain"
    },
    "sorghum": {
        "name": "Sorghum (ज्वार)",
        "ideal_temp": (10, 16),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "grain"
    },
    "oats": {
        "name": "Oats (जई)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (55, 60),
        "gas_risk_threshold": 380,
        "shelf_life_days": 120,
        "category": "grain"
    },
    "ragi": {
        "name": "Ragi (रागी)",
        "ideal_temp": (12, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 150,
        "category": "grain"
    },

    # === PULSES & LENTILS ===
    "chickpea": {
        "name": "Chickpea (चना)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 365,
        "category": "pulse"
    },
    "lentil": {
        "name": "Lentil (मसूर)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 365,
        "category": "pulse"
    },
    "moong": {
        "name": "Moong Dal (मूंग)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 300,
        "category": "pulse"
    },
    "urad": {
        "name": "Urad Dal (उड़द)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 300,
        "category": "pulse"
    },
    "toor": {
        "name": "Toor Dal (तुअर)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 365,
        "category": "pulse"
    },
    "rajma": {
        "name": "Rajma (राजमा)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 380,
        "shelf_life_days": 365,
        "category": "pulse"
    },
    "peanut": {
        "name": "Peanut (मूंगफली)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 350,
        "shelf_life_days": 120,
        "category": "pulse"
    },
    "soybean": {
        "name": "Soybean (सोयाबीन)",
        "ideal_temp": (10, 18),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "pulse"
    },

    # === VEGETABLES ===
    "potato": {
        "name": "Potato (आलू)",
        "ideal_temp": (4, 8),
        "ideal_humidity": (85, 95),
        "gas_risk_threshold": 300,
        "shelf_life_days": 90,
        "category": "vegetable"
    },
    "onion": {
        "name": "Onion (प्याज)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (65, 70),
        "gas_risk_threshold": 300,
        "shelf_life_days": 60,
        "category": "vegetable"
    },
    "tomato": {
        "name": "Tomato (टमाटर)",
        "ideal_temp": (12, 15),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "vegetable"
    },
    "carrot": {
        "name": "Carrot (गाजर)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 30,
        "category": "vegetable"
    },
    "cauliflower": {
        "name": "Cauliflower (फूल गोभी)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "vegetable"
    },
    "cabbage": {
        "name": "Cabbage (पत्ता गोभी)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 30,
        "category": "vegetable"
    },
    "brinjal": {
        "name": "Brinjal (बैंगन)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 7,
        "category": "vegetable"
    },
    "okra": {
        "name": "Okra/Lady Finger (भिंडी)",
        "ideal_temp": (7, 10),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 7,
        "category": "vegetable"
    },
    "capsicum": {
        "name": "Capsicum (शिमला मिर्च)",
        "ideal_temp": (7, 10),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 14,
        "category": "vegetable"
    },
    "green_chili": {
        "name": "Green Chili (हरी मिर्च)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 280,
        "shelf_life_days": 14,
        "category": "vegetable"
    },
    "spinach": {
        "name": "Spinach (पालक)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 7,
        "category": "vegetable"
    },
    "peas": {
        "name": "Green Peas (मटर)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 10,
        "category": "vegetable"
    },
    "bitter_gourd": {
        "name": "Bitter Gourd (करेला)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 280,
        "shelf_life_days": 10,
        "category": "vegetable"
    },
    "bottle_gourd": {
        "name": "Bottle Gourd (लौकी)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 280,
        "shelf_life_days": 10,
        "category": "vegetable"
    },
    "pumpkin": {
        "name": "Pumpkin (कद्दू)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (50, 70),
        "gas_risk_threshold": 300,
        "shelf_life_days": 90,
        "category": "vegetable"
    },
    "cucumber": {
        "name": "Cucumber (खीरा)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 10,
        "category": "vegetable"
    },
    "radish": {
        "name": "Radish (मूली)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 14,
        "category": "vegetable"
    },
    "beetroot": {
        "name": "Beetroot (चुकंदर)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 280,
        "shelf_life_days": 30,
        "category": "vegetable"
    },
    "garlic": {
        "name": "Garlic (लहसुन)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (60, 70),
        "gas_risk_threshold": 300,
        "shelf_life_days": 60,
        "category": "vegetable"
    },
    "ginger": {
        "name": "Ginger (अदरक)",
        "ideal_temp": (12, 14),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 300,
        "shelf_life_days": 30,
        "category": "vegetable"
    },
    "mushroom": {
        "name": "Mushroom (मशरूम)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 5,
        "category": "vegetable"
    },
    "sweet_potato": {
        "name": "Sweet Potato (शकरकंद)",
        "ideal_temp": (12, 15),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 300,
        "shelf_life_days": 30,
        "category": "vegetable"
    },
    "corn": {
        "name": "Sweet Corn (भुट्टा)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 300,
        "shelf_life_days": 5,
        "category": "vegetable"
    },
    "drumstick": {
        "name": "Drumstick (सहजन)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 280,
        "shelf_life_days": 10,
        "category": "vegetable"
    },

    # === FRUITS ===
    "apple": {
        "name": "Apple (सेब)",
        "ideal_temp": (0, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 60,
        "category": "fruit"
    },
    "banana": {
        "name": "Banana (केला)",
        "ideal_temp": (13, 15),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "mango": {
        "name": "Mango (आम)",
        "ideal_temp": (12, 14),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 10,
        "category": "fruit"
    },
    "grape": {
        "name": "Grape (अंगूर)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "orange": {
        "name": "Orange (संतरा)",
        "ideal_temp": (3, 8),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 30,
        "category": "fruit"
    },
    "papaya": {
        "name": "Papaya (पपीता)",
        "ideal_temp": (10, 12),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "guava": {
        "name": "Guava (अमरूद)",
        "ideal_temp": (8, 10),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 10,
        "category": "fruit"
    },
    "watermelon": {
        "name": "Watermelon (तरबूज)",
        "ideal_temp": (10, 15),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "pomegranate": {
        "name": "Pomegranate (अनार)",
        "ideal_temp": (5, 7),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 30,
        "category": "fruit"
    },
    "lemon": {
        "name": "Lemon (नींबू)",
        "ideal_temp": (10, 13),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "pineapple": {
        "name": "Pineapple (अनानास)",
        "ideal_temp": (7, 12),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "litchi": {
        "name": "Litchi (लीची)",
        "ideal_temp": (1, 5),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "coconut": {
        "name": "Coconut (नारियल)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (75, 85),
        "gas_risk_threshold": 350,
        "shelf_life_days": 60,
        "category": "fruit"
    },
    "jackfruit": {
        "name": "Jackfruit (कटहल)",
        "ideal_temp": (12, 14),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "sapota": {
        "name": "Sapota/Chikoo (चीकू)",
        "ideal_temp": (15, 20),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 250,
        "shelf_life_days": 10,
        "category": "fruit"
    },
    "custard_apple": {
        "name": "Custard Apple (सीताफल)",
        "ideal_temp": (15, 20),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 5,
        "category": "fruit"
    },
    "fig": {
        "name": "Fig (अंजीर)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (85, 90),
        "gas_risk_threshold": 200,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "strawberry": {
        "name": "Strawberry (स्ट्रॉबेरी)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 5,
        "category": "fruit"
    },
    "kiwi": {
        "name": "Kiwi (कीवी)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 30,
        "category": "fruit"
    },
    "plum": {
        "name": "Plum (आलूबुखारा)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "peach": {
        "name": "Peach (आड़ू)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 14,
        "category": "fruit"
    },
    "cherry": {
        "name": "Cherry (चेरी)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 7,
        "category": "fruit"
    },
    "apricot": {
        "name": "Apricot (खुबानी)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 10,
        "category": "fruit"
    },
    "pear": {
        "name": "Pear (नाशपाती)",
        "ideal_temp": (0, 2),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 250,
        "shelf_life_days": 30,
        "category": "fruit"
    },

    # === SPICES ===
    "turmeric": {
        "name": "Turmeric (हल्दी)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 450,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "red_chili": {
        "name": "Red Chili (लाल मिर्च)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "spice"
    },
    "cumin": {
        "name": "Cumin (जीरा)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "coriander": {
        "name": "Coriander (धनिया)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "spice"
    },
    "mustard_seed": {
        "name": "Mustard Seed (राई)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "fenugreek": {
        "name": "Fenugreek (मेथी)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "cardamom": {
        "name": "Cardamom (इलायची)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "black_pepper": {
        "name": "Black Pepper (काली मिर्च)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "clove": {
        "name": "Clove (लौंग)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "cinnamon": {
        "name": "Cinnamon (दालचीनी)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "fennel": {
        "name": "Fennel (सौंफ)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "ajwain": {
        "name": "Ajwain (अजवाइन)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "spice"
    },
    "saffron": {
        "name": "Saffron (केसर)",
        "ideal_temp": (5, 15),
        "ideal_humidity": (40, 50),
        "gas_risk_threshold": 350,
        "shelf_life_days": 730,
        "category": "spice"
    },

    # === OIL SEEDS ===
    "sesame": {
        "name": "Sesame (तिल)",
        "ideal_temp": (10, 20),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "oilseed"
    },
    "sunflower": {
        "name": "Sunflower Seed (सूरजमुखी)",
        "ideal_temp": (10, 20),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "oilseed"
    },
    "linseed": {
        "name": "Linseed (अलसी)",
        "ideal_temp": (10, 20),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "oilseed"
    },
    "castor": {
        "name": "Castor (अरंडी)",
        "ideal_temp": (10, 20),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "oilseed"
    },
    "groundnut": {
        "name": "Groundnut (मूंगफली)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 350,
        "shelf_life_days": 120,
        "category": "oilseed"
    },

    # === CASH CROPS ===
    "sugarcane": {
        "name": "Sugarcane (गन्ना)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (80, 85),
        "gas_risk_threshold": 300,
        "shelf_life_days": 14,
        "category": "cash_crop"
    },
    "cotton": {
        "name": "Cotton (कपास)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (45, 55),
        "gas_risk_threshold": 500,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },
    "jute": {
        "name": "Jute (जूट)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (50, 65),
        "gas_risk_threshold": 450,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },
    "tea": {
        "name": "Tea (चाय)",
        "ideal_temp": (5, 15),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 350,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },
    "coffee": {
        "name": "Coffee (कॉफी)",
        "ideal_temp": (10, 20),
        "ideal_humidity": (50, 60),
        "gas_risk_threshold": 350,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },
    "tobacco": {
        "name": "Tobacco (तम्बाकू)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },
    "rubber": {
        "name": "Rubber (रबड़)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 450,
        "shelf_life_days": 365,
        "category": "cash_crop"
    },

    # === DAIRY & OTHER ===
    "milk": {
        "name": "Milk (दूध)",
        "ideal_temp": (2, 4),
        "ideal_humidity": (80, 90),
        "gas_risk_threshold": 150,
        "shelf_life_days": 5,
        "category": "dairy"
    },
    "curd": {
        "name": "Curd (दही)",
        "ideal_temp": (2, 5),
        "ideal_humidity": (80, 90),
        "gas_risk_threshold": 150,
        "shelf_life_days": 7,
        "category": "dairy"
    },
    "paneer": {
        "name": "Paneer (पनीर)",
        "ideal_temp": (2, 4),
        "ideal_humidity": (80, 90),
        "gas_risk_threshold": 150,
        "shelf_life_days": 5,
        "category": "dairy"
    },
    "ghee": {
        "name": "Ghee (घी)",
        "ideal_temp": (15, 25),
        "ideal_humidity": (40, 50),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dairy"
    },
    "butter": {
        "name": "Butter (मक्खन)",
        "ideal_temp": (2, 5),
        "ideal_humidity": (75, 85),
        "gas_risk_threshold": 200,
        "shelf_life_days": 30,
        "category": "dairy"
    },

    # === DRY FRUITS ===
    "almond": {
        "name": "Almond (बादाम)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dry_fruit"
    },
    "cashew": {
        "name": "Cashew (काजू)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 180,
        "category": "dry_fruit"
    },
    "walnut": {
        "name": "Walnut (अखरोट)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dry_fruit"
    },
    "pistachio": {
        "name": "Pistachio (पिस्ता)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dry_fruit"
    },
    "raisin": {
        "name": "Raisin (किशमिश)",
        "ideal_temp": (5, 10),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dry_fruit"
    },
    "dates": {
        "name": "Dates (खजूर)",
        "ideal_temp": (0, 5),
        "ideal_humidity": (55, 65),
        "gas_risk_threshold": 400,
        "shelf_life_days": 365,
        "category": "dry_fruit"
    },

    # === FLOWERS ===
    "marigold": {
        "name": "Marigold (गेंदा)",
        "ideal_temp": (2, 5),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 3,
        "category": "flower"
    },
    "rose": {
        "name": "Rose (गुलाब)",
        "ideal_temp": (1, 4),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 5,
        "category": "flower"
    },
    "jasmine": {
        "name": "Jasmine (चमेली)",
        "ideal_temp": (2, 5),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 2,
        "category": "flower"
    },
    "lotus": {
        "name": "Lotus (कमल)",
        "ideal_temp": (2, 5),
        "ideal_humidity": (90, 95),
        "gas_risk_threshold": 200,
        "shelf_life_days": 3,
        "category": "flower"
    },
}


def get_crop_info(crop_key):
    """Get crop info by key, returns None if not found"""
    crop_key = crop_key.lower().strip().replace(' ', '_')
    return CROP_DATABASE.get(crop_key)


def get_all_crops():
    """Return all crops sorted by category"""
    return {k: v for k, v in sorted(CROP_DATABASE.items(), key=lambda x: x[1]['category'])}


def get_crops_by_category(category):
    """Return crops filtered by category"""
    return {k: v for k, v in CROP_DATABASE.items() if v['category'] == category}


def get_categories():
    """Return all unique categories"""
    return list(set(v['category'] for v in CROP_DATABASE.values()))


def search_crops(query):
    """Search crops by name"""
    query = query.lower().strip()
    results = {}
    for k, v in CROP_DATABASE.items():
        if query in k or query in v['name'].lower():
            results[k] = v
    return results
