import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime, timedelta
import time
from telegram import Bot

# ==========================
# CONFIG
# ==========================
BOT_TOKEN = ""       # BotFather token
CHAT_ID = ""         # your group chat ID

# ==========================
# FETCH RANDOM QUOTE
# ==========================
def get_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except:
        return "Stay positive, work hard, and make it happen!"

# ==========================
# GENERATE IMAGE WITH QUOTE
# ==========================
def generate_image(quote):
    img = Image.new("RGB", (800, 400), color=(240, 240, 255))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    # Wrap text
    lines, line = [], ""
    for word in quote.split():
        if draw.textlength(line + word, font=font) < 700:
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    y_text = 100
    for line in lines:
        width = draw.textlength(line, font=font)
        draw.text(((800 - width) / 2, y_text), line, font=font, fill=(0, 0, 0))
        y_text += 40

    return img

# ==========================
# SEND TO TELEGRAM
# ==========================
async def send_quote():
    bot = Bot(token=BOT_TOKEN)
    quote = get_quote()
    img = generate_image(quote)
    bio = BytesIO()
    img.save(bio, "PNG")
    bio.seek(0)
    await bot.send_photo(chat_id=CHAT_ID, photo=bio, caption="🌞 Morning Motivation 🌞")
    print(f"✅ Quote sent at {datetime.now().strftime('%H:%M:%S')}")

# ==========================
# SCHEDULE DAILY 8:30 AM
# ==========================
async def scheduler():
    while True:
        now = datetime.now()
        next_run = now.replace(hour=8, minute=30, second=0, microsecond=0)
        if next_run < now:
            next_run += timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        print(f"⏳ Waiting {int(wait_seconds)} seconds until 8:30 AM...")
        await asyncio.sleep(wait_seconds)
        await send_quote()

# ==========================
# RUN
# ==========================
asyncio.run(scheduler())
