ONESHELL:

.DEFAULT_GOAL		:= run

# ------------------ Colors ------------------ #
RESET				:= \033[0m
BOLD				:= \033[1m
UNDERLINE			:= \033[4m
RED					:= \033[1;91m
GREEN				:= \033[1;92m
BLUE				:= \033[1;94m
YELLOW				:= \033[1;93m
PURPLE				:= \033[1;95m
CYAN				:= \033[1;96m

# ------------------ Tools  ------------------ #
VENV				:= .venv
UV					:= uv
RUN_COMM			:= ${UV} run python
DEBUGGER			:= pdb

# ------------------ Flags ------------------ #
MYPY_FLAGS			:= . --warn-return-any --warn-unused-ignores \
						--ignore-missing-imports --disallow-untyped-defs \
						--check-untyped-defs --explicit-package-bases

MYPY_STRICT_FLAGS	:= . --strict --explicit-package-bases

# ------------------ Commands ------------------ #
help:
	@echo "$(YELLOW)Available Commands:$(RESET)"
	@echo "$(CYAN)  install	->$(RESET) Sync the virtual environment from uv.lock"
	@echo "$(CYAN)  run		->$(RESET) Run Pac-Man program"
	@echo "$(CYAN)  debug		->$(RESET) Run Pac-Man with pdb for debugging"
	@echo "$(CYAN)  clean		->$(RESET) Clean repo from unwanted files "
	@echo "$(CYAN)  fclean	->$(RESET) Remove caches and virtual environment"
	@echo "$(CYAN)  lint		->$(RESET) Run flake8 + mypy with required flags"
	@echo "$(CYAN)  lint-strict	->$(RESET) Run flake8 + mypy --strict"

check_uv:
	@command -v ${UV} >/dev/null 2>&1 || { \
		echo "${RED}uv not found. Install it: https://docs.astral.sh/uv/${RESET}"; \
		exit 1; \
	}

install: check_uv
	@if ! ${UV} sync --check >/dev/null 2>&1; then \
		echo "${YELLOW}Installing dependencies...${RESET}"; \
		${UV} sync >/dev/null 2>&1 || exit 1; \
	fi
	@echo "${GREEN}Everything installed${RESET}"

run: install
	@clear
	@echo "${GREEN}\nRunning program... !!\n${RESET}"
	@${RUN_COMM} -m src

debug: install
	@echo "${GREEN}\nRunning program in debug mode... !!\n${RESET}"
	@${RUN_COMM} -m $(DEBUGGER) -m src

clean:
	@echo "${RED}Removing '.mypy_cache' folders.${RESET}"
	@find . -type d -name .mypy_cache -exec rm -rf {} +

	@echo "${RED}Removing '__pycache__' folders.${RESET}"
	@find . -type d -name __pycache__ -exec rm -rf {} +

	@echo "${RED}Removing '.pytest_cache' folders.${RESET}"
	@find . -type d -name .pytest_cache -exec rm -rf {} +

	@echo "${RED}Removing '.pyc' files.${RESET}"
	@find . -type f -name "*.pyc" -exec rm -rf {} +

fclean: clean
	@echo "${RED}Removing '.venv'.${RESET}"
	@rm -rf $(VENV)


	@echo "${YELLOW}\nMAKE SURE YOU EXIT VENV 'deactivate'.${RESET}"

lint:
	@echo "${YELLOW}Running flake8...${RESET}"
	-@flake8 . && echo "${GREEN}✓ flake8 passed${RESET}" || true

	@echo "${YELLOW}\nRunning mypy...${RESET}"
	-@mypy ${MYPY_FLAGS} && echo "${GREEN}✓ mypy passed${RESET}" || true

lint-strict:
	@echo "${YELLOW}Running flake8...${RESET}"
	@flake8 . && echo "${GREEN}✓ flake8 passed${RESET}" || true

	@echo "${YELLOW}Running mypy --strict...${RESET}"
	@mypy ${MYPY_STRICT_FLAGS} && echo "${GREEN}✓ mypy --strict passed${RESET}"|| true

.PHONY: help install run debug clean fclean lint lint-strict