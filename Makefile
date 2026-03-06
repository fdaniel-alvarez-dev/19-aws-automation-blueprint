.PHONY: demo up down logs seed backup restore verify check runbooks test clean

demo: up seed check backup restore verify runbooks
	@echo "Demo complete. Try: make logs"

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

check:
	bash scripts/check_replication.sh

seed:
	bash scripts/seed_demo_data.sh

backup:
	bash scripts/backup.sh

restore:
	bash scripts/restore.sh

verify:
	bash scripts/backup_verify.sh

runbooks:
	python3 tools/validate_runbooks.py --mode demo

test:
	TEST_MODE=demo python3 tests/run_tests.py

clean:
	rm -rf artifacts
