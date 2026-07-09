.PHONY: validate zip

validate:
	python scripts/smoke_test.py

zip:
	cd .. && zip -r jupyterlite-global-health-gis-starter.zip jupyterlite-global-health-gis-starter -x "*/.git/*" "*/__pycache__/*"
