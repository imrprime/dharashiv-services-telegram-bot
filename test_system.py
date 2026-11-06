import os
import database
import config
from messages import get_msg

def test_workflow():
    print("=== Testing Dharashiv Home Services System ===")
    
    # 1. Initialize DB
    database.init_db()
    print("✅ Database initialized successfully.")
    
    # 2. Test Multilingual Messages
    welcome_mr = get_msg("welcome", lang="mr")
    assert "धाराशिव होम सर्व्हिसेस" in welcome_mr, "Marathi welcome failed"
    print("✅ Marathi welcome message verified.")
    
    welcome_en = get_msg("welcome", lang="en")
    assert "Dharashiv Home Services" in welcome_en, "English welcome failed"
    print("✅ English welcome message verified.")
    
    # 3. Create Sample Leads in Dharashiv
    sample_leads = [
        {
            "telegram_id": 99887766,
            "name": "राजेश पाटील (Rajesh Patil)",
            "phone": "9822112233",
            "service_id": "electrician",
            "service_title": "⚡ इलेक्ट्रिशियन (Electrician)",
            "problem": "हॉलमधील पंखा व गीझर वायरिंग शॉर्ट झाली आहे",
            "area": "समर्थ नगर, धाराशिव",
            "time": "उद्या सकाळी १० वाजता"
        },
        {
            "telegram_id": 88776655,
            "name": "गणेश शिंदे (Ganesh Shinde)",
            "phone": "9421556677",
            "service_id": "solar",
            "service_title": "☀️ सोलर दुरुस्ती व विक्री (Solar System)",
            "problem": "नवीन सोलर वॉटर हिटर बसवायचा आहे आणि एस्टिमेट पाहिजे",
            "area": "येडशी (Yedshi Village)",
            "time": "रविवार दुपारी २ वाजता"
        },
        {
            "telegram_id": 77665544,
            "name": "अमित कुलकर्णी (Amit Kulkarni)",
            "phone": "9977889900",
            "service_id": "lawn_gardening",
            "service_title": "🌱 लॉन व बागकाम (Lawn & Gardening)",
            "problem": "घरासमोर ५०० स्क्वेअर फूट जागेत नवीन लॉन लावायचे आहे",
            "area": "तेर रोड, धाराशिव",
            "time": "लवकरात लवकर"
        }
    ]
    
    created_leads = []
    for s in sample_leads:
        lead = database.create_lead(
            telegram_id=s["telegram_id"],
            customer_name=s["name"],
            customer_phone=s["phone"],
            service_id=s["service_id"],
            service_title=s["service_title"],
            problem_description=s["problem"],
            location_area=s["area"],
            preferred_time=s["time"]
        )
        created_leads.append(lead)
        print(f"✅ Created Lead #{lead['id']} ({lead['ref_code']}) for {s['name']} - {s['service_title']}")
        
    # 4. Check user history
    user_leads = database.get_user_leads(99887766)
    assert len(user_leads) >= 1
    print(f"✅ User leads retrieved: {len(user_leads)} requests found.")
    
    # 5. Test Status Update
    first_lead = created_leads[0]
    updated = database.update_lead_status(first_lead["id"], "VISIT_SCHEDULED", "टेक्निशियन सचिन यांना व्हिजिटसाठी सांगितले आहे")
    assert updated is True
    lead_check = database.get_lead(first_lead["id"])
    assert lead_check["status"] == "VISIT_SCHEDULED"
    print(f"✅ Lead status updated to: {lead_check['status']}")
    
    # 6. Test CSV Export
    csv_content = database.export_leads_to_csv()
    assert "राजेश पाटील" in csv_content
    assert "येडशी" in csv_content
    print("✅ CSV Export contains Marathi characters & lead details properly.")
    
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! The system is 100% ready.")

if __name__ == "__main__":
    test_workflow()
