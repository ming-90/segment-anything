import os
import urllib
import base64

import torch
import cv2
import numpy as np

from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import Dict, Any, Tuple
from server.utils.logger import get_logger
from segment_anything import sam_model_registry

logger = get_logger()


###################
# Model
###################

EmbeddingShape = Tuple[int, int, int, int]
class SegmentationImageEmbeddingResponse(BaseModel):
    """ML Inference Response model."""

    image_embedding: str = Field(..., description="Image Embedding")
    image_embedding_shape: EmbeddingShape = Field(..., example=[1, 256, 64, 64])

###################
# SAM Encoder Class
###################

class SAMImageEncoder():
    def __init__(
            self, checkpoint_path, checkpoint_name, checkpoint_url, model_type
        ) -> None:
        logger.info("Initialize SAMImageEncoder.")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if not os.path.exists(checkpoint_path):
            os.makedirs(checkpoint_path, exist_ok=True)
        checkpoint = os.path.join(checkpoint_path, checkpoint_name)
        if not os.path.exists(checkpoint):
            urllib.request.urlretrieve(checkpoint_url, checkpoint)
        self.model = sam_model_registry[model_type](checkpoint=checkpoint).to(
            self.device
        )
        logger.info("Complete to initialize SAMImageEncoder.")

    async def run(self, inputs: UploadFile) -> Dict[str, Any]:
        logger.info("Create image embedding")
        try:
            image = await inputs.read()
            image = self._preprocess({"image": image})

            # Run the inference.
            image_embedding = self.model.image_encoder(image)
            image_embedding = image_embedding.cpu().detach().numpy()

        except Exception as e:
            logger.error(e)

        return self._postprocess(image_embedding)

    def _preprocess(self, inputs: Dict[str, Any]) -> torch.Tensor:
        # Convert the bytes to numpy array.
        image = np.frombuffer(inputs["image"], dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)[:, :, ::-1]  # RGB

        # Get the target shape.
        origin_shape = image.shape[:2]
        target_shape = self.__get_preprocess_shape(*origin_shape)
        height, width = target_shape

        # Preprocess.
        image_fp = cv2.resize(image, dsize=(width, height)).astype(np.float32)
        image_fp -= np.array([123.675, 116.28, 103.53], dtype=np.float32)  # mean
        image_fp /= np.array([58.395, 57.12, 57.375], dtype=np.float32)  # std
        preprocessed = np.zeros((1024, 1024, 3), dtype=np.float32)
        preprocessed[:height, :width, :] = image_fp

        preprocessed = np.moveaxis(preprocessed, -1, 0)[None, :, :, :]
        preprocessed = torch.tensor(preprocessed).to(self.device)
        return preprocessed

    def _postprocess(self, image_embedding: torch.Tensor) -> Dict[str, Any]:
        image_embedding_shape = image_embedding.shape
        image_embedding = base64.b64encode(image_embedding.tobytes()).decode("utf8")
        return {
            "image_embedding": image_embedding,
            "image_embedding_shape": image_embedding_shape,
        }

    @staticmethod
    def __get_preprocess_shape(
        oldh: int, oldw: int, long_side_length: int = 1024
    ) -> Tuple[int, int]:
        scale = long_side_length * 1.0 / max(oldh, oldw)
        newh, neww = oldh * scale, oldw * scale
        neww = int(neww + 0.5)
        newh = int(newh + 0.5)
        return (newh, neww)