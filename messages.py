# Multilingual templates and strings for Dharashiv Home Services Bot

MESSAGES = {
    "mr": {
        "welcome": (
            "🙏 **नमस्कार! धाराशिव होम सर्व्हिसेस मध्ये आपले स्वागत आहे!**\n"
            "*(Welcome to Dharashiv Home Services)*\n\n"
            "आम्ही **धाराशिव शहर (उस्मानाबाद) आणि आजूबाजूच्या सर्व खेड्यांमध्ये** विश्वासू व दर्जेदार सेवा पुरवतो.\n\n"
            "आमचा कुशल कारागीर/तंत्रज्ञ आपल्या घरी प्रत्यक्ष भेट देऊन पाहणी करेल व कामाचा योग्य अंदाज (Estimate) देईल.\n\n"
            "👇 **कृपया आपल्याला हवी असलेली सेवा खाली निवडा:**"
        ),
        "choose_service": "🛠️ **कृपया आपल्याला आवश्यक असलेली सेवा निवडा:**",
        "service_selected": "आपण निवडलेली सेवा: **{service_name}**\n\n👤 **कृपया आपले पूर्ण नाव सांगा:**",
        "ask_phone": (
            "धन्यवाद {name}!\n\n"
            "📞 **कृपया आपला संपर्क (मोबाईल) नंबर पाठवा:**\n"
            "(तुम्ही खालील '📱 मोबाईल नंबर शेअर करा' बटण वापरू शकता किंवा टाईप करून पाठवू शकता)"
        ),
        "ask_area": (
            "📍 **आपला पत्ता / गाव सांगा:**\n"
            "(उदा. धाराशिव शहर, समर्थ नगर, नेहरू चौक, येडशी, तेर, ढोकी, बेंबळी किंवा इतर गाव)"
        ),
        "ask_problem": (
            "📝 **कामाचे थोडक्यात स्वरूप किंवा समस्या सांगा:**\n"
            "(उदा. नळ लिकेज आहे / नवीन वायरिंग करायची आहे / डिशचे सिग्नल येत नाही / रंगकाम करायचे आहे इ.)"
        ),
        "ask_preferred_time": (
            "⏰ **आमच्या तंत्रज्ञाने व्हिजिट/तपासणीसाठी (Visit for Estimation) कधी यावे?**\n"
            "(उदा. 'आज दुपारी', 'उद्या सकाळी १० वाजता', 'रविवार' किंवा 'लवकरात लवकर')"
        ),
        "confirm_lead": (
            "🎉 **आपली विनंती यशस्वीरीत्या नोंदवली गेली आहे!**\n\n"
            "📋 **आपल्या अर्जाचा तपशील:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔖 **नोंदणी क्र. (Booking ID):** `{ref_code}`\n"
            "👤 **नाव:** {name}\n"
            "📞 **मोबाईल:** {phone}\n"
            "🛠️ **सेवा:** {service}\n"
            "📍 **गाव / परिसर:** {area}\n"
            "📝 **समस्या / काम:** {problem}\n"
            "⏰ **सोयीची वेळ:** {time}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ **पुढील पायरी:**\n"
            "आमचा प्रतिनिधी / तंत्रज्ञ थोड्याच वेळात आपल्याशी फोनवर संपर्क साधेल आणि प्रत्यक्ष पाहणी व एस्टिमेटसाठी व्हिजिट ठरवेल.\n\n"
            "📞 काही अडचण असल्यास संपर्क: {support_phone}\n\n"
            "धाराशिव होम सर्व्हिसेस निवडल्याबद्दल धन्यवाद! 🙏"
        ),
        "btn_share_contact": "📱 मोबाईल नंबर शेअर करा",
        "btn_cancel": "❌ रद्द करा (Cancel)",
        "cancelled": "❌ आपली नोंदणी प्रक्रिया रद्द केली आहे. पुन्हा सुरू करण्यासाठी /start दाबा.",
        "invalid_phone": "⚠️ कृपया योग्य १० अंकी मोबाईल नंबर प्रविष्ट करा (उदा. 9823xxxxxx) किंवा बटण दाबा.",
        "lang_switched": "🌐 भाषा मराठीमध्ये बदलली आहे.",
        "help_text": (
            "ℹ️ **धाराशिव होम सर्व्हिसेस मदत केंद्र**\n\n"
            "📌 **उपलब्ध कमांड्स:**\n"
            "• /start - नवीन सेवा बुक करा / मुख्य मेनू\n"
            "• /services - सर्व उपलब्ध सेवांची यादी\n"
            "• /myrequests - तुमच्या आधीच्या विनंत्या तपासा\n"
            "• /language - भाषा बदला (मराठी / English)\n"
            "• /contact - आमचा पत्ता व फोन नंबर\n\n"
            "📍 **कार्यक्षेत्र:** धाराशिव शहर व लगतची सर्व गावे (येडशी, तेर, ढोकी, बेंबळी आदी)\n"
            "📞 **थेट संपर्क:** {support_phone}\n"
            "💬 **व्हॉट्सॲप:** {support_whatsapp}"
        ),
        "my_requests_empty": "आपण अजून कोणतीही सेवा विनंती नोंदवलेली नाही. सेवा बुक करण्यासाठी /start दाबा.",
        "status_map": {
            "NEW": "नवीन (New) - लवकरच संपर्क होईल",
            "CONTACTED": "संपर्क साधला (Contacted)",
            "VISIT_SCHEDULED": "व्हिजिट निश्चित झाली (Visit Scheduled)",
            "COMPLETED": "काम पूर्ण झाले (Completed)",
            "CANCELLED": "रद्द झाले (Cancelled)"
        }
    },
    "en": {
        "welcome": (
            "🙏 **Welcome to Dharashiv Home Services!**\n"
            "*(धाराशिव होम सर्व्हिसेसमध्ये आपले स्वागत आहे)*\n\n"
            "We offer trustworthy repair and maintenance services in **Dharashiv city and nearby villages**.\n\n"
            "Our certified technician will visit your location to inspect the work and provide an accurate estimate.\n\n"
            "👇 **Please choose the service you need below:**"
        ),
        "choose_service": "🛠️ **Please select the service required:**",
        "service_selected": "Selected Service: **{service_name}**\n\n👤 **Please enter your full name:**",
        "ask_phone": (
            "Thank you {name}!\n\n"
            "📞 **Please enter your contact (mobile) number:**\n"
            "(You can tap the '📱 Share Contact' button or type it)"
        ),
        "ask_area": (
            "📍 **Please provide your location / village / area:**\n"
            "(e.g., Dharashiv City, Samarth Nagar, Bus Stand, Yedshi, Ter, Dhoki, Bembli, etc.)"
        ),
        "ask_problem": (
            "📝 **Please briefly describe the problem or work required:**\n"
            "(e.g., tap leak, inverter repair, painting 2 BHK, dish tv no signal, etc.)"
        ),
        "ask_preferred_time": (
            "⏰ **When would you like our technician to visit for inspection/estimate?**\n"
            "(e.g., 'Today afternoon', 'Tomorrow 10 AM', 'Sunday', or 'As soon as possible')"
        ),
        "confirm_lead": (
            "🎉 **Your service request has been successfully registered!**\n\n"
            "📋 **Booking Summary:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "🔖 **Booking ID:** `{ref_code}`\n"
            "👤 **Name:** {name}\n"
            "📞 **Phone:** {phone}\n"
            "🛠️ **Service:** {service}\n"
            "📍 **Location/Village:** {area}\n"
            "📝 **Problem:** {problem}\n"
            "⏰ **Preferred Visit Time:** {time}\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ **Next Step:**\n"
            "Our coordinator/technician will call you shortly to confirm the appointment for inspection and estimation.\n\n"
            "📞 Helpline: {support_phone}\n\n"
            "Thank you for choosing Dharashiv Home Services! 🙏"
        ),
        "btn_share_contact": "📱 Share Contact Number",
        "btn_cancel": "❌ Cancel",
        "cancelled": "❌ Request booking was cancelled. Send /start to begin again.",
        "invalid_phone": "⚠️ Please enter a valid 10-digit mobile number (e.g., 9823xxxxxx) or tap Share Contact.",
        "lang_switched": "🌐 Language changed to English.",
        "help_text": (
            "ℹ️ **Dharashiv Home Services Helpdesk**\n\n"
            "📌 **Commands:**\n"
            "• /start - Book a new service / Main menu\n"
            "• /services - View all available services\n"
            "• /myrequests - Check your booking history\n"
            "• /language - Change language (मराठी / English)\n"
            "• /contact - Direct support & phone numbers\n\n"
            "📍 **Coverage Area:** Dharashiv city and surrounding villages.\n"
            "📞 **Call:** {support_phone}\n"
            "💬 **WhatsApp:** {support_whatsapp}"
        ),
        "my_requests_empty": "You have no registered requests yet. Type /start to book a service.",
        "status_map": {
            "NEW": "New - Pending Contact",
            "CONTACTED": "Contacted",
            "VISIT_SCHEDULED": "Visit Scheduled for Estimate",
            "COMPLETED": "Work Completed",
            "CANCELLED": "Cancelled"
        }
    }
}

def get_msg(key: str, lang: str = "mr", **kwargs) -> str:
    lang_dict = MESSAGES.get(lang, MESSAGES["mr"])
    text = lang_dict.get(key, MESSAGES["mr"].get(key, ""))
    if kwargs:
        return text.format(**kwargs)
    return text
