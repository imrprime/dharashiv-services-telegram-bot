import logging
import re
import io
from typing import Dict, Any

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

import config
import database
from messages import get_msg

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation States
(
    STATE_SERVICE,
    STATE_NAME,
    STATE_PHONE,
    STATE_AREA,
    STATE_PROBLEM,
    STATE_TIME
) = range(6)

def get_user_lang(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> str:
    if "lang" in context.user_data:
        return context.user_data["lang"]
    user = database.get_user(user_id)
    if user and user.get("language"):
        lang = user["language"]
        context.user_data["lang"] = lang
        return lang
    return "mr"

def build_services_keyboard(lang: str = "mr") -> InlineKeyboardMarkup:
    keyboard = []
    # 2 buttons per row
    row = []
    for s in config.SERVICES:
        btn_text = s["name_mr"] if lang == "mr" else s["name_en"]
        row.append(InlineKeyboardButton(btn_text, callback_data=f"srv_{s['id']}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
        
    # Language toggle button at bottom
    lang_btn_text = "🌐 English" if lang == "mr" else "🌐 मराठी (Marathi)"
    lang_code = "en" if lang == "mr" else "mr"
    keyboard.append([InlineKeyboardButton(lang_btn_text, callback_data=f"lang_{lang_code}")])
    
    return InlineKeyboardMarkup(keyboard)

def build_area_keyboard(lang: str = "mr") -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("📍 धाराशिव शहर (Dharashiv City)", callback_data="area_Dharashiv City"),
            InlineKeyboardButton("📍 येडशी (Yedshi)", callback_data="area_Yedshi"),
        ],
        [
            InlineKeyboardButton("📍 तेर (Ter)", callback_data="area_Ter"),
            InlineKeyboardButton("📍 ढोकी (Dhoki)", callback_data="area_Dhoki"),
        ],
        [
            InlineKeyboardButton("📍 बेंबळी (Bembli)", callback_data="area_Bembli"),
            InlineKeyboardButton("📍 तुळजापूर नाका परिसर", callback_data="area_Tuljapur Naka"),
        ],
        [
            InlineKeyboardButton("✍️ इतर गाव / पत्ता टाईप करा (Type Other)", callback_data="area_manual")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def build_time_keyboard(lang: str = "mr") -> InlineKeyboardMarkup:
    if lang == "mr":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ लवकरात लवकर (ASAP)", callback_data="time_लवकरात लवकर (ASAP)"),
                InlineKeyboardButton("🌅 आज दुपारी / संध्याकाळी", callback_data="time_आज दुपारी / संध्याकाळी"),
            ],
            [
                InlineKeyboardButton("☀️ उद्या सकाळी (१० ते १)", callback_data="time_उद्या सकाळी (१० ते १)"),
                InlineKeyboardButton("⛅ उद्या दुपारी (२ ते ६)", callback_data="time_उद्या दुपारी (२ ते ६)"),
            ],
            [
                InlineKeyboardButton("✍️ स्वतः टाईप करा (Type time)", callback_data="time_manual")
            ]
        ])
    else:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚡ As soon as possible (ASAP)", callback_data="time_ASAP"),
                InlineKeyboardButton("🌅 Today Afternoon / Evening", callback_data="time_Today Afternoon"),
            ],
            [
                InlineKeyboardButton("☀️ Tomorrow Morning (10-1)", callback_data="time_Tomorrow Morning"),
                InlineKeyboardButton("⛅ Tomorrow Afternoon (2-6)", callback_data="time_Tomorrow Afternoon"),
            ],
            [
                InlineKeyboardButton("✍️ Type custom time", callback_data="time_manual")
            ]
        ])

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Welcomes the user in Marathi & English and prompts for service."""
    user = update.effective_user
    database.save_or_update_user(
        telegram_id=user.id,
        username=user.username or "",
        full_name=user.full_name or ""
    )
    
    lang = get_user_lang(user.id, context)
    welcome_text = get_msg("welcome", lang=lang)
    reply_markup = build_services_keyboard(lang=lang)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        
    return STATE_SERVICE

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    target_lang = query.data.split("_")[1]
    user_id = update.effective_user.id
    
    database.set_user_language(user_id, target_lang)
    context.user_data["lang"] = target_lang
    
    welcome_text = get_msg("welcome", lang=target_lang)
    reply_markup = build_services_keyboard(lang=target_lang)
    
    await query.edit_message_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return STATE_SERVICE

async def service_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    service_id = query.data.replace("srv_", "")
    lang = get_user_lang(update.effective_user.id, context)
    
    # Find service details
    service_info = next((s for s in config.SERVICES if s["id"] == service_id), None)
    if not service_info:
        service_name = service_id
    else:
        service_name = service_info["name_mr"] if lang == "mr" else service_info["name_en"]
        
    context.user_data["service_id"] = service_id
    context.user_data["service_name"] = service_name
    
    text = get_msg("service_selected", lang=lang, service_name=service_name)
    
    await query.edit_message_text(text, parse_mode="Markdown")
    return STATE_NAME

async def name_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip()
    context.user_data["customer_name"] = name
    lang = get_user_lang(update.effective_user.id, context)
    
    # Request contact button
    btn_label = get_msg("btn_share_contact", lang=lang)
    btn_cancel = get_msg("btn_cancel", lang=lang)
    
    reply_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(btn_label, request_contact=True)],
            [KeyboardButton(btn_cancel)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    prompt = get_msg("ask_phone", lang=lang, name=name)
    await update.message.reply_text(prompt, reply_markup=reply_markup, parse_mode="Markdown")
    return STATE_PHONE

async def phone_contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    phone = contact.phone_number
    return await process_phone(phone, update, context)

async def phone_text_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    lang = get_user_lang(update.effective_user.id, context)
    
    if text in ["❌ रद्द करा (Cancel)", "❌ Cancel", "/cancel"]:
        return await cancel_handler(update, context)
        
    # Basic phone validation: at least 10 digits
    cleaned_phone = re.sub(r"[^\d+]", "", text)
    if len(re.sub(r"[^\d]", "", cleaned_phone)) < 10:
        await update.message.reply_text(get_msg("invalid_phone", lang=lang))
        return STATE_PHONE
        
    return await process_phone(cleaned_phone, update, context)

async def process_phone(phone: str, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["customer_phone"] = phone
    lang = get_user_lang(update.effective_user.id, context)
    
    # Prompt for area with quick suggestions
    await update.message.reply_text(
        get_msg("ask_area", lang=lang),
        reply_markup=ReplyKeyboardRemove()
    )
    
    area_markup = build_area_keyboard(lang=lang)
    await update.message.reply_text(
        "👇 धाराशिव शहर किंवा जवळचे गाव निवडा:" if lang == "mr" else "👇 Select Dharashiv or nearby village:",
        reply_markup=area_markup
    )
    return STATE_AREA

async def area_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    chosen = query.data.replace("area_", "")
    lang = get_user_lang(update.effective_user.id, context)
    
    if chosen == "manual":
        prompt = (
            "✍️ **कृपया आपल्या गावाचे नाव आणि गल्ली/पत्ता टाईप करून पाठवा:**" 
            if lang == "mr" else 
            "✍️ **Please type your village name or detailed address:**"
        )
        await query.edit_message_text(prompt, parse_mode="Markdown")
        return STATE_AREA
        
    context.user_data["location_area"] = chosen
    
    # Ask for problem description
    prompt = get_msg("ask_problem", lang=lang)
    await query.edit_message_text(f"📍 पत्ता/गाव: **{chosen}**\n\n{prompt}", parse_mode="Markdown")
    return STATE_PROBLEM

async def area_text_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    area = update.message.text.strip()
    context.user_data["location_area"] = area
    lang = get_user_lang(update.effective_user.id, context)
    
    prompt = get_msg("ask_problem", lang=lang)
    await update.message.reply_text(prompt, parse_mode="Markdown")
    return STATE_PROBLEM

async def problem_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    problem = update.message.text.strip()
    context.user_data["problem_description"] = problem
    lang = get_user_lang(update.effective_user.id, context)
    
    time_markup = build_time_keyboard(lang=lang)
    prompt = get_msg("ask_preferred_time", lang=lang)
    
    await update.message.reply_text(prompt, reply_markup=time_markup, parse_mode="Markdown")
    return STATE_TIME

async def time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    chosen = query.data.replace("time_", "")
    lang = get_user_lang(update.effective_user.id, context)
    
    if chosen == "manual":
        prompt = (
            "✍️ **कृपया आपल्या सोयीची वेळ किंवा वार टाईप करा:**\n(उदा. उद्या सायंकाळी ५ नंतर)" 
            if lang == "mr" else 
            "✍️ **Please type your preferred time or date:**"
        )
        await query.edit_message_text(prompt, parse_mode="Markdown")
        return STATE_TIME
        
    context.user_data["preferred_time"] = chosen
    return await finish_lead_creation(update, context, chosen)

async def time_text_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    time_text = update.message.text.strip()
    context.user_data["preferred_time"] = time_text
    return await finish_lead_creation(update, context, time_text)

async def finish_lead_creation(update: Update, context: ContextTypes.DEFAULT_TYPE, preferred_time: str) -> int:
    user = update.effective_user
    lang = get_user_lang(user.id, context)
    
    name = context.user_data.get("customer_name", user.full_name or "ग्राहक")
    phone = context.user_data.get("customer_phone", "")
    service_id = context.user_data.get("service_id", "other")
    service_name = context.user_data.get("service_name", "सर्व्हिस")
    area = context.user_data.get("location_area", "धाराशिव परिसर")
    problem = context.user_data.get("problem_description", "तपासणी व काम")
    
    # Create lead in database
    lead = database.create_lead(
        telegram_id=user.id,
        customer_name=name,
        customer_phone=phone,
        service_id=service_id,
        service_title=service_name,
        problem_description=problem,
        location_area=area,
        preferred_time=preferred_time
    )
    
    ref_code = lead.get("ref_code", "DH-NEW")
    
    # Customer confirmation text
    confirmation_text = get_msg(
        "confirm_lead",
        lang=lang,
        ref_code=ref_code,
        name=name,
        phone=phone,
        service=service_name,
        area=area,
        problem=problem,
        time=preferred_time,
        support_phone=config.SUPPORT_PHONE
    )
    
    if update.callback_query:
        await update.callback_query.edit_message_text(confirmation_text, parse_mode="Markdown")
    else:
        await update.message.reply_text(confirmation_text, parse_mode="Markdown")
        
    # Notify Admins
    admin_alert = (
        f"🚨 **नवीन सेवा विनंती (New Lead Alert)!**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔖 **Ref:** `{ref_code}` (ID: {lead['id']})\n"
        f"👤 **ग्राहक:** {name}\n"
        f"📞 **फोन:** [{phone}](tel:{phone})\n"
        f"🛠️ **सेवा:** {service_name}\n"
        f"📍 **गाव / परिसर:** {area}\n"
        f"📝 **तक्रार / काम:** {problem}\n"
        f"⏰ **सोयीची वेळ:** {preferred_time}\n"
        f"📅 **वेळ:** {lead.get('created_at')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👉 स्टेटस बदला:"
    )
    
    admin_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📞 संपर्क केला", callback_data=f"adm_stat_{lead['id']}_CONTACTED"),
            InlineKeyboardButton("📅 व्हिजिट ठरली", callback_data=f"adm_stat_{lead['id']}_VISIT_SCHEDULED"),
        ],
        [
            InlineKeyboardButton("✅ काम पूर्ण", callback_data=f"adm_stat_{lead['id']}_COMPLETED"),
            InlineKeyboardButton("❌ रद्द", callback_data=f"adm_stat_{lead['id']}_CANCELLED"),
        ]
    ])
    
    for admin_id in config.ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_alert,
                reply_markup=admin_markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Failed to alert admin {admin_id}: {e}")
            
    # Clear conversation data
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    lang = get_user_lang(update.effective_user.id, context)
    context.user_data.clear()
    text = get_msg("cancelled", lang=lang)
    
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text)
    else:
        await update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def services_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id, context)
    title = "🛠️ **धाराशिव होम सर्व्हिसेस - सर्व सेवांची यादी:**\n\n" if lang == "mr" else "🛠️ **Dharashiv Home Services - All Available Services:**\n\n"
    
    lines = [title]
    for s in config.SERVICES:
        name = s["name_mr"] if lang == "mr" else s["name_en"]
        desc = s["desc_mr"] if lang == "mr" else s["desc_en"]
        lines.append(f"**{name}**\n_{desc}_\n")
        
    lines.append("\n👉 सेवा बुक करण्यासाठी /start पाठवा किंवा खालील बटण दाबा.")
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ आताच बुक करा (Book Now)", callback_data="start_booking")]
    ])
    
    await update.message.reply_text("\n".join(lines), reply_markup=markup, parse_mode="Markdown")

async def my_requests_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id, context)
    leads = database.get_user_leads(user_id, limit=5)
    
    if not leads:
        await update.message.reply_text(get_msg("my_requests_empty", lang=lang))
        return
        
    status_map = MESSAGES[lang]["status_map"]
    lines = ["📋 **आपल्या अलीकडील सेवा विनंत्या:**\n" if lang == "mr" else "📋 **Your Recent Service Requests:**\n"]
    
    for l in leads:
        st_text = status_map.get(l["status"], l["status"])
        lines.append(
            f"🔖 **{l['ref_code']}** - {l['service_title']}\n"
            f"📍 {l['location_area']} | ⏰ {l['preferred_time']}\n"
            f"📊 स्थिती: `{st_text}`\n"
            f"📅 {l['created_at']}\n"
            f"──────────────────"
        )
        
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id, context)
    text = (
        f"🏢 **{config.BUSINESS_NAME_MR}**\n"
        f"({config.BUSINESS_NAME_EN})\n\n"
        f"📍 **पत्ता:** {config.OFFICE_LOCATION}\n"
        f"🌍 **कव्हरेज:** धाराशिव शहर व लगतची सर्व गावे\n"
        f"📞 **फोन कॉल:** [{config.SUPPORT_PHONE}](tel:{config.SUPPORT_PHONE})\n"
        f"💬 **व्हॉट्सॲप:** {config.SUPPORT_WHATSAPP}\n\n"
        f"आम्ही प्रत्यक्ष जागेवर येऊन कामाची पाहणी करतो व योग्य एस्टिमेट देतो!"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_user_lang(update.effective_user.id, context)
    text = get_msg(
        "help_text",
        lang=lang,
        support_phone=config.SUPPORT_PHONE,
        support_whatsapp=config.SUPPORT_WHATSAPP
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("मराठी (Marathi)", callback_data="lang_mr"),
            InlineKeyboardButton("English", callback_data="lang_en")
        ]
    ])
    await update.message.reply_text("🌐 कृपया भाषा निवडा / Please select your language:", reply_markup=keyboard)

# ── Admin Handlers ──────────────────────────────────────────────────────────

def is_admin(user_id: int) -> bool:
    return not config.ADMIN_IDS or user_id in config.ADMIN_IDS

async def admin_leads_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("⛔ You are not authorized as admin.")
        return
        
    leads = database.get_recent_leads(limit=10)
    if not leads:
        await update.message.reply_text("No leads in database yet.")
        return
        
    text_lines = ["📋 **Recent 10 Leads (Dharashiv):**\n"]
    for l in leads:
        text_lines.append(
            f"🔹 **ID {l['id']}** | `{l['ref_code']}` | **{l['status']}**\n"
            f"👤 {l['customer_name']} ({l['customer_phone']})\n"
            f"🛠️ {l['service_title']} @ {l['location_area']}\n"
            f"📅 {l['created_at']}\n"
        )
    text_lines.append("\nView details: `/lead <id>` | Export all: `/export`")
    await update.message.reply_text("\n".join(text_lines), parse_mode="Markdown")

async def admin_lead_detail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
        
    if not context.args:
        await update.message.reply_text("Usage: `/lead <id>` e.g. `/lead 1`")
        return
        
    try:
        lead_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid lead ID.")
        return
        
    lead = database.get_lead(lead_id)
    if not lead:
        await update.message.reply_text(f"Lead ID {lead_id} not found.")
        return
        
    text = (
        f"📋 **Lead Details (ID: {lead['id']})**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔖 Ref Code: `{lead['ref_code']}`\n"
        f"👤 Customer: {lead['customer_name']}\n"
        f"📞 Phone: {lead['customer_phone']}\n"
        f"🛠️ Service: {lead['service_title']}\n"
        f"📍 Area/Village: {lead['location_area']}\n"
        f"📝 Description: {lead['problem_description']}\n"
        f"⏰ Preferred Time: {lead['preferred_time']}\n"
        f"📊 Status: `{lead['status']}`\n"
        f"🗒️ Admin Notes: {lead['admin_notes'] or 'None'}\n"
        f"📅 Created: {lead['created_at']}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📞 Contacted", callback_data=f"adm_stat_{lead['id']}_CONTACTED"),
            InlineKeyboardButton("📅 Visit Scheduled", callback_data=f"adm_stat_{lead['id']}_VISIT_SCHEDULED"),
        ],
        [
            InlineKeyboardButton("✅ Completed", callback_data=f"adm_stat_{lead['id']}_COMPLETED"),
            InlineKeyboardButton("❌ Cancelled", callback_data=f"adm_stat_{lead['id']}_CANCELLED"),
        ]
    ])
    await update.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")

async def admin_status_update_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await query.answer("Unauthorized", show_alert=True)
        return
        
    # Format: adm_stat_<id>_<status>
    parts = query.data.split("_")
    lead_id = int(parts[2])
    new_status = parts[3]
    
    database.update_lead_status(lead_id, new_status)
    lead = database.get_lead(lead_id)
    
    await query.edit_message_text(
        f"{query.message.text}\n\n🔄 **Status Updated To: `{new_status}`**",
        parse_mode="Markdown"
    )
    
    # Notify customer of status update if possible
    if lead and lead.get("telegram_id"):
        try:
            cust_lang = database.get_user(lead["telegram_id"]).get("language", "mr")
            status_text = MESSAGES[cust_lang]["status_map"].get(new_status, new_status)
            notify_msg = (
                f"🔔 **आपल्या सेवा विनंतीचे अपडेट:**\n"
                f"नोंदणी क्र.: `{lead['ref_code']}`\n"
                f"नवीन स्थिती: **{status_text}**\n\n"
                f"आमची टीम आपल्या सेवेसाठी तत्पर आहे!"
                if cust_lang == "mr" else
                f"🔔 **Service Request Update:**\n"
                f"Ref ID: `{lead['ref_code']}`\n"
                f"New Status: **{status_text}**"
            )
            await context.bot.send_message(
                chat_id=lead["telegram_id"],
                text=notify_msg,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.warning(f"Could not notify customer {lead['telegram_id']}: {e}")

async def admin_export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
        
    csv_data = database.export_leads_to_csv()
    csv_bytes = io.BytesIO(csv_data.encode("utf-8-sig")) # utf-8 with BOM for Excel compatibility with Marathi text
    csv_bytes.name = "dharashiv_leads.csv"
    
    await update.message.reply_document(
        document=csv_bytes,
        filename="dharashiv_leads.csv",
        caption="📊 **Dharashiv Home Services - Full Leads Export**",
        parse_mode="Markdown"
    )

def main():
    database.init_db()
    
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("="*60)
        print("⚠️ BOT_TOKEN is not configured in .env file!")
        print("Please set your BOT_TOKEN in /workspace/project/.env")
        print("Get your token by talking to @BotFather on Telegram.")
        print("="*60)
        return
        
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    # Greeting / Booking Conversation Flow
    booking_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_handler),
            CommandHandler("book", start_handler),
            # Trigger when user says Hi, Hello, Namaskar, etc.
            MessageHandler(
                filters.TEXT & filters.Regex(re.compile(r"^(hi|hello|hey|start|book|काम|नमस्कार|हाय|हॅलो)", re.IGNORECASE)),
                start_handler
            ),
            CallbackQueryHandler(start_handler, pattern="^start_booking$")
        ],
        states={
            STATE_SERVICE: [
                CallbackQueryHandler(language_callback, pattern="^lang_"),
                CallbackQueryHandler(service_selected_callback, pattern="^srv_")
            ],
            STATE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, name_received)
            ],
            STATE_PHONE: [
                MessageHandler(filters.CONTACT, phone_contact_received),
                MessageHandler(filters.TEXT & ~filters.COMMAND, phone_text_received)
            ],
            STATE_AREA: [
                CallbackQueryHandler(area_callback, pattern="^area_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, area_text_received)
            ],
            STATE_PROBLEM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, problem_received)
            ],
            STATE_TIME: [
                CallbackQueryHandler(time_callback, pattern="^time_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, time_text_received)
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_handler),
            MessageHandler(filters.Regex(re.compile(r"^(रद्द करा|cancel)$", re.IGNORECASE)), cancel_handler)
        ],
        allow_reentry=True
    )
    
    app.add_handler(booking_handler)
    
    # User Commands
    app.add_handler(CommandHandler("services", services_list_command))
    app.add_handler(CommandHandler("myrequests", my_requests_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("language", language_command))
    app.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
    
    # Admin Handlers
    app.add_handler(CommandHandler("leads", admin_leads_command))
    app.add_handler(CommandHandler("lead", admin_lead_detail_command))
    app.add_handler(CommandHandler("export", admin_export_command))
    app.add_handler(CallbackQueryHandler(admin_status_update_callback, pattern="^adm_stat_"))
    
    print("🚀 Dharashiv Home Services Telegram Bot is ready!")
    app.run_polling()

if __name__ == "__main__":
    main()
