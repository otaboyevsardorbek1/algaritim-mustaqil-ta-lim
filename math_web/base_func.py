import os
import numpy as np
import math
import time
# APP JSON FILE PATH 
current_dir = os.getcwd()
final_dir = os.path.join(current_dir, 'Data')

# kesh faylillarni o`chirish uchun funqsiya
def clean_old_files(directory, age_limit_seconds=300):
    os.makedirs(directory, exist_ok=True)  # Papka mavjud bo‘lmasa yaratadi

    now = time.time()
    for filename in os.listdir(directory):
        file_path_full = os.path.join(directory, filename)
        if os.path.isfile(file_path_full):
            file_age = now - os.path.getmtime(file_path_full)
            if file_age > age_limit_seconds:
                try:
                    os.remove(file_path_full)
                except Exception:
                    return

                
def periodic_cleaner(interval_seconds=60):
    while True:
        clean_old_files(directory='Data', age_limit_seconds=86400) 
        time.sleep(interval_seconds)

# JSON fayl saqlanadigan yo'l
def file_path(filename):
    directory = os.path.join(os.path.dirname(__file__), 'Data')
    os.makedirs(directory, exist_ok=True)  # Yo‘lni yaratadi agar mavjud bo'lmasa
    return os.path.join(directory, filename)

# nuyuton itaratsiya funqsiylari
def is_valid_number(val): # KIRITILGAN STR ICHIDAGI RASMLARNI BOS YO`QLINI TESHKIISH`
    return isinstance(val, (int, float)) and not (np.isnan(val) or np.isinf(val))

# Foydalanuvchi ifodasini lambda funksiyaga aylantirish
def parse_to_lambda(expr):
    return eval(f"lambda x, y: {expr}", {"np": np, "__builtins__": {}})

# Jacobian matritsasini hisoblash (numerik hosilalar)
def numerical_jacobian(f1, f2, x0, y0, h=1e-5):
    df1_dx = (f1(x0 + h, y0) - f1(x0 - h, y0)) / (2 * h)
    df1_dy = (f1(x0, y0 + h) - f1(x0, y0 - h)) / (2 * h)
    df2_dx = (f2(x0 + h, y0) - f2(x0 - h, y0)) / (2 * h)
    df2_dy = (f2(x0, y0 + h) - f2(x0, y0 - h)) / (2 * h)
    return np.array([[df1_dx, df1_dy], [df2_dx, df2_dy]])

# Nyuton-Rafson usuli FUNQSIYASI
def newton_raphson(func1_str, func2_str, start_x, start_y, epsilon, max_iter=100):
    func1 = parse_to_lambda(func1_str)
    func2 = parse_to_lambda(func2_str)

    x0, y0 = start_x, start_y
    results = []

    for k in range(max_iter):
        f_val = np.array([func1(x0, y0), func2(x0, y0)])
        J = numerical_jacobian(func1, func2, x0, y0)

        try:
            delta = np.linalg.solve(J, -f_val)
        except np.linalg.LinAlgError:
            results.append({"error": "Jacobian singular (yechib bo'lmaydi)"})
            break

        x1, y1 = x0 + delta[0], y0 + delta[1]
         # ⚠️ NaN, Inf yoki noto'g'ri qiymat chiqsa, to'xtatamiz
        if not is_valid_number(x1) or not is_valid_number(y1):
            results.append({
                "error": f"Natijada yaroqsiz qiymat chiqdi: x={x1}, y={y1}"
            })
            break
        
        results.append({
            'iteration': k,
            'x': round(x1, 6),
            'y': round(y1, 6),
            'f1(x, y)': round(f_val[0], 6),
            'f2(x, y)': round(f_val[1], 6)
        })

        if np.linalg.norm([x1 - x0, y1 - y0]) < epsilon:
            break

        x0, y0 = x1, y1

    return results
# nuyuton itaratsiya funqsiyalari yakuni

# Formatlash funksiyasi: f(x,y)=C ko’rinishini g(x,y) = o'zgaruvchi qiymat sifatida yozish
def preprocess_expression(expr):
    if "=" in expr:
        lhs, rhs = expr.split("=")
        return f"({rhs})"  # Biz faqat ifodaning o'ng tarafini hisoblaymiz
    return expr

# ODDIY ITARATSIYA USULI UCHUN FUNQSIYA
def iterate_values(func1, func2, start_x, start_y, epsilon, max_iter=100):
    results = []
    k = 0
    x0 = start_x
    y0 = start_y

    func1 = preprocess_expression(func1)
    func2 = preprocess_expression(func2)

    while k < max_iter:
        local_dict = {'x': x0, 'y': y0, 'np': np, 'math': math}
        try:
            x1 = eval(func1, {"__builtins__": {}}, local_dict)
            y1 = eval(func2, {"__builtins__": {}}, local_dict)
        except Exception as e:
            results.append({"error": f"Xatolik: {e}"})
            break

        # ⚠️ NaN, Inf yoki noto'g'ri qiymat chiqsa, to'xtatamiz
        if not is_valid_number(x1) or not is_valid_number(y1):
            results.append({
                "error": f"Natijada yaroqsiz qiymat chiqdi: x={x1}, y={y1}"
            })
            break

        results.append({
            'iteration': k,
            'x': round(x1, 6),
            'y': round(y1, 6)
        })

        if abs(x1 - x0) + abs(y1 - y0) < epsilon:
            break

        x0, y0 = x1, y1
        k += 1

    return results
