virtualenv:
	virtualenv --python=python3.11 "./venv"

install:
	pip3 install -r requirements.txt

freeze:
	pipreqs > requirements.txt --force

dev:
	nodemon src/main.py

run:
	python3 src/main.py
