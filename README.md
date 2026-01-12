# Python-Template

## Features

* uv for environment management
* Pre-commit for linting and formatting
* Pydantic for configuration
* Structlog for logging

:arrow_right: For usage details see [Project Setup](https://github.com/Frontier-Economics/ds-knowledge/blob/main/docs/python/project-setup.md) on the DS Knowledge Hub.

## Project Structure

```
.
├── config                          
│   ├── __init__.py                 
│   ├── settings.py                 # settings using pydantic
│   └── logging.py                  # logging configuration
├── data            
│   ├── 01_raw                      # raw data
│   ├── 02_processed                # data after processing
│   ├── 03_final                    # data for output
│   └── 04_output                   # tables, graphs, etc.
├── docs                            # documentation for your project
├── logs                            # logs
├── models                          # models
├── notebooks                       # notebooks
├── src                             # source code
│   └── __init__.py                 
├── tests                           # tests
│   └── __init__.py                 
├── .gitignore                      # ignore files that cannot commit to Git
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # configure project
└── README.md                       

```

## Setup

1. Set up GitHub repository using this template
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
1. Move to the project directory 
    ```bash
    cd <project-name>
    ```
1. Initialize the project and install dependencies
    ```bash
    uv sync
    ```
1. Install pre-commit hooks for linting and formatting
    ```bash
    uv run pre-commit install
    ```
1. Add your dependencies to the project
    ```bash
    uv add <dependency>
    ```
1. Add and then run your code
    ```bash
    uv run <script>
    ```
