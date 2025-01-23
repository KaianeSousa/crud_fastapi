from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from app.database import engine
from app.models import Base
from app.routes import doadores, recebedores, doacoes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/doadores", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("doadores.html", {"request": request})

@app.get("/recebedores", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("recebedores.html", {"request": request})

app.include_router(doadores.router, prefix="/doadores")
app.include_router(recebedores.router, prefix="/recebedores")
app.include_router(doacoes.router, prefix="/doacoes")
