PYTHON=3.9
BASENAME=segment-anything

env:
	conda create -n $(BASENAME)  python=$(PYTHON) -y

setup:
	pip install -r requirements.txt

run-gradio:
	python gradio/app.py

run-server:
	PYTHONPATH=src python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8888 --reload
