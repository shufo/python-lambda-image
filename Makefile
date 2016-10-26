# constants

PACKAGE_NAME = "image_resize.zip"
CURRENT_DIR = $(shell pwd | sed -e "s/\/cygdrive//g")

.PHONY: package
ifeq (package,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif
# boot containers
package: ## lambda package : ## make package
	@echo "===> cleaning... " && \
	rm -f $(PACKAGE_NAME)
	@echo "===> package creating... " && \
	zip -r $(PACKAGE_NAME) *
	@echo "===> package created "

.PHONY: help
help: ## Show this help message : ## make help
	@echo -e "\nUsage: make [command] [args]\n"
	@grep -P '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ": ## "}; {printf "\t\033[36m%-20s\033[0m \033[33m%-30s\033[0m (e.g. \033[32m%s\033[0m)\n", $$1, $$2, $$3}'
	@echo -e "\n"

.DEFAULT_GOAL := help
