# Serving Segment Anything Model

## Description
Implement the [segment anything model (SAM)](https://github.com/facebookresearch/segment-anything) from meta in Gradio and use html to implement hover and click.
dockerize this to quickly test the SAM.

## Task
- Implementation Segment Anything Model image embedding API (Done)
- Implementation Segment Anything Model using Gradio
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