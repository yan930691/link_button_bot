# telegraph_utils.py
import requests

TELEGRAPH_API = "https://api.telegraph.com"

def create_telegraph_page(title, content):
    try:
        account = requests.post(
            f"{TELEGRAPH_API}/createAccount",
            json={"short_name": "LinkBot", "author_name": "Link Button Bot"}
        ).json()
        
        if not account.get("ok", False):
            return None
        
        access_token = account["result"]["access_token"]
        
        response = requests.post(
            f"{TELEGRAPH_API}/createPage",
            json={
                "access_token": access_token,
                "title": title[:256],
                "content": content,
                "return_content": False,
            }
        ).json()
        
        if response.get("ok", False):
            return response["result"]["url"]
        return None
    except Exception as e:
        print(f"Telegraph error: {e}")
        return None

def format_content_to_html(text):
    paragraphs = text.split("\n\n")
    # ✅ f-string အတွင်းမှာ backslash ကို တိုက်ရိုက်မသုံးဘဲ variable နဲ့ သုံးပါ
    newline = "\n"
    html = "".join([f"<p>{p.replace(newline, '<br>')}</p>" for p in paragraphs if p.strip()])
    return html
