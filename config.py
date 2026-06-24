# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # .env ဖိုင်ကနေ load လုပ်မယ်

# Telegram Bot Token (Render Environment Variable ကနေ ယူမယ်)
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# MongoDB Connection URI
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "link_button_bot")

# ခလုတ်အများဆုံးအရေအတွက် (Telegram ကန့်သတ်ချက် = 100)
MAX_BUTTONS = 100

# ခွင့်ပြုထားတဲ့ သုံးစွဲသူ ID (ခင်ဗျားတစ်ယောက်တည်းသုံးချင်ရင် ဒီမှာထည့်ပါ)
ALLOWED_USER_IDS = [123456789]  # ခင်ဗျားရဲ့ Telegram User ID ထည့်ပါ (အကုန်သုံးချင်ရင် [] ဗလာထားပါ)

# ============================================
# 📝 ဘာသာပြန်ဆိုမှုများ (မြန်မာ)
# ============================================
TEXTS = {
    "my": {
        "start": "👋 ကြိုဆိုပါတယ်။\n\nကျွန်တော်က **Link Button Maker Bot** ပါ။\n\n📌 အသုံးပြုနည်း -\n၁။ ဇာတ်ညွှန်း အပိုင်း (၁/၂) ပို့ပါ။\n၂။ ဇာတ်ညွှန်း အပိုင်း (၂/၂) ပို့ပါ။\n၃။ `a` ကိုနှိပ်ပြီး Telegraph မှာ တင်ပါ။\n၄။ လင့်ခ်နဲ့ ဖိုင်နာမည်ကို ပို့ပါ။\n\n📎 ဖိုင်တစ်ခုပို့ရင်လည်း Deep Link အလိုအလျောက်ထုတ်ပေးမယ်။\n\n🔧 /help - အသေးစိတ်ကြည့်ရန်",
        
        "help": "📖 **အသုံးပြုနည်း အပြည့်အစုံ**\n\n📌 **ဇာတ်ညွှန်း (Script) ပို့နည်း**\n၁။ ဇာတ်ညွှန်း အပိုင်း (၁/၂) ကို ပို့ပါ။\n၂။ ဇာတ်ညွှန်း အပိုင်း (၂/၂) ကို ပို့ပါ။\n၃။ `a` ကိုနှိပ်ပြီး Telegraph မှာ တင်ပါ။\n\n📌 **Deep Link ခလုတ်ဖန်တီးနည်း**\n၄။ အောက်ပါပုံစံအတိုင်း ပို့ပါ -\n`https://t.me/... ဖိုင်နာမည်.mp4`\n\n📌 **ဖိုင်တင်ခြင်းဖြင့် Deep Link ထုတ်နည်း**\n- ဗီဒီယို/စာရွက်စာတမ်း ဖိုင်တစ်ခုခုကို Bot ဆီပို့လိုက်ရုံပါပဲ။\n- Bot က အလိုအလျောက် Deep Link ကို ဖန်တီးပေးမယ်။\n\n📌 **ကိုယ်တိုင်ခလုတ်ဖန်တီးနည်း**\n/new ကိုနှိပ်ပြီး `အမည် - လင့်ခ်` ပုံစံဖြင့် ရိုက်ထည့်ပါ။\n\n📌 အခြား Command များ\n/view - ခလုတ်များကြည့်ရန်\n/delete - ခလုတ်အားလုံးဖျက်ရန်\n/settings - ဆက်တင်များ\n/reset - ဇာတ်ညွှန်းသိမ်းဆည်းမှုရှင်းရန်\n\n📌 ခလုတ်အများဆုံး: {} ခု",
        
        "new_button": "✏️ ခလုတ်အသစ်ဖန်တီးမယ်\n\nခလုတ်အမည်နဲ့ လင့်ခ်ကို အောက်ပါပုံစံအတိုင်း တစ်ကြောင်းချင်းစီ ရိုက်ထည့်ပါ။\n\n`ခလုတ်အမည် - လင့်ခ်`\n\nဥပမာ:\n`YouTube - https://youtube.com`\n`Facebook - https://facebook.com`\n\nအကုန်ရိုက်ပြီးရင် /done ကိုနှိပ်ပါ။\nပယ်ဖျက်ရန် /cancel",
        
        "done": "✅ ခလုတ်များကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။\n\nခလုတ် {} ခု ဖန်တီးထားပါတယ်။\n\n/view ဖြင့် ကြည့်ရှုပါ။",
        
        "view": "📋 **ခင်ဗျားရဲ့ ခလုတ်များ**\n\n{}\n\n/new - အသစ်ထပ်ဖန်တီးရန်\n/delete - အားလုံးဖျက်ရန်",
        
        "delete": "🗑️ ခလုတ်အားလုံးကို ဖျက်မှာသေချာလား?\n\n/confirm_delete ကိုနှိပ်ပြီး အတည်ပြုပါ။",
        
        "confirm_delete": "✅ ခလုတ်အားလုံးကို ဖျက်လိုက်ပါပြီ။",
        
        "settings": "⚙️ **ဆက်တင်များ**\n\n🌐 ဘာသာစကား: မြန်မာ\n📌 ခလုတ်အများဆုံး: {}\n📎 ဖိုင်တင်လျှင် Deep Link ထုတ်ပေးမယ်။\n\n🔁 ပြောင်းလဲလိုပါက /language ကိုနှိပ်ပါ။",
        
        "language": "🌐 ဘာသာစကားရွေးချယ်ပါ:\n\n/myanmar - မြန်မာ\n/english - English",
        
        "language_changed": "✅ ဘာသာစကားကို {} သို့ ပြောင်းလိုက်ပါပြီ။",
        
        "no_buttons": "❌ ခင်ဗျားမှာ ခလုတ်တွေ မရှိသေးပါဘူး။ /new နဲ့ အသစ်ဖန်တီးပါ။",
        
        "invalid_format": "❌ ပုံစံမှားနေပါတယ်။\n\n`ခလုတ်အမည် - လင့်ခ်` ဆိုတဲ့ပုံစံမှန်အောင် ရိုက်ထည့်ပါ။",
        
        "too_many_buttons": "❌ ခလုတ်အရေအတွက် {} ခုထက် မပိုရပါဘူး။",
        
        "button_added": "✅ '{}' ခလုတ်ကို ထည့်လိုက်ပါပြီ။ ({} / {})",
        
        "cancel": "❌ လုပ်ဆောင်မှုကို ဖျက်သိမ်းလိုက်ပါပြီ။",
        
        "reset": "🔄 ဇာတ်ညွှန်း သိမ်းဆည်းထားမှုအားလုံးကို ရှင်းလင်းလိုက်ပါပြီ။\n\nဇာတ်ညွှန်းအသစ်အတွက် ပြန်ပို့ပါ။",
        
        "script_part1_received": "✅ ဇာတ်ညွှန်း အပိုင်း (၁/၂) ကိုလက်ခံရရှိပါပြီ။\n\nဇာတ်ညွှန်း အပိုင်း (၂/၂) ကို ဆက်လက်ပို့ပါ။",
        
        "script_part2_received": "✅ ဇာတ်ညွှန်း အပိုင်း (၂/၂) ကိုလက်ခံရရှိပါပြီ။\n\nလင့်ခ်များမပို့မီ `a` ကိုနှိပ်ပြီး အဆင်သင့်ဖြစ်ကြောင်း အတည်ပြုပါ။",
        
        "script_telegraph_success": "✅ ဇာတ်ညွှန်းကို Telegraph မှာ တင်ပြီးပါပြီ။\n\nအခု လင့်ခ်များကို စတင်ပို့ပါ။\n(ဇာတ်ညွှန်းခလုတ် အလိုအလျောက် ပါလာမည်)",
        
        "script_telegraph_failed": "⚠️ Telegraph တင်ရန် အမှားဖြစ်သွားတယ်။\nစာသားအတိုင်း ထည့်ပေးလိုက်မယ်။\n\nလင့်ခ်များ စတင်ပို့ပါ။",
        
        "script_not_ready": "❌ ဇာတ်ညွှန်း အပိုင်း (၂/၂) ကို မရသေးပါဘူး။\nဇာတ်ညွှန်းကို အရင်ပို့ပါ။",
        
        "button_created": "✅ သင့်အတွက် ခလုတ်ကို ဖန်တီးပေးလိုက်ပါပြီ။\n\n📌 နာမည်: `{}`\n🔗 လင့်ခ်: {}",
        
        "script_attached": "\n\n📝 ဇာတ်ညွှန်းကိုလည်း ပါရှိပါတယ်။",
        
        "active_instruction": "ℹ️ ဇာတ်ညွှန်းအဆင်သင့်ဖြစ်နေပါပြီ။\nလင့်ခ်များကို ပို့ပေးပါ။\n(သို့မဟုတ် ဇာတ်ညွှန်းအသစ်အတွက် /reset ကိုနှိပ်ပါ)",
        
        "unknown": "❓ နားမလည်လို့ပါ။ /start ကိုနှိပ်ပြီး ပြန်စပါ။",
        
        "file_deeplink_created": "✅ ဖိုင်အတွက် Deep Link ကို ဖန်တီးပေးလိုက်ပါပြီ။\n\n📌 ဖိုင်နာမည်: `{}`\n🔗 Deep Link: {}",
        
        "not_authorized": "⛔ ခင်ဗျားကို ဒီ Bot သုံးခွင့်မရှိပါဘူး။"
    },
    "en": {
        "start": "👋 Welcome!\n\nI am **Link Button Maker Bot**.\n\n📌 How to use -\n1. Send script part (1/2).\n2. Send script part (2/2).\n3. Type `a` to upload to Telegraph.\n4. Send links with filenames.\n\n📎 Send any file to auto-generate Deep Link.\n\n🔧 /help - Details",
        
        "help": "📖 **Full Usage Guide**\n\n📌 **Script Upload**\n1. Send script part (1/2).\n2. Send script part (2/2).\n3. Type `a` to confirm & upload to Telegraph.\n\n📌 **Deep Link Button**\n4. Send in this format:\n`https://t.me/... filename.mp4`\n\n📌 **File Upload for Deep Link**\n- Send any file (video/document) to bot.\n- Bot auto-generates Deep Link for you.\n\n📌 **Custom Button Maker**\n/new - Create custom buttons\nFormat: `Name - Link`\n\n📌 Other Commands\n/view - View buttons\n/delete - Delete all buttons\n/settings - Settings\n/reset - Clear script data\n\n📌 Max buttons: {}",
        
        "new_button": "✏️ Creating new buttons\n\nEnter button names and links line by line.\n\n`Button Name - Link`\n\nExample:\n`YouTube - https://youtube.com`\n`Facebook - https://facebook.com`\n\nClick /done when finished.\nCancel: /cancel",
        
        "done": "✅ Buttons saved successfully.\n\n{} buttons created.\n\nView: /view",
        
        "view": "📋 **Your Buttons**\n\n{}\n\nNew: /new\nDelete: /delete",
        
        "delete": "🗑️ Delete all buttons? Click /confirm_delete",
        
        "confirm_delete": "✅ All buttons deleted.",
        
        "settings": "⚙️ **Settings**\n\n🌐 Language: English\n📌 Max Buttons: {}\n📎 File upload auto-generates Deep Link.\n\nChange: /language",
        
        "language": "🌐 Choose language:\n\n/myanmar - မြန်မာ\n/english - English",
        
        "language_changed": "✅ Language changed to {}.",
        
        "no_buttons": "❌ You have no buttons yet. Use /new to create.",
        
        "invalid_format": "❌ Invalid format.\n\nUse: `Button Name - Link`",
        
        "too_many_buttons": "❌ Cannot exceed {} buttons.",
        
        "button_added": "✅ '{}' added. ({} / {})",
        
        "cancel": "❌ Cancelled.",
        
        "reset": "🔄 Script data cleared.\n\nSend new script.",
        
        "script_part1_received": "✅ Script part (1/2) received.\n\nSend script part (2/2).",
        
        "script_part2_received": "✅ Script part (2/2) received.\n\nType `a` to confirm before sending links.",
        
        "script_telegraph_success": "✅ Script uploaded to Telegraph.\n\nNow send your links.\n(Script button will auto-attach)",
        
        "script_telegraph_failed": "⚠️ Telegraph upload failed. Will send as text.\n\nNow send your links.",
        
        "script_not_ready": "❌ Script part (2/2) not received yet.\nSend script first.",
        
        "button_created": "✅ Button created for you.\n\n📌 Name: `{}`\n🔗 Link: {}",
        
        "script_attached": "\n\n📝 Script is also attached.",
        
        "active_instruction": "ℹ️ Script is ready.\nSend your links.\n(Or /reset for new script)",
        
        "unknown": "❓ I don't understand. Use /start to begin.",
        
        "file_deeplink_created": "✅ Deep Link created for file.\n\n📌 Filename: `{}`\n🔗 Deep Link: {}",
        
        "not_authorized": "⛔ You are not authorized to use this bot."
    }
}
