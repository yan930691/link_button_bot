# handlers.py
import re
import uuid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from config import TEXTS, MAX_BUTTONS, ALLOWED_USER_IDS
from database import db
from keyboards import create_button_row, get_main_menu_keyboard
from telegraph_utils import create_telegraph_page, format_content_to_html

WAITING_FOR_BUTTONS = 1

def get_text(user_id, key):
    lang = db.get_user_lang(user_id)
    return TEXTS.get(lang, TEXTS["my"]).get(key, TEXTS["my"].get(key, key))

def is_authorized(user_id):
    if not ALLOWED_USER_IDS:  # ဗလာဆိုရင် အကုန်ခွင့်ပြု
        return True
    return user_id in ALLOWED_USER_IDS

# ============================================
# 📌 BASE COMMANDS
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    
    db.create_user(user_id)
    text = get_text(user_id, "start")
    keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    text = get_text(user_id, "help").format(MAX_BUTTONS)
    await update.message.reply_text(text, parse_mode="Markdown")

async def reset_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    db.clear_script_state(user_id)
    await update.message.reply_text(get_text(user_id, "reset"))

# ============================================
# 📌 CUSTOM BUTTON MAKER (Conversation)
# ============================================

async def new_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return ConversationHandler.END
    context.user_data["temp_buttons"] = []
    text = get_text(user_id, "new_button")
    await update.message.reply_text(text, parse_mode="Markdown")
    return WAITING_FOR_BUTTONS

async def receive_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return ConversationHandler.END
    
    message_text = update.message.text
    
    if message_text.startswith("/done"):
        buttons = context.user_data.get("temp_buttons", [])
        if not buttons:
            await update.message.reply_text(get_text(user_id, "no_buttons"))
            return WAITING_FOR_BUTTONS
        db.set_buttons(user_id, buttons)
        text = get_text(user_id, "done").format(len(buttons))
        await update.message.reply_text(text, parse_mode="Markdown")
        keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
        await update.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)
        return ConversationHandler.END
    
    if message_text.startswith("/cancel"):
        context.user_data.pop("temp_buttons", None)
        await update.message.reply_text(get_text(user_id, "cancel"))
        keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
        await update.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)
        return ConversationHandler.END
    
    pattern = r"^(.+?)\s*-\s*(.+)$"
    match = re.match(pattern, message_text)
    if not match:
        await update.message.reply_text(get_text(user_id, "invalid_format"))
        return WAITING_FOR_BUTTONS
    
    name = match.group(1).strip()
    url = match.group(2).strip()
    
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text("❌ လင့်ခ်က `http://` ဒါမှမဟုတ် `https://` နဲ့ စရပါမယ်။", parse_mode="Markdown")
        return WAITING_FOR_BUTTONS
    
    current_buttons = context.user_data.get("temp_buttons", [])
    if len(current_buttons) >= MAX_BUTTONS:
        await update.message.reply_text(get_text(user_id, "too_many_buttons").format(MAX_BUTTONS))
        return WAITING_FOR_BUTTONS
    
    current_buttons.append({"name": name, "url": url})
    context.user_data["temp_buttons"] = current_buttons
    await update.message.reply_text(
        get_text(user_id, "button_added").format(name, len(current_buttons), MAX_BUTTONS)
    )
    return WAITING_FOR_BUTTONS

async def view_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    buttons = db.get_buttons(user_id)
    if not buttons:
        await update.message.reply_text(get_text(user_id, "no_buttons"))
        return
    button_list = "\n".join([f"• {b['name']} → {b['url']}" for b in buttons])
    text = get_text(user_id, "view").format(button_list)
    await update.message.reply_text(text, parse_mode="Markdown")
    keyboard = create_button_row(buttons, columns=2)
    await update.message.reply_text("👇 ခင်ဗျားရဲ့ ခလုတ်တွေ", reply_markup=keyboard)

async def delete_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    await update.message.reply_text(get_text(user_id, "delete"))

async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    db.delete_buttons(user_id)
    await update.message.reply_text(get_text(user_id, "confirm_delete"))
    keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
    await update.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    text = get_text(user_id, "settings").format(MAX_BUTTONS)
    await update.message.reply_text(text, parse_mode="Markdown")

async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    text = get_text(user_id, "language")
    keyboard = [
        [InlineKeyboardButton("🇲🇲 မြန်မာ", callback_data="lang_my")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await query.edit_message_text(get_text(user_id, "not_authorized"))
        return
    lang = query.data.split("_")[1]
    db.set_user_lang(user_id, lang)
    lang_name = "မြန်မာ" if lang == "my" else "English"
    text = get_text(user_id, "language_changed").format(lang_name)
    await query.edit_message_text(text)
    keyboard = get_main_menu_keyboard(lang, TEXTS)
    await query.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    context.user_data.pop("temp_buttons", None)
    await update.message.reply_text(get_text(user_id, "cancel"))
    keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
    await update.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)

# ============================================
# 📌 MAIN MESSAGE PROCESSOR
# ============================================

async def process_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    
    message_text = update.message.text
    if not message_text:
        return

    script_state, script_data = db.get_script_state(user_id)
    
    # ---------- (၁) 'a' ကိုနှိပ်ခြင်း ----------
    if message_text.strip() == 'a':
        if script_state == 'ready':
            part1 = script_data.get('part1', '')
            part2 = script_data.get('part2', '')
            full_script = part1 + "\n\n" + part2
            
            title = full_script.split('\n')[0][:100] or "ဇာတ်ညွှန်း"
            html_content = format_content_to_html(full_script)
            telegraph_url = create_telegraph_page(title, html_content)
            
            if telegraph_url:
                db.set_script_state(user_id, 'active', {'script_url': telegraph_url})
                await update.message.reply_text(get_text(user_id, "script_telegraph_success"))
            else:
                db.set_script_state(user_id, 'active', {'script_text': full_script})
                await update.message.reply_text(get_text(user_id, "script_telegraph_failed"))
            return
        else:
            await update.message.reply_text(get_text(user_id, "script_not_ready"))
            return

    # ---------- (၂) Deep Link စစ်ဆေးခြင်း ----------
    link_pattern = r'(https?://t\.me/[^\s]+)\s+([^\s]+\.\w+)'
    link_match = re.search(link_pattern, message_text)
    
    if link_match:
        deep_link = link_match.group(1)
        filename = link_match.group(2)
        base_name = filename.rsplit('.', 1)[0]
        button_text = f"{base_name} ရယူရန်"
        
        keyboard = [[InlineKeyboardButton(button_text, url=deep_link)]]
        reply_text = get_text(user_id, "button_created").format(button_text, deep_link)
        
        # ဇာတ်ညွှန်းပါသလားစစ်
        if script_state == 'active':
            script_url = script_data.get('script_url')
            script_text = script_data.get('script_text')
            if script_url:
                keyboard.append([InlineKeyboardButton("📖 ဇာတ်ညွှန်းအပြည့်အစုံဖတ်ရန်", url=script_url)])
                reply_text += get_text(user_id, "script_attached")
            elif script_text:
                reply_text += f"\n\n📝 ဇာတ်ညွှန်း:\n{script_text[:500]}..."
                db.clear_script_state(user_id)  # ပြီးရင်ရှင်း
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode="Markdown")
        return

    # ---------- (၃) ဇာတ်ညွှန်း အပိုင်းများ စုဆောင်းခြင်း ----------
    if script_state == 'idle':
        db.set_script_state(user_id, 'part1_received', {'part1': message_text})
        await update.message.reply_text(get_text(user_id, "script_part1_received"))
        return
    
    elif script_state == 'part1_received':
        db.set_script_state(user_id, 'ready', {'part1': script_data.get('part1', ''), 'part2': message_text})
        await update.message.reply_text(get_text(user_id, "script_part2_received"))
        return
    
    elif script_state == 'active':
        await update.message.reply_text(get_text(user_id, "active_instruction"))
        return
    
    else:
        await update.message.reply_text(get_text(user_id, "unknown"))

# ============================================
# 📌 FILE HANDLER (ဖိုင်တင်လျှင် Deep Link ထုတ်ပေးမယ်)
# ============================================

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    
    # ဖိုင်အချက်အလက်ယူ
    document = update.message.document
    video = update.message.video
    audio = update.message.audio
    photo = update.message.photo
    
    file_name = None
    file_id = None
    
    if document:
        file_name = document.file_name or "file"
        file_id = document.file_id
    elif video:
        file_name = f"{video.file_name}" if video.file_name else "video.mp4"
        file_id = video.file_id
    elif audio:
        file_name = f"{audio.file_name}" if audio.file_name else "audio.mp3"
        file_id = audio.file_id
    elif photo:
        file_name = f"photo_{photo[-1].file_id[:8]}.jpg"
        file_id = photo[-1].file_id
    else:
        await update.message.reply_text("❌ ဒီဖိုင်အမျိုးအစားကို မထောက်ပံ့သေးပါဘူး။")
        return
    
    # Deep Link ဖန်တီး (ထူးခြားတဲ့ ID နဲ့)
    unique_id = str(uuid.uuid4())[:8]
    deep_link = f"https://t.me/{context.bot.username}?start=file_{unique_id}"
    
    # ဒေတာသိမ်းဆည်း (MongoDB)
    db.files.insert_one({
        "user_id": user_id,
        "file_id": file_id,
        "file_name": file_name,
        "unique_id": unique_id,
        "deep_link": deep_link,
        "created_at": update.message.date
    })
    
    # ခလုတ်ဖန်တီး
    button_text = f"{file_name} ရယူရန်"
    keyboard = [[InlineKeyboardButton(button_text, url=deep_link)]]
    
    # ဇာတ်ညွှန်းပါသလားစစ်
    script_state, script_data = db.get_script_state(user_id)
    if script_state == 'active':
        script_url = script_data.get('script_url')
        if script_url:
            keyboard.append([InlineKeyboardButton("📖 ဇာတ်ညွှန်းအပြည့်အစုံဖတ်ရန်", url=script_url)])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    reply_text = get_text(user_id, "file_deeplink_created").format(file_name, deep_link)
    await update.message.reply_text(reply_text, reply_markup=reply_markup, parse_mode="Markdown")

# ============================================
# 📌 START PAYLOAD HANDLER (Deep Link ကိုဖွင့်တဲ့အခါ)
# ============================================

async def deep_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text(get_text(user_id, "not_authorized"))
        return
    
    payload = context.args[0] if context.args else None
    if not payload:
        await start(update, context)
        return
    
    # file_ နဲ့စရင် file deep link
    if payload.startswith("file_"):
        unique_id = payload.replace("file_", "")
        file_data = db.files.find_one({"unique_id": unique_id})
        if file_data:
            # ဖိုင်ကို ပြန်ပို့ပေးမယ်
            file_id = file_data["file_id"]
            file_name = file_data["file_name"]
            await update.message.reply_document(
                document=file_id,
                filename=file_name,
                caption=f"📎 ခင်ဗျားတောင်းဆိုထားတဲ့ ဖိုင် - `{file_name}`",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ ဒီဖိုင်ကို ရှာမတွေ့ပါဘူး။")
    else:
        # ပုံမှန် start
        await start(update, context)

# ============================================
# 📌 CALLBACK HANDLER
# ============================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await query.edit_message_text(get_text(user_id, "not_authorized"))
        return
    
    data = query.data
    
    if data == "new":
        await new_buttons(update, context)
        text = get_text(user_id, "new_button")
        await query.edit_message_text(text, parse_mode="Markdown")
        return WAITING_FOR_BUTTONS
    
    elif data == "view":
        buttons = db.get_buttons(user_id)
        if not buttons:
            await query.edit_message_text(get_text(user_id, "no_buttons"))
            return
        button_list = "\n".join([f"• {b['name']} → {b['url']}" for b in buttons])
        text = get_text(user_id, "view").format(button_list)
        await query.edit_message_text(text, parse_mode="Markdown")
        keyboard = create_button_row(buttons, columns=2)
        await query.message.reply_text("👇 ခင်ဗျားရဲ့ ခလုတ်တွေ", reply_markup=keyboard)
    
    elif data == "delete":
        await query.edit_message_text(get_text(user_id, "delete"))
        await query.message.reply_text("/confirm_delete")
    
    elif data == "settings":
        text = get_text(user_id, "settings").format(MAX_BUTTONS)
        await query.edit_message_text(text, parse_mode="Markdown")
    
    elif data == "cancel":
        context.user_data.pop("temp_buttons", None)
        await query.edit_message_text(get_text(user_id, "cancel"))
        keyboard = get_main_menu_keyboard(db.get_user_lang(user_id), TEXTS)
        await query.message.reply_text("📌 ပင်မစာမျက်နှာ", reply_markup=keyboard)
