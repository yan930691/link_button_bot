# keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import MAX_BUTTONS

def create_button_row(buttons, columns=2):
    keyboard = []
    row = []
    for i, btn in enumerate(buttons):
        row.append(InlineKeyboardButton(btn["name"], url=btn["url"]))
        if (i + 1) % columns == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard(lang, texts):
    if lang == "my":
        keyboard = [
            [InlineKeyboardButton("📝 အသစ်ဖန်တီးမယ်", callback_data="new")],
            [InlineKeyboardButton("📋 ကြည့်မယ်", callback_data="view")],
            [InlineKeyboardButton("🗑️ ဖျက်မယ်", callback_data="delete")],
            [InlineKeyboardButton("⚙️ ဆက်တင်", callback_data="settings")],
            [InlineKeyboardButton("❌ ပယ်ဖျက်မယ်", callback_data="cancel")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("📝 Create New", callback_data="new")],
            [InlineKeyboardButton("📋 View", callback_data="view")],
            [InlineKeyboardButton("🗑️ Delete", callback_data="delete")],
            [InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")],
        ]
    return InlineKeyboardMarkup(keyboard)
