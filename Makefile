install:
	pip install -r requirements.txt

format:
	black **/*.py

test:
	pytest

start:
	python service/main.py

start_gtk3_linux:
	python service/gtk3_linux_main.py

build_linux:
	rm -rf dist/ build/
	rm -f build_executable_specific/linux/.progconf
	echo "ARG1=${HOME}/.config/active-dir-favorizer/config.json" > build_executable_specific/linux/.progconf
	pyinstaller service/gtk3_linux_main.py --add-data ./build_executable_specific/linux/.progconf:./