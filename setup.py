from setuptools import setup, find_packages
setup(
    name="metafoam",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(include=['metafoam'],
                           exclude=['test', 'artefacts']),
)
