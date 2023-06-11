import os
import uvicorn
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

###################
# Settings
###################

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response

templates = Jinja2Templates(directory="web/client")
app.mount("/sample", StaticFiles(directory="web/client/sample"), name="static")

###################
# APIs
###################

# Healthcheck
@app.get("/healthcheck")
def healthcheck() -> bool:
    """Server health check."""
    return True

# pylint: disable=invalid-name,unused-argument
@app.get("/")
async def read_users(request: Request):
    context = {}
    context["request"] = request

    return templates.TemplateResponse("index.html", context)