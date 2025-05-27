import numpy as np
import datetime
import json
import plotly.graph_objects as go
 
X1 = [1700, 1750, 1750, 2150]
X2 = [5, 10, 15, 20]
Y = [14.91, 14.18, 12.96, 10]

def Regresiya_analiz(X1=None, X2=None, Y=None,json_file_save=False,json_file_name="main1",grafik=False,grafik_file_name="main1.png"):
    start_time = datetime.datetime.now()

    x1 = np.array(X1)
    x2 = np.array(X2)
    y = np.array(Y)

    X = np.vstack([np.ones(len(x1)), x1, x2]).T

    beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ beta

    relative_errors = np.abs(y - y_pred) / y * 100
    mean_relative_error = np.mean(relative_errors)

    ss_total = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_total)

    results = {
        "coefficients": {
            "beta_0": round(float(beta[0]), 6),
            "beta_1": round(float(beta[1]), 6),
            "beta_2": round(float(beta[2]), 6)
        },
        "predictions": [
            {
                "x_1": round(float(x1[i]), 6),
                "x_2": round(float(x2[i]), 6),
                "y_actual": round(float(y[i]), 6),
                "y_predicted": round(float(y_pred[i]), 6),
                "relative_error_percent": round(float(relative_errors[i]), 6)
            } for i in range(len(y))
        ],
        "mean_relative_error_percent": round(float(mean_relative_error), 6),
        "r_squared": round(float(r_squared), 6),
        "execution_time": str(datetime.datetime.now() - start_time)
    }
    if json_file_save:
        with open(f'{json_file_name}.json', 'w') as f:
            json.dump(results, f, indent=4)
    # Plotly grafik
    if grafik:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=y,
            mode='lines+markers',
            name='Haqiqiy (Y)'
        ))
        fig.add_trace(go.Scatter(
            y=y_pred,
            mode='lines+markers',
            name='Bashorat (Ŷ)'
        ))

        fig.update_layout(
            title='Siqilish Mustahkamligi: Haqiqiy vs Bashorat',
            xaxis_title='Kuzatishlar',
            yaxis_title='Siqilish Mustahkamligi',
            legend=dict(x=0, y=1),
            template="plotly_white"
        )
        fig.write_html("main1.html")

    return results

if __name__ == "__main__":
    results = Regresiya_analiz(X1=X1, X2=X2, Y=Y,json_file_save=True,grafik=True)
    print("Regressiya koeffitsiyentlari:")
    print(f"β_0: {results['coefficients']['beta_0']}")
    print(f"β_1: {results['coefficients']['beta_1']}")
    print(f"β_2: {results['coefficients']['beta_2']}")
    print("\nKuzatishlar uchun natijalar:")
    for pred in results['predictions']:
        print(f"x_1: {pred['x_1']}, x_2: {pred['x_2']}, y_haqiqiy: {pred['y_actual']}, "
              f"y_taxminiy: {pred['y_predicted']:.6f}, nisbiy_xatolik: {pred['relative_error_percent']:.6f}%")
    print(f"\nO'rtacha nisbiy xatolik: {results['mean_relative_error_percent']:.6f}%")
    print(f"R^2 (Determinatsiya koeffitsiyenti): {results['r_squared']:.6f}")
    print(f"Hisoblash vaqti: {results['execution_time']}")
