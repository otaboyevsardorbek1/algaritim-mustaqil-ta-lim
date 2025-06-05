from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from regresiya import Regressiya_3D_data,Regresiya_analiz_2D

app = FastAPI()

# Statik fayllarni (grafiklar) ochish uchun
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates uchun
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/hisobla", response_class=HTMLResponse)
async def hisobla(
    request: Request,
    x1: str = Form(...),
    x2: str = Form(...),
    y: str = Form(...),
    tur: str = Form(...)
):
    # Matnni listga aylantiramiz
    X1 = [float(i.strip()) for i in x1.split(',')]
    X2 = [float(i.strip()) for i in x2.split(',')]
    Y = [float(i.strip()) for i in y.split(',')]

    if tur == "2D":
        result = await Regresiya_analiz_2D(X1, X2, Y)
    else:
        result = await Regressiya_3D_data(X1, X2, Y, save_data_html=True)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "natija": result,
        "tur": tur
    })

# run cammand python -m uvicorn main:app --reload
