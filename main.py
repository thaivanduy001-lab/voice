import discord
import asyncio
import os
from threading import Thread
from flask import Flask

# Web server giữ Render luôn hoạt động
app = Flask(__name__)

@app.route('/')
def home():
    return "Voice Bot 24/7 dang hoat dong!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

t = Thread(target=run_web)
t.start()

# === ĐIỀN ID KÊNH VOICE BẠN MUỐN TREO VÀO ĐÂY ===
VOICE_CHANNEL_ID = 1417884212249493638  # Thay ID kênh voice của bạn vào đây

client = discord.Client()

@client.event
async def on_ready():
    print(f"=== DA DANG NHAP VOICE BOT: {client.user} ===")
    client.loop.create_task(keep_voice_connected())

async def keep_voice_connected():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            # Kiểm tra xem bot đã vào kênh voice chưa
            if not client.voice_clients:
                channel = client.get_channel(VOICE_CHANNEL_ID) or await client.fetch_channel(VOICE_CHANNEL_ID)
                if channel:
                    await channel.connect(reconnect=True, timeout=30.0)
                    print(f"[VOICE] Da ket noi vao kenh: {channel.name}")
            else:
                # Nếu đã vào nhưng bị rớt kết nối
                for vc in client.voice_clients:
                    if not vc.is_connected():
                        await vc.disconnect()
        except Exception as e:
            print(f"[VOICE LOI]: {e}")
        
        # Kiểm tra lại trạng thái mỗi 30 giây
        await asyncio.sleep(30)

client.run(os.getenv('DISCORD_TOKEN'))
