from setuptools import setup



with open("echoviz/__init__.py", 'r') as fd:
    for line in fd:
        if line.startswith("__version__"):
            VERSION = line.split('=')[-1].strip()


setup(name="echoviz",
      version=VERSION,
      url="https://github.com/mailys-hau/echoviz",
      author="Maïlys HAU",
      packages=["echoviz", "echoviz.threed", "echoviz.twod", "echoviz.utils"],
      install_requires=["kaleido", "numpy", "pandas", "pillow", "plotly",
                        "scikit-image"],
     )
