.PHONY: install test smoke preflight
install:
	python -m pip install -e ".[dev]"
test:
	python -m pytest -q
smoke:
	python -m pcc_micro_fighter sweep --matches-per-order 25 --output validation/pairwise-sweep.json
preflight: test smoke
	@echo "Micro-Fighter v0.7 preflight passed."
