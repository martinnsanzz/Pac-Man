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

.PHONY: install run debug

# COMMANDS
install:
	@echo "$(GREEN)Installing program...$(RESET)"
	@$(UV) sync

run:
	@echo "$(GREEN)Running program.$(RESET)"
	@$(PY) $(MAIN) $(CONFIG)

debug:
	@echo "$(GREEN)Running program with debugger.$(RESET)"
	@$(PY) -m pdb $(MAIN) $(CONFIG)

