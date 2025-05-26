import numpy as np
import datetime
import json
 
# Ushbu kod suvning siqilish mustahkamligi va qo'shimcha ma'lumotlar asosida
X1=[1700, 1750, 1750, 2150]
X2=[5, 10, 15, 20]
Y=[14.91, 14.18, 12.96, 10]
# Ushbu kod suvning siqilish mustahkamligi va qo'shimcha ma'lumotlar asosida
# chiziqli regressiya tahlilini amalga oshiradi va natijalarni JSON formatida saqlaydi.
def linear_regression_analysis(X1=None, X2=None, Y=None):
    # Hisoblash boshlanish vaqti
    start_time = datetime.datetime.now()
    
    # 1-jadval ma'lumotlari
    x1 = np.array(X1)  # suv
    x2 = np.array(X2)          # qo'shimcha
    y = np.array(Y) # siqilish mustahkamligi
    
    # X matritsasini shakllantirish (birinchi ustun 1 lar, sababi β_0 uchun)
    X = np.vstack([np.ones(len(x1)), x1, x2]).T
    # β = (X^T X)^(-1) X^T y
    beta = np.linalg.inv(X.T @ X) @ X.T @ y
     
    # Regressiya tenglamasi y(x_1, x_2) = β_0 + β_1*x_1 + β_2*x_2
    y_pred = X @ beta
    
    # Nisbiy xatolikni hisoblash: A_i = |y - y_pred| / y * 100%
    relative_errors = np.abs(y - y_pred) / y * 100
    mean_relative_error = np.mean(relative_errors)
    
    # Natijalarni JSON formatida saqlash uchun tayyorlash
    results = {
        "coefficients": {
            "beta_0": round(float(beta[0]), 6),
            "beta_1": round(float(beta[1]),6),
            "beta_2": round(float(beta[2]),6),
            "beta_3": round(float(beta[3]),6),
            "beta_4": round(float(beta[4]),6)
        },
        "predictions": [
            {
                "x_1":round( float(x1[i]),6),
                "x_2": round(float(x2[i]),6),
                "y_actual":round(float(y[i]),6),
                "y_predicted": round(float(y_pred[i]),6),
                "relative_error_percent":round(float(relative_errors[i]),6)
            } for i in range(len(y))
        ],
        "mean_relative_error_percent": round(float(mean_relative_error),6),
        "execution_time": str(datetime.datetime.now() - start_time)
    }
    
    # JSON faylga saqlash
    with open('regression_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    return results

# Funksiyani ishga tushirish
if __name__ == "__main__":
    results = linear_regression_analysis(X1=X1,X2=X2,Y=Y)
    print("Regressiya koeffitsiyentlari:")
    print(f"β_0: {results['coefficients']['beta_0']}")
    print(f"β_1: {results['coefficients']['beta_1']}")
    print(f"β_2: {results['coefficients']['beta_2']}")
    print("\nKuzatishlar uchun natijalar:")
    for pred in results['predictions']:
        print(f"x_1: {pred['x_1']}, x_2: {pred['x_2']}, y_haqiqiy: {pred['y_actual']}, "
              f"y_taxminiy: {pred['y_predicted']:.6f}, nisbiy_xatolik: {pred['relative_error_percent']:.6f}%")
    print(f"\nO'rtacha nisbiy xatolik: {results['mean_relative_error_percent']:.6f}%")
    print(f"Hisoblash vaqti: {results['execution_time']}")