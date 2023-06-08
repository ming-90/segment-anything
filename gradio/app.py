"""

"""
import os
import gradio as gr

def get_coords(evt: gr.SelectData):
    print(f"x: {evt.index[1]} y: {evt.index[0]}")
    return evt.index[1], evt.index[0]

def image_click(
    input_img,
    coord_x,
    coord_y,
):
    print(coord_x, coord_y)

##################################
# UI
##################################

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown("# Segment Anything Model")

    with gr.Row():
        input_img = gr.Image(label="Input Image").style(height=500)
        output_img = gr.Image(label="Output image").style(height=500)

    with gr.Row():
        coord_x = gr.Number(label="Mouse coords x")
        coord_y = gr.Number(label="Mouse coords y")


    input_img.select(get_coords, None, [coord_x, coord_y]).then(
        image_click,
        [input_img, coord_x, coord_y],
        output_img
    )
    gr.Examples(
        examples=[
            [
                os.path.join(os.path.dirname(__file__), "examples/strawberry.png"),
                327,
                467
            ]
        ],
        inputs=[input_img, coord_x, coord_y],
        outputs=output_img
    )




if __name__ == "__main__":
    app.queue().launch(server_name="0.0.0.0")