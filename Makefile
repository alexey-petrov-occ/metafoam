all: test test-foam-extend-3.0 test-openfoam-6

.PHONY: test-openfoam-6 test-foam-extend-3.0 clean-viscosity

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

viscosity_grep = $$(grep -Ril -E "public viscosityModel" .)
viscosity_basename = basename -a $(viscosity_grep) | sed "s%\([^.]*\).*%\1%g"
viscosity = (cd $< && cd ./src/transportModels/ && $(viscosity_basename)) > viscosity/$<.txt

test-openfoam-6: openfoam-6
	- $(viscosity)

test-foam-extend-3.0: foam-extend-3.0
	- $(viscosity)

clean:
	rm -fr foam-extend-* openfoam-*

clean-viscosity:
	rm -fr viscosity/*.*

test:
	pytest test
