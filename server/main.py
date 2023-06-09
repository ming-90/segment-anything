import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from server.sam import SAMImageEncoder

from server.utils.logger import get_logger

###################
# Settings
###################

logger = get_logger()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configs = dict(
    checkpoint_path=os.path.join("checkpoint"),
    checkpoint_name="sam_vit_h_4b8939.pth",
    checkpoint_url="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
    model_type="default",
)

SAMImageEncoder(**configs)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response


###################
# APIs
###################

# Healthcheck
@app.get("/healthcheck")
def healthcheck() -> bool:
    """Server health check."""
    return True


# pylint: disable=invalid-name,unused-argument
@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request) -> Request:
    context = {}
    context["request"] = request

    return templates.TemplateResponse("index.html", context)

# pylint: disable=invalid-name,unused-argument
@app.get("/image-embedding", response_class=HTMLResponse)
async def image_embedding(request: Request) -> Request:
    context = {}
    context["request"] = request

    sam = SAMImageEncoder()

    return ""
