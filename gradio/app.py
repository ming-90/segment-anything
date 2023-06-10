"""

"""
import os
import gradio as gr
import numpy as np
import requests
import cv2

####################
# Settings
####################
API_URL = os.environ.get("API_SERVER_URL", "http://localhost:8888")

####################
# Functions
####################
def get_coords(evt: gr.SelectData):
    print(f"x: {evt.index[1]} y: {evt.index[0]}")
    return evt.index[1], evt.index[0]

def image_click(
    input_img,
    coord_x,
    coord_y,
):
    print(coord_x, coord_y)


def get_image_embedding(image: np.ndarray):
    image_bytes = cv2.imencode(".jpg", image)[1].tobytes()
    response = requests.get(
        f'{API_URL}/image-embedding',
        files={"file":image_bytes},
        headers={"accept": "application/json"}
    )
    return response.json()["image_embedding"]


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
            [input_img, coord_x, coord_y],
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