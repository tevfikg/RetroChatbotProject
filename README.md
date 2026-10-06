https://retro-chatbot-project.vercel.app/

# RetroBot98 — 90'lar Temalı Retro Chatbot

Kullanıcıyla sanki 1990'larda yaşıyormuş gibi sohbet eden, Gemini API
destekli, Windows 95/98 görünümlü nostaljik bir chatbot uygulaması.

- **Backend:** Python + FastAPI + Google Gemini API (`google-generativeai`)
- **Frontend:** Sade HTML + CSS + Vanilla JavaScript (framework yok)

---

## 📁 Proje Yapısı

```
RetroChatbotProject/
├── backend/
│   ├── main.py            # FastAPI uygulaması ve /chat endpoint'i
│   ├── requirements.txt   # Python bağımlılıkları
│   ├── .env.example       # Ortam değişkeni şablonu
│   └── .env               # (senin oluşturacağın, gerçek API anahtarını içerir)
├── frontend/
│   ├── index.html         # Windows 95/98 görünümlü sohbet penceresi
│   ├── style.css          # Retro Windows estetiği stilleri
│   └── script.js          # Backend ile haberleşen JS mantığı
└── README.md
```

---

## 1) Ön Gereksinimler

- Python 3.9 veya üzeri
- Ücretsiz bir **Gemini API anahtarı**
  (https://aistudio.google.com/app/apikey adresinden "Get API key" ile
  saniyeler içinde alabilirsin)

---

## 2) Backend Kurulumu

### a. Sanal ortam oluştur (önerilir)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### b. Bağımlılıkları kur

```bash
pip install -r requirements.txt
```

### c. `.env` dosyanı oluştur

`backend/.env.example` dosyasını kopyalayıp `backend/.env` adıyla kaydet,
içine kendi Gemini API anahtarını yapıştır:

```bash
cp .env.example .env
```

`.env` dosyasının içeriği şöyle görünmeli:

```
GEMINI_API_KEY=senin_gercek_api_anahtarin
```

⚠️ `.env` dosyasını **asla** paylaşma veya versiyon kontrolüne (git) ekleme.

### d. Backend'i çalıştır

```bash
python main.py
```

veya

```bash
uvicorn main:app --reload
```

Backend başarıyla ayağa kalkarsa terminalde şuna benzer bir çıktı görürsün:

```
Uvicorn running on http://0.0.0.0:8000
```

Tarayıcıdan `http://127.0.0.1:8000` adresine gidip
`{"status":"ok", ...}` cevabını görerek backend'in çalıştığını
doğrulayabilirsin.

---

## 3) Frontend'i Çalıştırma

Frontend tamamen statik dosyalardan oluşuyor, herhangi bir build adımı
gerekmiyor. İki seçeneğin var:

### Seçenek A — Doğrudan tarayıcıda aç

`frontend/index.html` dosyasına çift tıklayıp tarayıcıda açman yeterli.

### Seçenek B — Basit bir yerel sunucu ile aç (önerilir)

Bazı tarayıcılar `file://` üzerinden `fetch` isteklerinde kısıtlama
uygulayabilir, bu yüzden küçük bir yerel sunucu üzerinden açmak daha
güvenlidir:

```bash
cd frontend
python3 -m http.server 5500
```

Ardından tarayıcıdan `http://127.0.0.1:5500` adresine git.

---

## 4) Kullanım

1. Backend'in (`http://127.0.0.1:8000`) çalıştığından emin ol.
2. Frontend'i tarayıcıda aç.
3. Alt kısımdaki metin kutusuna bir mesaj yaz, Enter'a bas ya da
   "Gönder ▶" butonuna tıkla.
4. RetroBot98, 90'ların ruhuyla sana cevap versin! 📼

---

## 5) Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|---|---|
| "Modemim bağlanamadı" tarzı hata mesajı | Backend'in çalıştığından ve `script.js` içindeki `API_URL` adresinin doğru olduğundan emin ol. |
| `GEMINI_API_KEY tanımlı değil` hatası | `backend/.env` dosyasının var olduğundan ve içinde geçerli bir anahtar olduğundan emin ol, backend'i yeniden başlat. |
| CORS hatası | Backend zaten tüm origin'lere izin verecek şekilde ayarlı; yine de sorun yaşarsan frontend'i `file://` yerine yerel bir sunucu üzerinden (Seçenek B) açmayı dene. |
| Gemini API'den hata dönüyor | API anahtarının geçerli ve aktif olduğunu, ücretsiz kotanın dolmadığını kontrol et. |

---

## 6) Notlar

- Bot, sistem talimatı (`SYSTEM_PROMPT`) sayesinde kendini 1990'ların
  sonlarında yaşıyormuş gibi tanıtır ve 2000 sonrası konulara şaşkın/meraklı
  bir tavırla yaklaşır.
- API anahtarı hiçbir zaman kod içine yazılmaz; yalnızca `.env` dosyasından
  okunur (`python-dotenv` ile).
- Tasarım, klasik Windows 95/98 penceresini taklit eder: mavi gradient
  başlık çubuğu, kabartmalı (beveled) butonlar, inset giriş alanı ve retro
  bir durum çubuğu içerir.
