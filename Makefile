.PHONY: install test smoke chaos-validation preflight
install:
	python -m pip install -e ".[dev]"
test:
	python -m pytest -q
smoke:
	python -m pcc_micro_fighter sweep --matches-per-order 25 --output validation/pairwise-sweep.json
chaos-validation:
	python -m pcc_micro_fighter chaos-validation --output validation/effective-chaos-validation-v0.9.0.json
preflight: test smoke chaos-validation
	@echo "Micro-Fighter v0.9 preflight passed."
