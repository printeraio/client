virtualenv:
	virtualenv --python=python3.11 "./venv"

install:
	pip3 install -r requirements.txt

freeze:
	pipreqs > requirements.txt --force

dev:
	nodemon src/__init__.py

run:
	python3 src/__init__.py
