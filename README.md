## Local install

#### Prerequisites

1. Python 3.12
2. Install packege manager Poetry https://python-poetry.org/docs/#installation


```shell
# 1. Create virtual environment
poetry shell

# 2. Install dependencies
poetry install
```

## Local Run

```shell
# 1. Create .env and set your own configs  
cp .env.example .env

# 2. Before running script make sure that `SOURCE_BRANCH` and `TARGET_BRANCH` in your local repo is up to date

# 3. Run script
./main.py
```