# NOTE: make help uses a special comment format to group targets.
# If you'd like your target to show up use the following:
#
# my_target: ##@category_name sample description for my_target

default: help

SRE_PROJECT := "mnscpd-sre"
_DOPPLER_TOKEN := $(shell _DT='${DOPPLER_TOKEN}'; echo "$${_DT}")
NVM_VERSION := $(shell cat .nvmrc)

.PHONY: install

install: ##@Environment Installs needed prerequisites and software to develop in the SRE space
	$(info ********** Installing Prerequisites **********)
	@brew bundle install --file=Brewfile"
	$(info ********** Installing asdf Tooling **********)
	@make asdf-install
	$(info ********** Installing Python Requirements **********)
	@make python-install
	@npm install -g @shopify/cli @shopify/theme
	@npm install -g yarn
	@echo "Complete!"

############# Extensions Section #############
PHONY: build

############# Extras Section #############
asdf-install: ##@extras Installs asdf and plugins
	$(info ********** Installing asdf/Plugins **********)
	@sh sre-software/install.sh -a
	@asdf reshim
	@echo "Complete!"

python-install: ##@extras Installs Python and Python packages
	$(info ********** Installing Python **********)
	@bash sre-software/install.sh -p
	@echo "Complete!"

############# Development Section #############
help: ##@misc Show this help.
	@echo $(MAKEFILE_LIST)
	@perl -e '$(HELP_FUNC)' $(MAKEFILE_LIST)

# helper function for printing target annotations
# ripped from https://gist.github.com/prwhite/8168133
HELP_FUNC = \
	%help; \
	while(<>) { \
		if(/^([a-z0-9_-]+):.*\#\#(?:@(\w+))?\s(.*)$$/) { \
			push(@{$$help{$$2}}, [$$1, $$3]); \
		} \
	}; \
	print "usage: make [target]\n\n"; \
	for ( sort keys %help ) { \
		print "$$_:\n"; \
		printf("  %-20s %s\n", $$_->[0], $$_->[1]) for @{$$help{$$_}}; \
		print "\n"; \
	}
