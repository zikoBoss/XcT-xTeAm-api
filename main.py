import asyncio
import ssl
import logging
from datetime import datetime
import os

import aiohttp
from fastapi import FastAPI, Query, HTTPException
import uvicorn

from xC4 import (
    OpEnSq, cHSq, SEnd_InV, ExiT, GeneRaTePk, CrEaTe_ProTo,
    Ua, EnC_PacKeT, DecodE_HeX
)

# ================== إعدادات ==================
FF_UID = "4378068850"
FF_PASSWORD = "8C583277F6A0221993BAC8FBBD712BC25B171A445A34FB1DD0966609CB74729D"
API_KEY = "yakoubpy"

online_writer = None
whisper_writer = None
key = None
iv = None
region = None

app = FastAPI(title="FPI Squad API")
logging.basicConfig(level=logging.INFO)

# ================== دوال الاتصال (مبسطة) ==================
async def GeNeRaTeAccEss(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": await Ua(),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid, "password": password, "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as resp:
            if resp.status != 200: return None, None
            data = await resp.json()
            return data.get("open_id"), data.get("access_token")

async def encrypted_proto(encoded_hex):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    cipher = AES.new(b'Yg&tc%DEuh6%Zc^8', AES.MODE_CBC, b'6oyZDr22E3ychjM%')
    return cipher.encrypt(pad(encoded_hex, AES.block_size))

async def EncRypTMajoRLoGin(open_id, access_token):
    from Pb2 import MajoRLoGinrEq_pb2
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.123.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    headers = {
        'User-Agent': await Ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Expect': '100-continue',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB53',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_ctx) as resp:
            return await resp.read() if resp.status == 200 else None

async def DecRypTMajoRLoGin(response):
    from Pb2 import MajoRLoGinrEs_pb2
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(response)
    return proto

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': await Ua(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Expect': '100-continue',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB53',
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers, ssl=ssl_ctx) as resp:
            return await resp.read() if resp.status == 200 else None

async def DecRypTLoGinDaTa(data):
    from Pb2 import PorTs_pb2
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(data)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def SEndPacKeT(typE, packet):
    global online_writer
    if typE == 'OnLine' and online_writer:
        online_writer.write(packet)
        await online_writer.drain()

async def login_to_freefire():
    global key, iv, region, online_writer, whisper_writer
    try:
        open_id, access_token = await GeNeRaTeAccEss(FF_UID, FF_PASSWORD)
        if not open_id: return False
        payload = await EncRypTMajoRLoGin(open_id, access_token)
        response = await MajorLogin(payload)
        if not response: return False
        login_res = await DecRypTMajoRLoGin(response)
        url = login_res.url
        region = login_res.region
        token = login_res.token
        bot_uid = login_res.account_uid
        key = login_res.key
        iv = login_res.iv
        timestamp = login_res.timestamp

        login_data = await GetLoginData(url, payload, token)
        if not login_data: return False
        login_dec = await DecRypTLoGinDaTa(login_data)

        online_ip, online_port = login_dec.Online_IP_Port.split(":")
        chat_ip, chat_port = login_dec.AccountIP_Port.split(":")
        auth_token = await xAuThSTarTuP(int(bot_uid), token, int(timestamp), key, iv)

        async def run_online():
            global online_writer
            while True:
                try:
                    reader, writer = await asyncio.open_connection(online_ip, int(online_port))
                    online_writer = writer
                    writer.write(bytes.fromhex(auth_token))
                    await writer.drain()
                    while True:
                        data = await reader.read(4096)
                        if not data: break
                except:
                    await asyncio.sleep(5)

        async def run_chat():
            global whisper_writer
            while True:
                try:
                    reader, writer = await asyncio.open_connection(chat_ip, int(chat_port))
                    whisper_writer = writer
                    writer.write(bytes.fromhex(auth_token))
                    await writer.drain()
                    while True:
                        data = await reader.read(4096)
                        if not data: break
                except:
                    await asyncio.sleep(5)

        asyncio.create_task(run_online())
        asyncio.create_task(run_chat())
        await asyncio.sleep(5)
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False

async def cmd_3(uid: int):
    try:
        PAc = await OpEnSq(key, iv, region)
        await SEndPacKeT('OnLine', PAc)
        await asyncio.sleep(0.3)
        C = await cHSq(3, uid, key, iv, region)
        await SEndPacKeT('OnLine', C)
        V = await SEnd_InV(3, uid, key, iv, region)
        await SEndPacKeT('OnLine', V)
        await asyncio.sleep(2)
        E = await ExiT(None, key, iv)
        await SEndPacKeT('OnLine', E)
        return True
    except Exception as e:
        logging.error(f"cmd_3 error: {e}")
        return False

async def cmd_5(uid: int):
    try:
        PAc = await OpEnSq(key, iv, region)
        await SEndPacKeT('OnLine', PAc)
        await asyncio.sleep(0.3)
        C = await cHSq(5, uid, key, iv, region)
        await SEndPacKeT('OnLine', C)
        V = await SEnd_InV(5, uid, key, iv, region)
        await SEndPacKeT('OnLine', V)
        await asyncio.sleep(2)
        E = await ExiT(None, key, iv)
        await SEndPacKeT('OnLine', E)
        return True
    except Exception as e:
        logging.error(f"cmd_5 error: {e}")
        return False

async def cmd_6(uid: int):
    try:
        PAc = await OpEnSq(key, iv, region)
        await SEndPacKeT('OnLine', PAc)
        await asyncio.sleep(0.3)
        C = await cHSq(6, uid, key, iv, region)
        await SEndPacKeT('OnLine', C)
        V = await SEnd_InV(6, uid, key, iv, region)
        await SEndPacKeT('OnLine', V)
        await asyncio.sleep(2)
        E = await ExiT(None, key, iv)
        await SEndPacKeT('OnLine', E)
        return True
    except Exception as e:
        logging.error(f"cmd_6 error: {e}")
        return False

@app.on_event("startup")
async def startup():
    logging.info("جاري تسجيل الدخول إلى فري فاير...")
    if not await login_to_freefire():
        logging.error("فشل الاتصال باللعبة!")
    else:
        logging.info("تم الاتصال بنجاح.")

@app.get("/3")
async def squad_3(uid: int = Query(..., description="UID الهدف"), api_key: str = Query("")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="مفتاح API غير صحيح")
    success = await cmd_3(uid)
    return {"status": "success" if success else "failed", "uid": uid, "squad": 3}

@app.get("/5")
async def squad_5(uid: int = Query(..., description="UID الهدف"), api_key: str = Query("")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="مفتاح API غير صحيح")
    success = await cmd_5(uid)
    return {"status": "success" if success else "failed", "uid": uid, "squad": 5}

@app.get("/6")
async def squad_6(uid: int = Query(..., description="UID الهدف"), api_key: str = Query("")):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="مفتاح API غير صحيح")
    success = await cmd_6(uid)
    return {"status": "success" if success else "failed", "uid": uid, "squad": 6}

@app.get("/health")
async def health():
    return {"status": "ok", "connected": online_writer is not None}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)