all: test test-foam-extend-3 test-openfoam-6

.PHONY: test-openfoam-6 test-foam-extend-3

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

test-openfoam-6: openfoam-6
	cd openfoam-6 && cd ./src/transportModels/ && grep -Ril -E "public viscosityModel" .

foam-extend-3:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3

test-foam-extend-3: foam-extend-3
	cd foam-extend-3 && cd ./src/transportModels/ && grep -Ril -E "public viscosityModel" .

clean:
	rm -fr foam-extend-* openfoam-*

test:
	pytest
