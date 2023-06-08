from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


# pylint: disable=invalid-name,unused-argument
def create_app() -> FastAPI:
    """Create a fastapi app instance."""

    app_instance = FastAPI()

    origins = ["*"]
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app_instance

app = create_app()

# Healthcheck
@app.get("/healthcheck")
def healthcheck() -> bool:
    """Server health check."""
    return True

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response


# pylint: disable=invalid-name,unused-argument
@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request) -> Request:
    context = {}
    context["request"] = request

    return templates.TemplateResponse("index.html", context)
