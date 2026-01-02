.PHONY: setup test run clean deploy

setup:
	pip install -r requirements.txt
	npm install --prefix talos_vault

test:
	pytest tests/
	anchor test --root talos_vault

run:
	python mission_night.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf talos_vault/target

deploy:
	cd talos_vault && anchor build && anchor deploy
