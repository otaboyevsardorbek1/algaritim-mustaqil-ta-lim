from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objects as go
import datetime

app = Flask(__name__)

def Regresiya_analiz(X1, X2, Y):
    start_time = datetime.datetime.now()

    x1 = np.array(X1, dtype=float)
    x2 = np.array(X2, dtype=float)
    y = np.array(Y, dtype=float)

    X = np.vstack([np.ones(len(x1)), x1, x2]).T
    beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ beta

    relative_errors = np.abs(y - y_pred) / y * 100
    mean_relative_error = np.mean(relative_errors)

    ss_total = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum((y - y_pred) ** 2)
    r_squared = 1 - (ss_res / ss_total)

    # Grafikni saqlash
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y, mode='lines+markers', name='Haqiqiy (Y)'))
    fig.add_trace(go.Scatter(y=y_pred, mode='lines+markers', name='Bashorat (Ŷ)'))
    fig.update_layout(
        title='Siqilish Mustahkamligi: Haqiqiy vs Bashorat',
        xaxis_title='Kuzatishlar',
        yaxis_title='Siqilish Mustahkamligi',
        template="plotly_white"
    )
    fig.write_html("static/main1.html")

    predictions = [
        {
            "x_1": round(float(x1[i]), 2),
            "x_2": round(float(x2[i]), 2),
            "y_actual": round(float(y[i]), 2),
            "y_predicted": round(float(y_pred[i]), 2),
            "relative_error": round(float(relative_errors[i]), 2)
        }
        for i in range(len(y))
    ]

    return {
        "coefficients": {
            "beta_0": round(float(beta[0]), 4),
            "beta_1": round(float(beta[1]), 4),
            "beta_2": round(float(beta[2]), 4)
        },
        "predictions": predictions,
        "mean_relative_error": round(float(mean_relative_error), 2),
        "r_squared": round(float(r_squared), 4),
        "execution_time": str(datetime.datetime.now() - start_time)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Formadan olingan qiymatlarni o'qish
            x1_raw = request.form.get('x1', '')
            x2_raw = request.form.get('x2', '')
            y_raw = request.form.get('y', '')

            # Har bir satrni vergul orqali ajratamiz va tozalaymiz
            x1 = [float(i.strip()) for i in x1_raw.split(',') if i.strip()]
            x2 = [float(i.strip()) for i in x2_raw.split(',') if i.strip()]
            y = [float(i.strip()) for i in y_raw.split(',') if i.strip()]

            if len(x1) == len(x2) == len(y) and len(x1) >= 2:
                results = Regresiya_analiz(x1, x2, y)
                return render_template('result.html', results=results)
            else:
                error = "Har bir ro‘yxat uzunligi bir xil bo‘lishi va kamida 2 ta element bo‘lishi kerak!"
                return render_template('index.html', error=error)

        except Exception as e:
            return render_template('index.html', error=f"Xatolik: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
