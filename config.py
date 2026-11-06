import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Admin Telegram Chat IDs (comma-separated if multiple, e.g. "12345678,87654321")
ADMIN_IDS = [
    int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()
]

# Business Information for Dharashiv
BUSINESS_NAME_MR = "धाराशिव होम सर्व्हिसेस"
BUSINESS_NAME_EN = "Dharashiv Home Services"
SUPPORT_PHONE = os.getenv("SUPPORT_PHONE", "+91 98XXXXXXXX")
SUPPORT_WHATSAPP = os.getenv("SUPPORT_WHATSAPP", "+91 98XXXXXXXX")
OFFICE_LOCATION = "धाराशिव शहर (उस्मानाबाद), महाराष्ट्र"

# Coverage Area
POPULAR_AREAS = [
    "धाराशिव शहर (Dharashiv City)",
    "शिवाजी नगर / समर्थ नगर",
    "नेहरू चौक / बस स्टँड परिसर",
    " MIDC / औसा रोड",
    "येडशी (Yedshi)",
    "तेर (Ter)",
    "ढोकी (Dhoki)",
    "बेंबळी (Bembli)",
    "कळंब रोड परिसर (Kalamb Rd)",
    "तुळजापूर नाका परिसर",
    "इतर जवळचे गाव (Nearby Village)"
]

# Services List
SERVICES = [
    {
        "id": "electrician",
        "name_mr": "⚡ इलेक्ट्रिशियन (Electrician)",
        "name_en": "⚡ Electrician Work",
        "desc_mr": "घरातील वायरिंग, पंखा, गिझर, ट्यूबलाईट, शॉर्ट सर्किट, स्वीच बोर्ड दुरुस्ती.",
        "desc_en": "Wiring, Fan, Geyser, MCB, Short circuit, Inverter and all electrical repairs."
    },
    {
        "id": "painting",
        "name_mr": "🎨 घर रंगकाम / पेंटिंग (Home Painting)",
        "name_en": "🎨 Home Painting",
        "desc_mr": "आतील व बाहेरील रंगकाम, वॉटरप्रूफिंग, पुट्टी, डिझाईन पेंटिंग कामे.",
        "desc_en": "Interior & Exterior painting, Waterproofing, Putty, Wall design work."
    },
    {
        "id": "dish_tv",
        "name_mr": "📡 डिश टीव्ही दुरुस्ती (Dish TV Repair)",
        "name_en": "📡 Dish TV Repair & Fitting",
        "desc_mr": "टाटा प्ले, एअरटेल, डिश टीव्ही सिग्नल सेटिंग, नवीन फिटिंग व वायर दुरुस्ती.",
        "desc_en": "Tata Play, Airtel, Dish TV signal alignment, new dish fitting & wire repairs."
    },
    {
        "id": "plumbing",
        "name_mr": "🔧 प्लंबिंग / नळ दुरुस्ती (Plumbing)",
        "name_en": "🔧 Plumbing & Pipe Fitting",
        "desc_mr": "नळ लीकेज, पाण्याची टाकी फिटिंग, पाईपलाईन दुरुस्ती, बाथरूम फिटिंग.",
        "desc_en": "Tap leakages, water tank installation, drainage, bathroom sanitary fittings."
    },
    {
        "id": "solar",
        "name_mr": "☀️ सोलर दुरुस्ती व विक्री (Solar System)",
        "name_en": "☀️ Solar Repair & Sales",
        "desc_mr": "सोलर वॉटर हिटर, रूफटॉप सोलर पॅनेल बसवणे, सर्व्हिसिंग व सुटे भाग.",
        "desc_en": "Solar water heater, rooftop solar panels sales, installation and maintenance."
    },
    {
        "id": "appliances",
        "name_mr": "❄️ फ्रिज व वॉशिंग मशीन (Fridge/Washing Machine)",
        "name_en": "❄️ Fridge & Washing Machine Repair",
        "desc_mr": "सिंगल/डबल डोअर फ्रिज कूलिंग समस्या, गॅस भरणे, वॉशिंग मशीन दुरुस्ती.",
        "desc_en": "Single/double door fridge cooling issues, gas refilling, washing machine repairs."
    },
    {
        "id": "construction",
        "name_mr": "🧱 लहान बांधकाम व दुरुस्ती (Small Construction)",
        "name_en": "🧱 Small Construction & Masonry",
        "desc_mr": "टाईल्स फिटिंग, कट्टा बांधकाम, भिंतीला तडे/प्लास्टर, बाथरूम बांधकाम दुरुस्ती.",
        "desc_en": "Tiles fixing, plastering, crack repairs, kitchen/bathroom small civil repairs."
    },
    {
        "id": "lawn_gardening",
        "name_mr": "🌱 लॉन व बागकाम (Lawn & Gardening)",
        "name_en": "🌱 Lawn Making & Gardening",
        "desc_mr": "नवीन लॉन तयार करणे, झाडे कापणे/छाटणी, गार्डन मेंटेनन्स, माती व खत पुरवठा.",
        "desc_en": "New lawn development, plant trimming, garden maintenance, soil and fertilizers."
    },
    {
        "id": "all_other",
        "name_mr": "🛠️ इतर सर्व प्रकारच्या सेवा (Other Services)",
        "name_en": "🛠️ All Other Handyman Services",
        "desc_mr": "सुतारकाम, वेल्डिंग काम, आरओ वॉटर प्युरिफायर, सीसीटीव्ही आणि इतर सर्व कामे.",
        "desc_en": "Carpentry, Welding, RO water purifier, CCTV installation & all other handyman jobs."
    }
]
