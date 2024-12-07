format: 
	isort dmcli/ tests/ main.py && black --line-length=79 dmcli/ tests/ main.py

lint:
	ruff check dmcli/ tests/ main.py

fix:
	ruff check dmcli/ tests/ main.py --fix
