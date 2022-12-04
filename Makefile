install:
	pip install -r requirements.txt

format:
	black **/*.py

test:
	pytest

start:
	python main.py

start-gtk3-linux:
	python gtk3-linux-main.py

build_linux:
	rm -r dist/ build/
	pyinstaller gtk3-linux-main.py