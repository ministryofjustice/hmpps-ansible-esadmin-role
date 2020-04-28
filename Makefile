default: build
.PHONY: build

prepare:
	pip install -r requirements.txt

check:
	molecule converge
	molecule idempotence
	molecule verify

test:
	molecule test

cleanup:
	molecule destroy
