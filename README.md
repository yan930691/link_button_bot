# link_button_bot
# Link Button Maker Bot (MongoDB + Web Service)

Telegram အတွက် လင့်ခ်ခလုတ်များ ဖန်တီးပေးတဲ့ Bot (MongoDB နဲ့ချိတ်ဆက်ထား)

## ✨ အင်္ဂါရပ်များ

- 🎬 **ဇာတ်ညွှန်း ၂ပိုင်း** ပို့ပြီး `a` နှိပ်ကာ Telegraph မှာ တင်နိုင်တယ်
- 🔗 **Deep Link** ကို အလိုအလျောက် ခလုတ်ဖြစ်အောင် ဖန်တီးပေးတယ်
- 📎 **ဖိုင်တင်လျှင်** Deep Link အလိုအလျောက်ထုတ်ပေးတယ်
- 📝 **ကိုယ်တိုင်ခလုတ်** ဖန်တီးနိုင်တယ် (အများဆုံး ၁၀၀ ခု)
- 🌐 **မြန်မာလို** အပြည့်အစုံ အသုံးပြုလို့ရတယ်
- 🗄️ **MongoDB** နဲ့ ချိတ်ဆက်ထားပြီး ဒေတာများကို သိမ်းဆည်းထားတယ်
- 🔐 **ခွင့်ပြုထားတဲ့သူများသာ** သုံးလို့ရအောင် လုပ်ထားတယ်

## 🚀 တည်ဆောက်နည်း (Render Web Service)

### ၁။ MongoDB Database ပြင်ဆင်ပါ
- MongoDB Atlas မှာ အခမဲ့ Cluster တစ်ခုဖန်တီးပါ
- Connection URI ကို ရယူပါ (mongodb+srv://...)

### ၂။ Render မှာ Deploy လုပ်ပါ
1. Render မှာ **New Web Service** ကိုရွေးပါ
2. GitHub Repository ကိုချိတ်ပါ
3. **Settings** -
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
4. **Environment Variables** အောက်မှာ ထည့်ပါ -
   - `BOT_TOKEN` = ခင်ဗျားရဲ့ Bot Token
   - `MONGO_URI` = MongoDB Connection URI
   - `DATABASE_NAME` = link_button_bot (သို့) ကြိုက်တဲ့အမည်
5. **Create Web Service** ကိုနှိပ်ပါ

## 📖 အသုံးပြုနည်း

### 🎬 ဇာတ်ညွှန်းတင်နည်း
1. ဇာတ်ညွှန်း အပိုင်း (၁/၂) ပို့ပါ
2. ဇာတ်ညွှန်း အပိုင်း (၂/၂) ပို့ပါ
3. `a` ကိုနှိပ်ပြီး Telegraph မှာ တင်ပါ

### 🔗 Deep Link ခလုတ်ဖန်တီးနည်း
အောက်ပါပုံစံအတိုင်း ပို့ပါ -
