# Backend
### *How to use*:
This project is built with [FastAPI](https://fastapi.tiangolo.com/) and managed by [uv](https://docs.astral.sh/uv/) for high-performance dependency management and environment isolation.

## 1. Prerequisites
You need `uv` installed.
## 2. Directory
Make sure you are in the backend folder or CD into it:
```
cd ./backend
```
## 3. Install Dependencies
You do not need to manually create a virtual environment. Simply run:

```bash
uv sync
```
What this does: It reads pyproject.toml, creates a .venv folder, and installs all required packages exactly as specified in uv.lock.
## 4. Run this bitch
Use:
```bash
uv run fastapi dev app/main.py
```
to run the server, and the
```bash
uv run pytest
```
to run the tests.

Good luck :)