all: test test-foam-extend-3.0 test-openfoam-6

.PHONY: test-openfoam-6 test-foam-extend-3.0

openfoam-6:
	git clone https://github.com/OpenFOAM/OpenFOAM-6.git openfoam-6

test-openfoam-6: openfoam-6
	cd $< && cd ./src/transportModels/ && grep -Ril -E "public viscosityModel" .

foam-extend-3.0:
	git clone https://git.code.sf.net/p/foam-extend/foam-extend-3.0 foam-extend-3.0

test-foam-extend-3.0: foam-extend-3.0
	cd $< && cd ./src/transportModels/ && grep -Ril -E "public viscosityModel" .

clean:
	rm -fr foam-extend-* openfoam-*

test:
	pytest test
