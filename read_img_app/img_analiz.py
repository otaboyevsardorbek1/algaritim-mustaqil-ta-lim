from PIL import Image
import pytesseract
import sympy as sp
import re

# Tesseract OCR yo'lini ko'rsatish
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 📌 C++ dagi matematik funksiyalarni tanib olish uchun context
sympy_locals = {
    'exp': sp.exp,
    'sqrt': sp.sqrt,
    'log': sp.log,
    'log10': lambda x: sp.log(x, 10),
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'abs': sp.Abs,
    'pow': sp.Pow,
}

# 📷 Rasm orqali matn olish
def get_text_from_image(img_path):
    try:
        image = Image.open(img_path)
        raw_text = pytesseract.image_to_string(image, lang='eng')
        return raw_text
    except Exception as e:
        print(f"❌ Rasmni o‘qishda xatolik: {e}")
        return ""

# 🧹 Matnni tozalash
def clean_expression(text):
    text = text.replace('\x0c', '')
    return re.sub(r'[^0-9a-zA-Z\+\-\*/\^\.\(\)=xXyY\s]', '', text).strip()

# 🧠 Matnda matematik ifoda borligini aniqlash
def contains_math_expression(text):
    return bool(re.search(r'[0-9xXyYzZ\+\-\*/\^\=\(\)]', text))

# 🧮 O‘zgaruvchilarni aniqlash
def extract_variables(expr_str):
    try:
        expr = sp.sympify(expr_str, locals=sympy_locals)
        return sorted(expr.free_symbols, key=lambda s: str(s))
    except Exception as e:
        print(f"❌ O‘zgaruvchilarni aniqlashda xatolik: {e}")
        return []

# 🔎 Ifodani tahlil qilish
def analyze_and_compute(expr_str, var_limits):
    try:
        expr = sp.sympify(expr_str, locals=sympy_locals)
        simplified = sp.simplify(expr)
        derivatives = {str(v): sp.diff(expr, v) for v in expr.free_symbols}
        integrals = {}
        values = {}

        for var, (a, b) in var_limits.items():
            symbolic_var = sp.Symbol(var)
            integrals[var] = sp.integrate(expr, (symbolic_var, a, b))
            values[var] = expr.subs(symbolic_var, b)

        return {
            "original": expr,
            "simplified": simplified,
            "derivatives": derivatives,
            "integrals": integrals,
            "values_at_endpoints": values
        }
    except Exception as e:
        print(f"❌ Hisoblashda xatolik: {e}")
        return {}

# ▶️ Asosiy menyu
def main():
    print("📌 Matematik ifoda tahlil dasturiga xush kelibsiz!")
    print("1. 📷 Rasm orqali ifoda yuklash")
    print("2. ⌨️  Qo‘lda ifoda kiritish")
    tanlov = input("Tanlovingizni kiriting (1/2): ").strip()

    if tanlov == '1':
        img_path = input("Rasmning to‘liq yo‘lini kiriting: ").strip()
        raw_text = get_text_from_image(img_path)

        if not contains_math_expression(raw_text):
            print("❗ Rasmda matematik ifoda aniqlanmadi. Iltimos, boshqa rasm yuklang.")
            return

        print(f"📝 OCR topgan ifoda: {raw_text}")
        confirm = input("Bu ifoda to‘g‘rimi? (ha/yo‘q): ").strip().lower()
        if confirm != 'ha':
            print("❗ Iltimos, to‘g‘ri rasmni yuboring.")
            return

        cleaned = clean_expression(raw_text)

    elif tanlov == '2':
        raw_text = input("Ifodani kiriting: ")
        cleaned = clean_expression(raw_text)

    else:
        print("❌ Noto‘g‘ri tanlov.")
        return

    print(f"\n🔎 Tozalangan ifoda: {cleaned}")

    variables = extract_variables(cleaned)
    if not variables:
        print("❌ O‘zgaruvchilar topilmadi.")
        return

    var_limits = {}
    for var in variables:
        try:
            a = float(input(f"🔢 {var} uchun boshlang‘ich qiymat (a): "))
            b = float(input(f"🔢 {var} uchun yakuniy qiymat (b): "))
            var_limits[str(var)] = (a, b)
        except:
            print(f"❌ {var} uchun noto‘g‘ri kiritma.")
            return

    result = analyze_and_compute(cleaned, var_limits)
    if result:
        print(f"\n📈 Original:        {result['original']}")
        print(f"♻️ Soddalashtirilgan: {result['simplified']}")
        for var, deriv in result['derivatives'].items():
            print(f"🔺 Hosila ({var}):     {deriv}")
        for var, integ in result['integrals'].items():
            print(f"🔻 Integral ({var}):   {integ}")
        for var, val in result['values_at_endpoints'].items():
            print(f"📊 {var}=b uchun qiymat: {val}")
        
        qiymatlar = list(result['values_at_endpoints'].values())
        print(f"\n📥 Natijaviy massiv: {qiymatlar}")
    else:
        print("❌ Tahlil muvaffaqiyatsiz.")

if __name__ == "__main__":
    main()
