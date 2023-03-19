virtualenv:
	virtualenv --python=$(path) "./venv"

install:
	pip3 install -r requirements.txt

dev:
	nodemon src/main.py

run:
	python3 src/main.py
