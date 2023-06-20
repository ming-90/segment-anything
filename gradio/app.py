import os
import gradio as gr
import numpy as np
import requests
import cv2
import base64
import onnxruntime as ort
import multiprocessing
from utils import get_preprocess_shape

####################
# Settings
####################
API_URL = os.environ.get("API_SERVER_URL", "http://localhost:8888")
POINT_LABELS = np.array([[1, -1]], dtype=np.float32)
MASK_INPUT = np.zeros((1, 1, 256, 256), dtype=np.float32)
HAS_MASK_INPUT = np.zeros(1, dtype=np.float32)

####################
# OnnxRuntime
####################
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.intra_op_num_threads = min(8, multiprocessing.cpu_count() // 2)
ort_sess = ort.InferenceSession("decoder/sam_onnx_quantized.onnx", sess_options)

####################
# Functions
####################
def get_coords(evt: gr.SelectData):
    print(f"x: {evt.index[1]} y: {evt.index[0]}")
    return evt.index[0], evt.index[1]

def image_click(
    input_img: np.ndarray,
    embedding_file: str,
    x: int,
    y: int,
):
    print(x, y)
    # load image embedding
    image_embedding = np.load(embedding_file.name)
    image_embedding = image_embedding.reshape(1, 256, 64, 64)

    image_shape = input_img.shape[:-1]

    # resize coordinates
    old_h, old_w = image_shape
    new_h, new_w = get_preprocess_shape(old_h, old_w, 1024)
    x *= new_w / old_w
    y *= new_h / old_h

    # Get a regional mask
    points_coords = np.array([[(x, y), (0, 0)]], dtype=np.float32)
    orig_im_size = np.array(image_shape, dtype=np.float32)
    masks, iou_predictions, _ = ort_sess.run(
        None,
        {
            "image_embeddings": image_embedding,
            "point_coords": points_coords,
            "point_labels": POINT_LABELS,
            "mask_input": MASK_INPUT,
            "has_mask_input": HAS_MASK_INPUT,
            "orig_im_size": orig_im_size,
        },
    )
    mask = masks[0, 0, :, :]
    return (mask > 0).astype(np.uint8)*255

def get_image_embedding(image: np.ndarray):
    image_bytes = cv2.imencode(".jpg", image)[1].tobytes()
    response = requests.get(
        f'{API_URL}/image-embedding',
        files={"file":image_bytes},
        headers={"accept": "application/json"}
    )
    resp = response.json()

    image_embedding = base64.b64decode(resp["image_embedding"])
    image_embedding = np.frombuffer(image_embedding, dtype=np.float32)

    os.makedirs("embeddings", exist_ok=True)
    filepath = "embeddings/image_embedding.npy"
    np.save(filepath, image_embedding)

    return filepath


####################
# Gradio UI
####################

with gr.Blocks() as app:
    with gr.Tab("SAM"):
        with gr.Row():
            gr.Markdown("# Segment Anything Model")

        with gr.Row():
            input_img = gr.Image(label="Input Image").style(height=500)
            output_img = gr.Image(label="Output image").style(height=500)

        with gr.Row():
            coord_x = gr.Number(label="Mouse coords x")
            coord_y = gr.Number(label="Mouse coords y")

        with gr.Row():
            embedding_file = gr.File(label="image embedding file", type="file")

        input_img.select(get_coords, None, [coord_x, coord_y]).then(
            image_click,
            [input_img, embedding_file, coord_x, coord_y],
            output_img
        )

        gr.Examples(
            examples=[
                [
                    os.path.join(os.path.dirname(__file__), "examples/images/strawberry.png"),
                    os.path.join(os.path.dirname(__file__), "examples/embeddings/strawberry.npy"),
                    327,
                    467
                ]
            ],
            inputs=[input_img, embedding_file, coord_x, coord_y],
            outputs=output_img
        )
    with gr.Tab("Image Embedding"):

        with gr.Row():
            with gr.Column():
                image = gr.Image(label="Input Image").style(height=500)
            with gr.Column():
                image_embedding_file = gr.File(label="image embedding file", type="file")
                btn_embedding = gr.Button(value="Get image embedding")


        btn_embedding.click(
            get_image_embedding,
            inputs=image,
            outputs=image_embedding_file,
        )

if __name__ == "__main__":
    app.queue().launch(server_name="0.0.0.0")