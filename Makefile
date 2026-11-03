#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

# TOOLS
UV = uv
PY = $(UV) run python3
MAIN = pac-man.py
CONFIG = config.json

.PHONY: help install run debug clean fclean lint lint-strict

# COMMANDS
help:
	@echo "$(YELLOW)Available Commands:$(RESET)"
	@echo "$(GREEN)  install	->$(RESET) Sync the virtual environment from uv.lock"
	@echo "$(GREEN)  run		->$(RESET) Run Pac-Man program"
	@echo "$(GREEN)  debug		->$(RESET) Run Pac-Man with pdb"
	@echo "$(GREEN)  clean		->$(RESET) Remove caches"
	@echo "$(GREEN)  fclean	->$(RESET) Remove caches and virtual environment"
	@echo "$(GREEN)  lint		->$(RESET) Run flake8 + mypy with required flags"
	@echo "$(GREEN)  lint-strict	->$(RESET) Run flake8 + mypy --strict"

install:
	@echo "$(GREEN)Installing program...$(RESET)"
	@$(UV) sync

run:
	@echo "$(GREEN)Running program.$(RESET)"
	@$(PY) $(MAIN) $(CONFIG)

debug:
	@echo "$(GREEN)Running program with debugger.$(RESET)"
	@$(PY) -m pdb $(MAIN) $(CONFIG)

clean:
	@echo "$(RED)Removing cache files.$(RESET)"
	@find . -path './.venv' -prune -o -type d -name '__pycache__' -print0 \
		| xargs -0 -r rm -rf
	@find . -path './.venv' -prune -o -type f -name '*.py[co]' -print0 \
		| xargs -0 -r rm -f
	@rm -rf .mypy_cache .pytest_cache .ruff_cache

fclean: clean
	@echo "$(RED)Removing virtual environment.$(RESET)"
	@rm -rf .venv

lint:
	@$(UV) run flake8 . --extend-exclude=venv,.venv
	@echo "flake8... $(GREEN)Success.$(RESET)"
	@$(UV) run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs
	@echo "mypy... $(GREEN)Success.$(RESET)"

lint-strict:
	@$(UV) run flake8 . --extend-exclude=venv,.venv
	@echo "flake8... $(GREEN)Success.$(RESET)"
	@$(UV) run mypy . --strict
	@echo "mypy --strict... $(GREEN)Success.$(RESET)"
