// ============================================================================
// RetroBot98 - Frontend Mantığı (Vanilla JS)
// ============================================================================

// Backend adresi. Yerelde ayrı bir portta çalışan FastAPI'ye, canlıda ise
// (Vercel) aynı origin'deki /api/chat serverless fonksiyonuna gider.
const YEREL_HOST = ["localhost", "127.0.0.1", ""].includes(location.hostname);
const API_URL = YEREL_HOST
  ? "http://127.0.0.1:8000/chat"
  : "/api/chat";

const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");
const typingName = document.getElementById("typing-name");
const titleText = document.getElementById("title-text");
const titleIcon = document.getElementById("title-icon");
const statusConnection = document.getElementById("status-connection");
const taskbarClock = document.getElementById("taskbar-clock");
const timeTravelBtn = document.getElementById("time-travel-btn");
const timeTravelIcon = document.getElementById("time-travel-icon");
const timeTravelLabel = document.getElementById("time-travel-label");

let istekGonderiliyor = false;

// ----------------------------------------------------------------------------
// Mod yönetimi: "retro" (90'lar) <-> "modern" (günümüz / Back to the Future)
// ----------------------------------------------------------------------------
let mod = "retro";

const MOD_AYARLARI = {
  retro: {
    botAdi: "RetroBot98",
    baslik: "RetroBot98.exe - 90'lar Sohbet Botu",
    baslikIkon: "💾",
    baglanti: "Bağlantı: 56K Modem 📞",
    buttonIkon: "🔮",
    buttonEtiket: "Back to the Future",
  },
  modern: {
    botAdi: "RetroBot",
    baslik: "RetroBot.exe - Günümüz Sohbet Botu",
    baslikIkon: "🤖",
    baglanti: "Bağlantı: Wi-Fi 6E ⚡",
    buttonIkon: "📼",
    buttonEtiket: "Back to the 90s",
  },
};

function botAdiniGuncelle() {
  const ad = MOD_AYARLARI[mod].botAdi;
  document.querySelectorAll(".bot-name-label").forEach((el) => {
    el.textContent = `${ad}:`;
  });
  typingName.textContent = ad;
}

function saatiGuncelle() {
  if (!taskbarClock) return;
  const simdi = new Date();
  const ss = String(simdi.getHours()).padStart(2, "0");
  const dd = String(simdi.getMinutes()).padStart(2, "0");
  taskbarClock.textContent = `${ss}:${dd}`;
}
setInterval(saatiGuncelle, 1000 * 15);
saatiGuncelle();

// ----------------------------------------------------------------------------
// Zaman makinesi sesi: geleceğe giderken yükselen, geçmişe giderken düşen bip
// ----------------------------------------------------------------------------
function zamanMakinesiSesiCal(gelecege) {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sawtooth";
    gain.gain.value = 0.05;
    osc.connect(gain);
    gain.connect(ctx.destination);
    const simdi = ctx.currentTime;
    if (gelecege) {
      osc.frequency.setValueAtTime(220, simdi);
      osc.frequency.exponentialRampToValueAtTime(1100, simdi + 0.5);
    } else {
      osc.frequency.setValueAtTime(1100, simdi);
      osc.frequency.exponentialRampToValueAtTime(220, simdi + 0.5);
    }
    osc.start(simdi);
    osc.stop(simdi + 0.5);
  } catch (e) {
    // Ses çalışmazsa sessizce yok say, kritik değil.
  }
}

// ----------------------------------------------------------------------------
// Retro <-> Modern modu arasında geçiş yapar
// ----------------------------------------------------------------------------
function modDegistir() {
  const gelecege = mod === "retro";
  mod = gelecege ? "modern" : "retro";
  const ayar = MOD_AYARLARI[mod];

  document.body.classList.toggle("theme-modern", mod === "modern");
  titleText.textContent = ayar.baslik;
  titleIcon.textContent = ayar.baslikIkon;
  statusConnection.textContent = ayar.baglanti;
  timeTravelIcon.textContent = ayar.buttonIkon;
  timeTravelLabel.textContent = ayar.buttonEtiket;
  botAdiniGuncelle();

  zamanMakinesiSesiCal(gelecege);

  mesajEkle(
    gelecege
      ? "⚡ Zaman makinesi devrede! Modem sesleri kesildi, ekran güncellendi... Artık günümüzdeyiz!"
      : "📼 Zaman makinesi geri sardı! Modem sesleri geri geldi, her şey 90'lara döndü...",
    "system"
  );
}

timeTravelBtn.addEventListener("click", modDegistir);

// ----------------------------------------------------------------------------
// Basit bir "retro tık" sesi hissi vermek için Web Audio API ile kısa bir bip
// ----------------------------------------------------------------------------
function retroBipCal() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "square";
    osc.frequency.value = 620;
    gain.gain.value = 0.04;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.06);
  } catch (e) {
    // Ses çalışmazsa sessizce yok say, kritik değil.
  }
}

// ----------------------------------------------------------------------------
// Ekrana yeni bir mesaj balonu ekler
// ----------------------------------------------------------------------------
function mesajEkle(metin, tip) {
  const mesajDiv = document.createElement("div");
  mesajDiv.className =
    tip === "user"
      ? "message user-message"
      : tip === "error"
      ? "message error-message"
      : tip === "system"
      ? "message system-message"
      : "message bot-message";

  const baslik = document.createElement("div");
  baslik.className =
    tip === "bot" ? "message-header bot-name-label" : "message-header";
  baslik.textContent =
    tip === "user"
      ? "Sen:"
      : tip === "error"
      ? "Sistem Hatası:"
      : tip === "system"
      ? "Sistem:"
      : `${MOD_AYARLARI[mod].botAdi}:`;

  const govde = document.createElement("div");
  govde.className = "message-text";
  govde.textContent = metin;

  mesajDiv.appendChild(baslik);
  mesajDiv.appendChild(govde);
  chatMessages.appendChild(mesajDiv);

  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ----------------------------------------------------------------------------
// "Yazıyor..." göstergesini aç/kapat
// ----------------------------------------------------------------------------
function yaziyorGoster(goster) {
  typingIndicator.style.display = goster ? "block" : "none";
  if (goster) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// ----------------------------------------------------------------------------
// Mesajı backend'e gönder ve cevabı ekrana bas
// ----------------------------------------------------------------------------
async function mesajGonder() {
  const mesaj = userInput.value.trim();

  if (!mesaj || istekGonderiliyor) {
    return;
  }

  retroBipCal();
  mesajEkle(mesaj, "user");
  userInput.value = "";
  userInput.focus();

  istekGonderiliyor = true;
  sendBtn.disabled = true;
  yaziyorGoster(true);

  try {
    const yanit = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: mesaj, mode: mod }),
    });

    const veri = await yanit.json().catch(() => null);

    if (!yanit.ok) {
      const hataMesaji =
        (veri && (veri.detail || veri.message)) ||
        `Sunucu ${yanit.status} koduyla cevap verdi.`;
      throw new Error(hataMesaji);
    }

    if (!veri || !veri.reply) {
      throw new Error("Sunucudan geçersiz bir cevap geldi.");
    }

    mesajEkle(veri.reply, "bot");
  } catch (hata) {
    console.error("Sohbet isteği başarısız oldu:", hata);
    mesajEkle(
      `Hop, bağlantı koptu galiba! 📴 (${hata.message}) ` +
        `Modemi kontrol edip tekrar dener misin?`,
      "error"
    );
  } finally {
    istekGonderiliyor = false;
    sendBtn.disabled = false;
    yaziyorGoster(false);
  }
}

// ----------------------------------------------------------------------------
// Olay dinleyicileri
// ----------------------------------------------------------------------------
sendBtn.addEventListener("click", mesajGonder);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    mesajGonder();
  }
});

userInput.focus();
