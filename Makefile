run:
	poetry run uvicorn src.main:app --reload

al:
	poetry run alembic revision --autogenerate -m "init"
	poetry run alembic upgrade head