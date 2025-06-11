#Sets the default shell for executing commands as /bin/bash and specifies command should be executed in a Bash shell.
SHELL := /bin/bash

# Color codes for terminal output
COLOR_RESET=\033[0m
COLOR_CYAN=\033[1;36m
COLOR_GREEN=\033[1;32m

# Defines the targets help, install, dev-install, and run as phony targets.
.PHONY: help install run dev debug app server test clean requirements

#sets the default goal to help when no target is specified on the command line.
.DEFAULT_GOAL := help

#Disables echoing of commands.
.SILENT:

#Sets the variable name to the second word from the MAKECMDGOALS.
name := $(word 2,$(MAKECMDGOALS))

#Defines a target named help.
help:
	@echo "Please use 'make <target>' where <target> is one of the following:"
	@echo "  help           	Return this message with usage instructions."
	@echo "  install        	Will install the dependencies using Poetry."
	@echo "  run <folder_name>  Runs GPT Engineer on the folder with the given name."
	@echo "  app            	Run the main FastAPI application (app.py)"
	@echo "  dev            	Run the application in development mode with hot reload"
	@echo "  debug          	Run the application in debug mode (no reload)"
	@echo "  server         	Run the ASGI server directly with uvicorn"
	@echo "  test           	Run all tests"
	@echo "  requirements   	Install Python requirements from requirements.txt"
	@echo "  clean          	Clean up temporary files and caches"

#Defines a target named install. This target will install the project using Poetry.
install: poetry-install install-pre-commit farewell

#Defines a target named poetry-install. This target will install the project dependencies using Poetry.
poetry-install:
	@echo -e "$(COLOR_CYAN)Installing project with Poetry...$(COLOR_RESET)" && \
	poetry install

#Defines a target named install-pre-commit. This target will install the pre-commit hooks.
install-pre-commit:
	export OPENAI_API_BASE="https://api.groq.com/openai/v1/chat/completions"
	export OPENAI_API_KEY="sk-key-from-open-router"
	export MODEL_NAME="meta-llama/llama-3-8b-instruct:extended"
	export LOCAL_MODEL=true
	@echo -e "$(COLOR_CYAN)Installing pre-commit hooks...$(COLOR_RESET)" && \
	poetry run pre-commit install

#Defines a target named farewell. This target will print a farewell message.
farewell:
	@echo -e "$(COLOR_GREEN)All done!$(COLOR_RESET)"

#Defines a target named run. This target will run GPT Engineer on the folder with the given name.


runs:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN)...$(COLOR_RESET)"
	@cd ./gpt-engineer && \
	echo -e "y\ny\ny" | poetry run gpt-engineer "/home/user/app/controllers/$(name)" --model Llama3-70b-8192 --temperature 0.1
run:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN) folder...$(COLOR_RESET)" && \
	cd ./gpt-engineer && poetry run gpt-engineer /home/user/app/app/Http/controller/$(name) --model Llama3-70b-8192 --temperature 0.1

runbabyagi:
	cd ./babyagi && python babyagi.py $(name)

install:
	@echo -e "$(COLOR_CYAN)Running GPT Engineer on $(COLOR_GREEN)$(name)$(COLOR_CYAN) folder...$(COLOR_RESET)" && \
	cd ./gpt-engineer && pip install poetry && make install


# Counts the lines of code in the project
cloc:
	cloc . --exclude-dir=node_modules,dist,build,.mypy_cache,benchmark --exclude-list-file=.gitignore --fullpath --not-match-d='docs/_build' --by-file

ssh:
	ssh-keygen -t rsa -b 4096 \-f ~/.ssh/id_rsa_new

# Application commands
app:
	@echo -e "$(COLOR_CYAN)Starting FastAPI application...$(COLOR_RESET)"
	SPACE_ID="" python app.py

dev:
	@echo -e "$(COLOR_CYAN)Starting application in development mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py

debug:
	@echo -e "$(COLOR_CYAN)Starting application in debug mode...$(COLOR_RESET)"
	SPACE_ID="" python app.py --debug

server:
	@echo -e "$(COLOR_CYAN)Starting ASGI server directly...$(COLOR_RESET)"
	uvicorn mysite.asgi:app --host 0.0.0.0 --port 7860 --reload

# Requirements and dependencies
requirements:
	@echo -e "$(COLOR_CYAN)Installing Python requirements...$(COLOR_RESET)"
	pip install -r requirements.txt

# Testing
test:
	@echo -e "$(COLOR_CYAN)Running tests...$(COLOR_RESET)"
	python -m pytest tests/ -v

# Utility commands
clean:
	@echo -e "$(COLOR_CYAN)Cleaning up temporary files...$(COLOR_RESET)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Database commands
migrate:
	@echo -e "$(COLOR_CYAN)Running database migrations...$(COLOR_RESET)"
	python manage.py migrate

makemigrations:
	@echo -e "$(COLOR_CYAN)Creating database migrations...$(COLOR_RESET)"
	python manage.py makemigrations

# Docker commands
docker-build:
	@echo -e "$(COLOR_CYAN)Building Docker image...$(COLOR_RESET)"
	docker-compose build

docker-up:
	@echo -e "$(COLOR_CYAN)Starting Docker containers...$(COLOR_RESET)"
	docker-compose up -d

docker-down:
	@echo -e "$(COLOR_CYAN)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose down

docker-logs:
	@echo -e "$(COLOR_CYAN)Showing Docker logs...$(COLOR_RESET)"
	docker-compose logs -f