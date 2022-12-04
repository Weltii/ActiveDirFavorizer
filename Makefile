install:
	pip install -r requirements.txt

format:
	black **/*.py

test:
	pytest

start:
	python main.py

start_gtk3_linux:
	python gtk3-linux-main.py

build_linux:
	rm -rf dist/ build/
	rm -f build_executable_specific/linux/.progconf
	echo "ARG1=${HOME}/.config/active-dir-favorizer/config.json" > build_executable_specific/linux/.progconf
	pyinstaller gtk3-linux-main.py --add-data ./build_executable_specific/linux/.progconf:./