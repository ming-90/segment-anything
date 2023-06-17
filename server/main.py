import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from server.sam import SAMImageEncoder, SegmentationImageEmbeddingResponse

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
    # checkpoint_name="sam_vit_h_4b8939.pth",
    checkpoint_name="sam_hq_vit_l.pth",
    checkpoint_url="https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
    model_type="default",
)

sam_image_encoder = SAMImageEncoder(**configs)

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
@app.get("/image-embedding", response_model=SegmentationImageEmbeddingResponse)
async def image_embedding(
    file: UploadFile
) -> SegmentationImageEmbeddingResponse:
    logger.info("Create SAM image embedding.")
    try:
        sam = await sam_image_encoder.run(file)
    except Exception as e:
        logger.error(e)

    return SegmentationImageEmbeddingResponse(**sam)
