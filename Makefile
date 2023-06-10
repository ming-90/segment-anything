PYTHON=3.9
BASENAME=mlwiz-apis-server

env:
	conda create -n $(BASENAME)  python=$(PYTHON) -y

gradio:
	python gradio/app.py

server:
	PYTHONPATH=src python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8888 --reload