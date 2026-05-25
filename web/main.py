"""
Argos — Aplicación web de clasificación de imágenes
Actividad 4: Visión por Computador — La Salle 2026

Autores:
  - María Alejandra Gómez Piedrahita
  - Juan Manuel Castillo Pinto
"""

import os
import io
import base64
import logging
from datetime import datetime, timezone
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer, BadSignature
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

# ─── Configuración ────────────────────────────────────────────────────────────
APP_USERNAME   = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD   = os.getenv("APP_PASSWORD", "argos2026")
SECRET_KEY     = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
AWS_REGION     = os.getenv("AWS_REGION", "us-east-1")
MODEL_ARN      = os.getenv("MODEL_ARN", "")
MODEL_MAX_MIN  = int(os.getenv("MODEL_MAX_MINUTES", "60"))

# ─── Estado del modelo (en memoria) ──────────────────────────────────────────
model_started_at: Optional[datetime] = None

# ─── FastAPI + Jinja2 ─────────────────────────────────────────────────────────
app = FastAPI(title="Argos — Clasificador de Imágenes")
templates = Jinja2Templates(directory="templates")
serializer = URLSafeTimedSerializer(SECRET_KEY)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("argos")


# ─── AWS Helper ──────────────────────────────────────────────────────────────
def rekognition_client():
    return boto3.client("rekognition", region_name=AWS_REGION)


def get_model_status() -> str:
    """Retorna: RUNNING | STOPPED | STARTING | STOPPING | FAILED"""
    try:
        r = rekognition_client()
        project_arn = MODEL_ARN.rsplit("/version/", 1)[0]
        resp = r.describe_project_versions(
            ProjectArn=project_arn,
            VersionNames=[MODEL_ARN.split("/")[-2]]
        )
        versions = resp.get("ProjectVersionDescriptions", [])
        if not versions:
            return "STOPPED"
        return versions[0].get("Status", "STOPPED")
    except Exception as e:
        log.error(f"Error al consultar estado del modelo: {e}")
        return "UNKNOWN"


def start_model():
    global model_started_at
    try:
        r = rekognition_client()
        r.start_project_version(ProjectVersionArn=MODEL_ARN, MinInferenceUnits=1)
        model_started_at = datetime.now(timezone.utc)
        log.info("Modelo iniciado")
    except ClientError as e:
        log.error(f"Error al iniciar modelo: {e}")
        raise


def stop_model():
    global model_started_at
    try:
        r = rekognition_client()
        r.stop_project_version(ProjectVersionArn=MODEL_ARN)
        model_started_at = None
        log.info("Modelo detenido")
    except ClientError as e:
        log.error(f"Error al detener modelo: {e}")
        raise


# ─── Auto-apagado por seguridad ──────────────────────────────────────────────
def auto_shutoff_check():
    """Corre cada minuto. Apaga el modelo si lleva más de MODEL_MAX_MIN minutos."""
    global model_started_at
    if model_started_at is None:
        return
    elapsed = (datetime.now(timezone.utc) - model_started_at).total_seconds() / 60
    if elapsed >= MODEL_MAX_MIN:
        log.warning(f"Auto-apagado: modelo lleva {elapsed:.1f} min. Apagando...")
        try:
            stop_model()
        except Exception:
            pass


scheduler = BackgroundScheduler()
scheduler.add_job(auto_shutoff_check, "interval", minutes=1)
scheduler.start()


# ─── Auth helper ─────────────────────────────────────────────────────────────
SESSION_COOKIE = "argos_session"
SESSION_MAX_AGE = 60 * 60 * 8  # 8 horas


def create_session_token(username: str) -> str:
    return serializer.dumps(username)


def get_current_user(request: Request) -> Optional[str]:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    try:
        return serializer.loads(token, max_age=SESSION_MAX_AGE)
    except BadSignature:
        return None


def require_auth(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=302, headers={"Location": "/"})
    return user


# ─── Rutas ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if username == APP_USERNAME and password == APP_PASSWORD:
        token = create_session_token(username)
        response = RedirectResponse("/dashboard", status_code=303)
        response.set_cookie(
            SESSION_COOKIE, token,
            max_age=SESSION_MAX_AGE,
            httponly=True,
            samesite="lax"
        )
        return response
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": "Usuario o contraseña incorrectos"},
        status_code=401
    )


@app.get("/logout")
async def logout():
    response = RedirectResponse("/")
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse("/")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "max_minutes": MODEL_MAX_MIN,
    })


# ─── API: Estado del modelo ───────────────────────────────────────────────────

@app.get("/api/model/status")
async def api_model_status(request: Request):
    require_auth(request)
    status = get_model_status()
    minutes_on = None
    if model_started_at:
        minutes_on = round((datetime.now(timezone.utc) - model_started_at).total_seconds() / 60, 1)
    return JSONResponse({
        "status": status,
        "minutes_on": minutes_on,
        "max_minutes": MODEL_MAX_MIN,
    })


@app.post("/api/model/start")
async def api_model_start(request: Request):
    require_auth(request)
    try:
        start_model()
        return JSONResponse({"ok": True, "message": "Modelo iniciando..."})
    except Exception as e:
        return JSONResponse({"ok": False, "message": str(e)}, status_code=500)


@app.post("/api/model/stop")
async def api_model_stop(request: Request):
    require_auth(request)
    try:
        stop_model()
        return JSONResponse({"ok": True, "message": "Modelo detenido"})
    except Exception as e:
        return JSONResponse({"ok": False, "message": str(e)}, status_code=500)


# ─── API: Clasificar imagen ───────────────────────────────────────────────────

@app.post("/api/classify")
async def api_classify(request: Request, file: UploadFile = File(...)):
    require_auth(request)

    status = get_model_status()
    if status != "RUNNING":
        return JSONResponse(
            {"ok": False, "message": f"El modelo no está activo (estado: {status}). Inícialo primero."},
            status_code=400
        )

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        return JSONResponse({"ok": False, "message": "Imagen demasiado grande (máx 5 MB)"}, status_code=400)

    try:
        r = rekognition_client()
        resp = r.detect_custom_labels(
            ProjectVersionArn=MODEL_ARN,
            Image={"Bytes": contents},
            MinConfidence=30,
        )
        labels = sorted(resp.get("CustomLabels", []), key=lambda x: x["Confidence"], reverse=True)

        # Miniatura base64 para mostrar en UI
        thumbnail = base64.b64encode(contents).decode()
        ext = (file.content_type or "image/jpeg").split("/")[-1]

        return JSONResponse({
            "ok": True,
            "labels": [{"name": l["Name"], "confidence": round(l["Confidence"], 1)} for l in labels],
            "image_b64": f"data:{file.content_type};base64,{thumbnail}",
        })
    except Exception as e:
        return JSONResponse({"ok": False, "message": str(e)}, status_code=500)
