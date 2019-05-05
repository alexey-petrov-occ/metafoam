[![Build Status](https://travis-ci.com/alexey-petrov-occ/ketepflow.svg?branch=master)](https://travis-ci.com/alexey-petrov-occ/ketepflow)[![Reviewed by Hound](https://img.shields.io/badge/Reviewed_by-Hound-8E64B0.svg)](https://houndci.com)[![Requirements Status](https://requires.io/github/alexey-petrov-occ/ketepflow/requirements.svg)](https://requires.io/github/alexey-petrov-occ/ketepflow/requirements)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)[![Coverage Status](https://coveralls.io/repos/github/alexey-petrov-occ/ketepflow/badge.svg?branch=master)](https://coveralls.io/github/alexey-petrov-occ/ketepflow?branch=master)
# ketepflow

## Development environment

To prepare development environment it is suggested to use [Docker](https://www.docker.com/resources/what-container).

Use the following command to build Docker image
```bash
make x-docker-env
```
Once Docker image is ready corresponding Docker container can be run
```bash
make x-docker-run
```
Use the following command to install all Python related dependecies
```bash
make x-pipenv-env
```
The following command need to be run to finally enter the development environment
```bash
make x-pipenv-run
```
## Development OpenFOAM extractions procedures
From the very begining `meta-foam` is supposed to easily introduce and support different OpenFOAM forks and versions.
To prove this posibility [openfoam-6](https://github.com/OpenFOAM/OpenFOAM-6.git) and [foam-extend-3.0](https://git.code.sf.net/p/foam-extend/foam-extend-3.0) are introduced. To run corresponding `extraction` procedures the following `makefile` targets can be run, for example
```bash
make x-foam-extend-3.0
```
## Development OpenFOAM Python meta-model support
```bash
make x-check-code
```
