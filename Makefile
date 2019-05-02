all: test-foam-extend-3.0 test-openfoam-6 test

.PHONY: test-openfoam-6 test-foam-extend-3.0 clean-artefacts test

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

foam = $<
viscosity_dir = artefacts/viscosity
viscosity_out = $(viscosity_dir)/$(foam).txt
viscosity_grep = $$(grep -Ril -E "public viscosityModel" .)
viscosity_basename = basename -a $(viscosity_grep) | sed "s%\([^.]*\).*%\1%g"
transportModels_dir = $(foam)/src/transportModels
viscosity_generate = (cd $(transportModels_dir) && $(viscosity_basename) | sort --ignore-case) > $(viscosity_out)
viscosity_check = diff --ignore-space-change $(viscosity_dir)/$(foam).ref $(viscosity_out) || (cat $(viscosity_out) && exit 1)

test-openfoam-6: openfoam-6
	- $(viscosity_generate)
	$(viscosity_check)

test-foam-extend-3.0: foam-extend-3.0
	- $(viscosity_generate)
	$(viscosity_check)
	(cd $(foam) && find . -name powerLaw.C -exec grep lookup {} \;) > $(viscosity_dir)/$(foam)/powerLaw.txt
	(cat $(viscosity_out) | while read f; do find $(transportModels_dir) -name $${f}.C -print ; done)

clean: clean-artefacts
	rm -fr foam-extend-* openfoam-*

clean-artefacts:
	find artefacts -name '*.txt' -exec rm -fr {} \;

test:
	pytest test

install:
	sudo apt-get install -y coreutils findutils grep

requirements:
	pipenv run pipenv_to_requirements -d requirements-dev.txt
