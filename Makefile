###############################################
#
# campusromero-openedx-extensions commands.
#
###############################################

.DEFAULT_GOAL := help

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## delete most git-ignored files
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +

requirements: ## install development environment requirements
	pip install -r requirements/base.txt

extract_translations: ## Extract translations es_419.
	django-admin.py makemessages -l es_419 -v0 -d django

compile_translations: ## Compile .po files into .mo files.
	django-admin.py compilemessages

bump: ## Tag the current version using semantinc versioning and git tags
      ## Run with make bump version=[minor|major|patch]
	 bumpversion $(version)

python-quality-test:
	pylint ./campusromero_openedx_extensions
	pycodestyle ./campusromero_openedx_extensions

