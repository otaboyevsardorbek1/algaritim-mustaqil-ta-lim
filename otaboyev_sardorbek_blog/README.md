# 🧮 2D Nyuton-Rafson Metodi — Python + Plotly Vizualizatsiyasi

Bu loyiha ikki o‘zgaruvchili (x, y) tenglamalar sistemasini **Nyuton-Rafson usuli** yordamida iteratsion yechadi va natijalarni **interaktiv grafik** shaklida vizual tarzda taqdim etadi.

> Dastur matematikani kod bilan uyg‘unlashtirgan holda, foydalanuvchidan formulalarni kiritishni talab qiladi va hisoblash natijalarini grafik ko‘rinishida ko‘rsatadi.

---

## 🚀 Asosiy imkoniyatlar

- ✍️ Konsol orqali **f(x, y)** ko‘rinishida matematik tenglamalarni kiritish.
- ⚙️ Boshlang‘ich qiymatlar, aniqlik (epsilon) va maksimal iteratsiyalar sozlanadi.
- 📈 Iteratsiya davomida `x` va `y` qiymatlarining o‘zgarishini **Plotly** yordamida chizish.
- 💾 Natijalarni `iteratsiyalar.json` formatida saqlash.
- 🌐 Avtomatik ochiladigan HTML grafik: `newton_dinamik_grafik.html`.
- 🧠 Jakobi matritsasi **raqamli hosila** yordamida hisoblanadi (numerik differensial).

---

## 📂 Loyihaning fayl tuzilmasi

📦 NewtonVisualizer/
┣ 📄 newton_plot_app.py # Asosiy dastur kodi
┣ 📄 iteratsiyalar.json # Iteratsiya natijalari (avtomatik yaratiladi)
┣ 📄 newton_dinamik_grafik.html # Grafik vizualizatsiyasi (avtomatik yaratiladi)
┗ 📄 README.md # Ushbu fayl (tavsif hujjati)
---

## 🧰 O‘rnatish

Loyihani ishga tushirishdan oldin kerakli kutubxonalarni o‘rnating:

```bash
pip install numpy plotly
▶️ Ishlatish

python newton_plot_app.py
👇 Sizdan quyidagilar so‘raladi:
f1(x, y) funksiyasi: 1 - 0.5*np.cos(y) kabi.

f2(x, y) funksiyasi: np.sin(x + 1) - 1.2 kabi.

🔢 Dastur bajaradi:
Nyuton-Rafson iteratsiyasi.

Har bir bosqichdagi nuqtalarni yig‘adi.

Interpolatsiya asosida x-y grafigini chizadi.

Eng yaqin y ≈ 0 nuqtani aniqlaydi.

HTML grafikni avtomatik ochadi.

📊 Vizualizatsiya
Plotly interaktiv grafigida quyidagilar tasvirlanadi:

Element	Tavsifi
🔹 x qiymati	Har bir iteratsiyada x ning qiymati
🟢 y qiymati	Har bir iteratsiyada y ning qiymati
🟠 Interpolatsiya	Uzluksiz egri chiziq bilan x va y bog‘liqligi
⚫ y = 0 chizig‘i	Gorizontal nol chiziq
🔴 y ≈ 0 ga yaqin nuqta	Topilgan eng yaqin nuqta

Interaktiv grafik avtomatik ochiladi va HTML fayl sifatida saqlanadi.

🧠 Texnik tafsilotlar
Jakobi matritsasi raqamli differensial orqali (finite difference) hisoblanadi.

Funksiyalar eval() orqali dinamik ravishda kompilyatsiya qilinadi.

Iteratsiyalar epsilon qiymatidan kichik bo‘lsa — yaqinlashish deb qabul qilinadi.

Singular Jakobi matritsa holatlari aniqlanadi va foydalanuvchiga xabar beriladi.

📁 JSON natija formati
iteratsiyalar.json fayl quyidagi ko‘rinishda saqlanadi:
{
  "iterations": [
    {"iteration": 0, "x": 0.125, "y": 0.876},
    {"iteration": 1, "x": 0.231, "y": 0.754},
    ...
  ]
}
⚠️ E'tibor bering
eval() xavfsizligi: foydalanuvchi kiritgan ifoda Python sintaksisi asosida baholanadi. Faqat ishonchli muhitda ishlatish tavsiya etiladi.

np kutubxonasi funksiyalarda ishlatiladi (np.sin, np.cos, va h.k.).

Dastur faqat Python 3.x versiyasida ishlaydi.

👨‍💻 Muallif
Ismingizni bu yerga yozing
📧 Email: otaboyevsardorbek295@gmail.com
🔗 GitHub: github.com/otaboyevsardorbek1

📜 Litsenziya
Ushbu loyiha erkin foydalanish uchun taqdim etilgan. Istasangiz o‘zgartiring, tarqating yoki takomillashtiring.
---

### ✅ Foydalanish bo‘yicha eslatma:
Ushbu `README.md` faylini loyihangiz joylashgan papkaga nusxalab qo‘ying. GitHub sahifasida avtomatik ko‘rinadi.

Agar xohlasangiz, ushbu faylni `.md` formatda yuklab olish uchun tayyorlab bera olaman. Yuklab olishni xohlaysizmi?



