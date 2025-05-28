import numpy as np
import datetime
import json
import plotly.graph_objects as go
import uuid
from pathlib import Path

# regresiya 3D ma'lumotlarini tahlil qilish funksiyasi
async def Regressiya_3D_data(X1=None, X2=None, Y=None,save_data_json=False,save_data_html=False):

    start_time = datetime.datetime.now()
    x1 = np.array(X1)
    x2 = np.array(X2)
    y = np.array(Y)

    # Regressiya uchun X matritsa
    X = np.vstack([np.ones(len(x1)), x1, x2]).T
    beta, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
    y_pred = X @ beta

    # Statistika
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
    if save_data_json:
        # JSON faylini saqlash
        file_name = f'regression_results_{uuid.uuid4().hex}.json'
        file_path = Path('data') / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)
        
    if save_data_html:
        fig = go.Figure()

        # Haqiqiy nuqtalar
        fig.add_trace(go.Scatter3d(
            x=x1,
            y=x2,
            z=y,
            mode='markers',
            marker=dict(size=6, color='blue'),
            name='Haqiqiy nuqtalar'
        ))

        # Yuzani (regression plane) chizish
        x1_grid, x2_grid = np.meshgrid(
            np.linspace(min(x1), max(x1), 10),
            np.linspace(min(x2), max(x2), 10)
        )
        z_grid = beta[0] + beta[1] * x1_grid + beta[2] * x2_grid

        fig.add_trace(go.Surface(
            x=x1_grid,
            y=x2_grid,
            z=z_grid,
            colorscale='Viridis',
            name='Regression yuzasi',
            opacity=0.6
        ))

        fig.update_layout(
            scene=dict(
                xaxis_title='X1 (modda hajmi)',
                yaxis_title='X2 (qo\'shimcha)',
                zaxis_title='Y (siqilish mustahkamligi)'
            ),
            title='3D Regressiya modeli: Haqiqiy nuqtalar + model yuzasi',
            margin=dict(l=0, r=0, b=0, t=0)
        )
        graph_filename = f"static/{uuid.uuid4().hex}.html"
        Path("static").mkdir(exist_ok=True)
        fig.write_html(graph_filename)

    return results



# regressiya tahlil qilish funksiyasi 2d 
async def Regresiya_analiz_2D(X1=None, X2=None, Y=None):
    start_time = datetime.datetime.now()
    if X1 is None or X2 is None or Y is None:
        return {"error": "X1, X2, and Y must be provided"}
    if len(X1) != len(X2) or len(X1) != len(Y):
        return {"error": "X1, X2, and Y must have the same length"}
    if (len(X1) < 3 or len(X2) < 3 or len(Y) < 3):
        return {"error": "At least 3 data points are required for regression analysis"}
    # Ma'lumotlarni numpy massivlariga aylantirish

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
    graph_filename = f"static/{uuid.uuid4().hex}.html"
    Path("static").mkdir(exist_ok=True)
    fig.write_html(graph_filename)

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
        "graph_filename": graph_filename,
        "execution_time": str(datetime.datetime.now() - start_time)
    }