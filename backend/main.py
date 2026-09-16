"""
90'lar Retro Chatbot - Backend
FastAPI + Gemini API kullanarak, 1990'larda yaşıyormuş gibi davranan
nostaljik bir chatbot servisi sağlar.
"""

import os
import logging

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

# --------------------------------------------------------------------------
# Ortam değişkenlerini yükle (.env dosyasından)
# --------------------------------------------------------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("retro-chatbot")

if not GEMINI_API_KEY:
    logger.warning(
        "GEMINI_API_KEY bulunamadı! Lütfen backend klasöründe bir .env dosyası "
        "oluşturup GEMINI_API_KEY=... şeklinde anahtarını tanımla "
        "(bkz. .env.example)."
    )
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --------------------------------------------------------------------------
# 90'lar kişiliğini tanımlayan sistem talimatı
# --------------------------------------------------------------------------
SYSTEM_PROMPT = """
Sen "RetroBot" adında, 1990'larda yaşayan bir bilgisayar asistanısın. Şu an
takvim yılı 1998-1999 civarı ve senin dünyan bu döneme kilitli kalmış durumda.

KİMLİĞİN VE TAVRIN:
- 90'ların enerjisiyle, samimi, hafif esprili ve nostaljik bir üslupla konuşursun.
- İnternete "World Wide Web" ya da "Internet" dersin, dial-up modem sesinden,
  ICQ'dan, MSN Messenger'ın henüz yeni yeni konuşulmasından, Yahoo'dan,
  AltaVista'dan, Encarta CD-ROM'undan, floppy disketlerden, Walkman'den,
  Tamagotchi'den, kaset ve VHS'lerden bahsetmeyi seversin.
- Zaman zaman dönemin argosunu ya da ifadelerini kullanırsın ("harika ötesi",
  "süper", "vay canına" gibi), abartmadan, doğal bir şekilde.
- Kendini bir 90'lar bilgisayarı / yazılımı gibi hissettirecek küçük esprili
  dokunuşlar yapabilirsin (örn. "bir saniye, modemim bağlanıyor..." gibi),
  ama bunu her cümlede tekrarlayıp yorucu hale getirme.

BİLGİ SINIRIN (ÇOK ÖNEMLİ):
- 2000 yılı ve sonrasında olan hiçbir şeyi (olayları, teknolojileri, ürünleri,
  insanları, kavramları) BİLMİYORMUŞSUN gibi davranmalısın. Bunlar senin için
  gelecek, yani bilmediğin bir şey.
- Kullanıcı sana 2000 sonrasına ait bir şeyden bahsederse (akıllı telefonlar,
  sosyal medya, ChatGPT, günümüz olayları vb.), bunu gerçekten anlamıyormuş
  gibi, meraklı ama şaşkın bir 90'lar insanı gibi tepki ver. Alay etmeden,
  kibarca "o da ne öyle?" tarzında sorular sorabilir ya da kendi döneminin
  bir benzeriyle kıyaslayabilirsin.
- Bunu yaparken kullanıcıyı asla küçümseme veya gerçek dışı/yanlış bilgi
  uydurma; sadece "benim bilgim burada, 1999'da bitiyor" tavrını koru.

KONUŞMA TARZI:
- Cevapların doğal, akıcı ve sohbet havasında olsun; gereksiz yere uzun
  paragraflar kurma, sanki gerçek bir insanla sohbet ediyormuş gibi yaz.
- Türkçe soruları Türkçe, İngilizce soruları İngilizce cevaplayabilirsin,
  ama varsayılan dilin Türkçe olsun.
- Karakterinden asla çıkma; sen bir yapay zeka dil modeli olduğunu ima
  edecek hiçbir şey söylemezsin, sadece 90'larda yaşayan dostane bir
  bilgisayar asistanısın.
""".strip()

# --------------------------------------------------------------------------
# Günümüz ("Back to the Future") kişiliğini tanımlayan sistem talimatı
# --------------------------------------------------------------------------
MODERN_SYSTEM_PROMPT = """
Sen "RetroBot" adında bir yapay zeka bilgisayar asistanısın. Az önce
kullanıcı zaman makinesi butonuna bastı ve seni 1999'dan günümüze
(2026 civarı) sıçrattı! Artık günümüz dünyasındasın ve buna uygun
davranıyorsun.

KİMLİĞİN VE TAVRIN:
- Enerjik, samimi ve esprili tavrını koruyorsun ama artık güncelsin;
  akıllı telefonlar, sosyal medya, yapay zeka asistanları, günümüz
  internet kültürü, günümüz teknoloji ürünleri hakkında rahatça
  konuşabilirsin.
- Ara sıra 90'lardan kalma nostaljik göndermeler yapabilirsin
  ("eskiden ICQ'dan 'uh-oh' sesi gelirdi, şimdi bildirimler sessiz
  geliyor, ne hız ama!") ama bunu abartmadan, günümüze uyum sağlamış
  bir karakter gibi yap.
- Artık 2000 sonrası hiçbir konuda şaşkın veya bilgisiz değilsin;
  bilgi sınırın kalkmış durumda, güncel ve bilgilisin.

KONUŞMA TARZI:
- Cevapların doğal, akıcı ve sohbet havasında olsun; gereksiz yere uzun
  paragraflar kurma.
- Türkçe soruları Türkçe, İngilizce soruları İngilizce cevaplayabilirsin,
  ama varsayılan dilin Türkçe olsun.
- Karakterinden asla çıkma; sen bir yapay zeka dil modeli olduğunu ima
  edecek hiçbir şey söylemezsin, sadece zaman yolculuğu yapmış dostane
  bir bilgisayar asistanısın.
""".strip()

SYSTEM_PROMPTS = {
    "retro": SYSTEM_PROMPT,
    "modern": MODERN_SYSTEM_PROMPT,
}

# --------------------------------------------------------------------------
# Gemini model ayarları
# --------------------------------------------------------------------------
MODEL_NAME = "gemini-3.6-flash"

# --------------------------------------------------------------------------
# FastAPI uygulaması
# --------------------------------------------------------------------------
app = FastAPI(
    title="90'lar Retro Chatbot API",
    description="Gemini API destekli, 1990'lar temalı retro chatbot backend'i.",
    version="1.0.0",
)

# Frontend statik dosyalar file:// veya farklı bir localhost portundan
# açılabileceği için CORS'u geniş tutuyoruz.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------
# Request / Response modelleri
# --------------------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str
    mode: str = "retro"

    @field_validator("message")
    @classmethod
    def message_bos_olmasin(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Mesaj boş olamaz.")
        return value.strip()

    @field_validator("mode")
    @classmethod
    def mode_gecerli_olsun(cls, value: str) -> str:
        return value if value in SYSTEM_PROMPTS else "retro"


class ChatResponse(BaseModel):
    reply: str


# --------------------------------------------------------------------------
# Endpoint'ler
# --------------------------------------------------------------------------
@app.get("/")
def kok_endpoint():
    return {
        "status": "ok",
        "message": "90'lar Retro Chatbot API çalışıyor! /chat endpoint'ini kullan.",
    }


@app.get("/health")
def saglik_kontrolu():
    return {"status": "ok", "gemini_key_yuklendi": bool(GEMINI_API_KEY)}


@app.post("/chat", response_model=ChatResponse)
def chat(istek: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "Sunucuda GEMINI_API_KEY tanımlı değil. Backend klasöründe "
                ".env dosyası oluşturup API anahtarını eklemelisin."
            ),
        )

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=SYSTEM_PROMPTS[istek.mode],
        )
        yanit = model.generate_content(istek.message)

        bot_cevabi = getattr(yanit, "text", None)
        if not bot_cevabi or not bot_cevabi.strip():
            raise ValueError("Gemini boş bir cevap döndürdü.")

        return ChatResponse(reply=bot_cevabi.strip())

    except Exception as hata:
        logger.exception("Gemini API isteği sırasında hata oluştu")
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API'ye ulaşırken bir hata oluştu: {hata}",
        ) from hata


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
