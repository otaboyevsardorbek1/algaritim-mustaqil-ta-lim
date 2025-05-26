from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, txt="CV: Otaboyev Sardorbek", ln=True, align="C")

# Shaxsiy ma'lumotlar
pdf.set_font("Arial", size=12)
pdf.ln(10)
pdf.cell(200, 10, txt="Manzil: Toshkent, O‘zbekiston", ln=True)
pdf.cell(200, 10, txt="Telefon: (Telefon raqamingiz)", ln=True)
pdf.cell(200, 10, txt="Email: (Email manzilingiz)", ln=True)
pdf.cell(200, 10, txt="Telegram: @otaboyev_sardorbek_blog_dev", ln=True)
pdf.cell(200, 10, txt="GitHub: github.com/otaboyevsardorbek1", ln=True)

# Maqsad
pdf.ln(10)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Maqsad", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "Backend dasturchisi sifatida Django, Python, MongoDB, MySQL va SQLite3 texnologiyalarida ishlashni davom ettirish va o‘z ko‘nikmalarimni rivojlantirish.")

# Ko'nikmalar
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Ko‘nikmalar", ln=True)
pdf.set_font("Arial", size=12)
skills = [
    "Python, JavaScript",
    "HTML, CSS",
    "Django",
    "MongoDB, MySQL, SQLite3",
    "Git, GitHub"
]
for skill in skills:
    pdf.cell(200, 10, txt="- " + skill, ln=True)

# Loyihalar
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Muhim loyihalar", ln=True)
pdf.set_font("Arial", size=12)
projects = [
    "BotInlineShop - Telegram bot orqali onlayn do‘kon yaratish.",
    "airavata-django-portal - Apache Airavata portalini fork qilish.",
    "Automated-Penetration-Testing-Framework - Penetratsion test tizimi.",
    "bot - Aiogram yordamida kurs yaratish.",
    "Constructor-Telegram-Bots - Django asosida bot konstruktori.",
    "django-bot-misol - Django asosida bot misollar."
]
for p in projects:
    pdf.multi_cell(0, 10, "- " + p)

# Tajriba
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Tajriba", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "PRODEV MCHJ | Backend dasturchi | Toshkent | (Ishlagan yilingiz)\nDjango asosida backend tizimlarini ishlab chiqish va qo‘llab-quvvatlash.")

# Ta'lim
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Ta'lim", ln=True)
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, "(O‘qigan oliy o‘quv yurti) | (Yo‘nalish) | (O‘qish yillari) | (Daraja)")

# Tillar
pdf.ln(5)
pdf.set_font("Arial", 'B', 14)
pdf.cell(200, 10, txt="Til bilimi", ln=True)
pdf.set_font("Arial", size=12)
langs = [
    "O‘zbek tili: Ona tili",
    "Rus tili: (Bilish darajasi)",
    "Ingliz tili: (Bilish darajasi)"
]
for lang in langs:
    pdf.cell(200, 10, txt="- " + lang, ln=True)

# Faylni saqlash
pdf.output("Otaboyev_Sardorbek_CV.pdf")
