PYTHON := python
BLACK := black
CODE_DIR := data_clean/ data_process/

help:
	@echo "Targets:"
	@echo "* black: reformat by black"
	@echo ""

.PHONY: black
black:
	${PYTHON} -m ${BLACK} -l 120 -t py37 cli.py ${CODE_DIR}