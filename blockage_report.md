It seems there are persistent issues with the Python virtual environment, specifically with `uv`'s ability to properly install and make `alembic` accessible, even after attempting to recreate the environment and reinstall dependencies. This is blocking the generation and application of database migrations (Task T002).

I recommend the following steps:
1.  **Manually verify `uv` and Python installation**: Ensure `uv` itself is correctly installed and functioning, and that the Python interpreter it's using is healthy.
2.  **Manual Migration**: You might need to manually run `uv venv --clear`, `uv pip install -e .` within the `backend` directory, and then manually execute `alembic init -t generic alembic` (if `alembic.ini` is missing) and `alembic revision --autogenerate -m "Add new Task attributes"` from your terminal after activating the virtual environment.

I am currently blocked from proceeding with Task T002 due to these environment issues. Please advise on how to proceed.