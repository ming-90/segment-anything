import os
import gradio as gr

# Trasnforms
patch_height_nums = 40
patch_width_nums = 40
patch_size = 14

height, width = patch_size * patch_height_nums, patch_size * patch_width_nums

def greet(name):
    return "Hello " + name + "!"


examples_sam_brush = [
    [
        os.path.join(os.path.dirname(__file__), "examples/strawberry.png"),
        os.path.join(os.path.dirname(__file__), "examples/strawberry.png"),
    ]
]
def get_coords(evt: gr.SelectData):
    print(f"x: {evt.index[1]} y: {evt.index[0]}")
    return evt.index[1], evt.index[0]

def image_click(e):
    print(e)

with gr.Row():
    gr.Markdown("# Inputs")
with gr.Row():
    input_img = gr.Image(label="Input Image")

input_img.select(get_coords, None).then(
    fn = image_click,
    input=[gr.SelectData]
)




if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0")