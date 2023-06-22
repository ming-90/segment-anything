# Serving Segment Anything Web demo
## Description
[segment anything model (SAM)](https://github.com/facebookresearch/segment-anything) that can reduce the resources of the server by meta. You can get image embedding in a single inference and do all the segmentation of the image on the client side.
I implemented the click and hover of this model using gradio and web. And I've dockerized it so you can quickly test it out.

## Task
- Implementation Segment Anything Model image embedding API (Done)
- Implementation Segment Anything Model using Gradio (Done)
- Create frontend UI for SAM ( Hover, Click inference )
- Create triton and inference server
- Dockerize server
- Create Docker compose

## How to use
### Gradio run
```bash
make gradio
```
### Server run
```bash
make server
```

## References
- https://github.com/facebookresearch/segment-anything