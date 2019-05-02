viscosity = artefacts/viscosity
viscosity_dir = $(viscosity)/$(foam)
viscosity_file = $(viscosity)/$(foam).txt
viscosity_grep = $$(grep -Ril -E "public viscosityModel" .)
viscosity_basename = basename -a $(viscosity_grep) | sed "s%\([^.]*\).*%\1%g"
transportModels_dir = $(foam)/src/transportModels
viscosity_generate = (cd $(transportModels_dir) && $(viscosity_basename) | sort --ignore-case) > $(viscosity_file)
viscosity_check = diff --ignore-space-change $(viscosity)/$(foam).ref $(viscosity_file) || (cat $(viscosity_file) && exit 1)
