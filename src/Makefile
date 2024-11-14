venv:
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

build: venv app.py
	. venv/bin/activate; pyinstaller --onefile app.py -n ask

clean:
	rm -rf venv
	rm -rf dist
	rm -rf build
	rm -rf *.spec