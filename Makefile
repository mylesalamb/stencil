HPYTHON	 	:= /usr/bin/python
VPYTHON		:= venv/bin/python
PIP 		:= venv/bin/pip
BLACK 		:= venv/bin/black
PYLINT      := venv/bin/pylint
PYTEST      := venv/bin/pytest
MYPY		:= venv/bin/mypy
BUILD		:= venv/bin/build
REORDER 	:= venv/bin/reorder-python-imports

dev: venv
venv:
	${HPYTHON} -m venv venv
	${PIP} install --require-virtualenv setuptools wheel
	${PIP} install --require-virtualenv --upgrade pip
	${PIP} install --require-virtualenv --editable '.[dev]' -c constraints.txt 

lint:
	@ echo "=== Running reorder-python-imports ==="
	@ find src/ -name *.py | xargs ${REORDER} || true
	@ find tests/ -name *.py | xargs ${REORDER} || true
	@ echo "=== Running Black ==="
	@${BLACK} src/ tests/
	@ echo "=== Running Pylint ==="
	@${PYLINT} --exit-zero src/ tests/
	@ echo "=== Running Mypy ==="
	@${MYPY} src/ tests/

test:
	${PYTEST}

dist:
	${HPYTHON} -m build .

install:
	${HPYTHON} -m venv /opt/stencil
	/opt/stencil/bin/pip install --require-virtualenv dist/*.whl
	@echo Stencil installed to /opt/stencil/bin, you may want to add this to your PATH

uninstall:
	rm -rf /opt/stencil

clean:
	rm -rf venv/ dist/

.PHONY: clean venv dev test install uninstall