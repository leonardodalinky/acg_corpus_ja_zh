PYTHON := python
BLACK := black
ISORT := isort
CODE_DIR := data_*/

help:
	@echo "Targets:"
	@echo "* black: reformat by black"
	@echo "* isort: sort the imports by isort"
	@echo ""

.PHONY: black
black:
	${PYTHON} -m ${BLACK} -l 120 -t py37 cli.py ${CODE_DIR}

.PHONY: isort
isort:
	${PYTHON} -m ${ISORT} -n --ls --tc --py 37 --balanced -l 120 cli.py ${CODE_DIR}
