import os
import urllib

import torch
from server.utils.logger import get_logger
from segment_anything import sam_model_registry

logger = get_logger()

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
