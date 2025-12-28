# genAi_project

A small repository demonstrating simple data generation and query utilities for HR-style sample data. This project includes modules to generate synthetic data, query it, and run a minimal application that ties the pieces together.

## Overview

- **Purpose:** Generate realistic-looking HR data for testing, experimentation, or demos and provide a simple query interface to explore that data.
- **Core modules:** data generation, querying utilities, and a minimal application entry point.

## Files

- `app.py`: Minimal application / runner that ties generation and query components together.
- `data_generation.py`: Script and helpers to generate synthetic HR-style data (employees, departments, roles, etc.).
- `data_query_module.py`: Utilities and functions to query the generated data.
- `hr_schema.ddl`: DDL schema describing the database/tables used by the project.
- `style.css`: Simple styles used by any frontend or HTML exporter included in the project.

## Requirements

- Python 3.8 or newer
- (Optional) Create a virtual environment and install any dependencies if you add a `requirements.txt` file.

## Quick Start

1. (Optional) Create and activate a virtual environment:

	python -m venv .venv
	source .venv/bin/activate

2. Generate sample data:

	python data_generation.py

3. Run the app / query module (example):

	python app.py

Adjust the exact commands based on how you wire up `app.py` and `data_generation.py`.

## Next Steps / Suggestions

- Add a `requirements.txt` or `pyproject.toml` to list dependencies.
- Expand `app.py` with CLI flags or a small web UI to demonstrate queries.
- Add tests for `data_generation.py` and `data_query_module.py`.

If you'd like, I can add usage examples, create a `requirements.txt`, or wire `app.py` into a simple Flask/Streamlit UI — tell me which next step you prefer.