# Development

This document provides information on how to develop the project.

## Prerequisites

Before you start developing the project, make sure you have the following installed:

- Python 3.10^^

## Makefile

### STOP!

Before you start, make sure you have the following:

DOPPLER_TOKEN=<your-doppler-token>

You can set this in your SHELL environment prior to running the code:

```bash
export DOPPLER_TOKEN=<your-doppler-token> # Replace <your-doppler-token> with your Doppler token
```

#### NOTE

To attain your Doppler token, please see your technical lead, or the SRE team.

The project includes a Makefile that provides a set of commands to help with the deployment process. The Makefile includes the following commands:

This helps with Developer experience because the Doppler configuration is already set, no .env files are needed.

## Commands

- `make install`: Installs the project dependencies (Python, NodeJS, NPM, Yarn, etc.)
- `make setup`: Sets up the project - Python Packages, NPM Packages, etc.
- `make build`: Builds the project locally - Creates the toml-file.

Example:

```bash
make install # Runs brew bundle, python install, npm, nodejs, etc.
make setup # This is a custom command to setup the project -- Python Packages, NPM Packages, etc.
make build-local
```
