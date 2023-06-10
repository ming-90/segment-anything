# Serving Segment Anything Model

## Description
Implement the [segment anything model (SAM)](https://github.com/facebookresearch/segment-anything) from meta in Gradio and use html to implement hover and click.
dockerize this to quickly test the SAM.

## Task
- Implementation Segment Anything Model image embedding (Done)
- Implementation Segment Anything Model using Gradio
- Create frontend UI for SAM ( Hover, Click inference)
- Create backend for SAM image embedding
- Create triton and inference server
- Dockerize server
- Create Docker compose

## How to use
### Client run
```bash

```
### Server run
```bash
PYTHONPATH=src python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8888 --reload
```

## References
- https://github.com/facebookresearch/segment-anything