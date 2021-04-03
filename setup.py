from setuptools import find_packages, setup

from core import __title__, __version__


def get_requirements(suffix=""):
    with open("requirements{}.txt".format(suffix)) as f:
        rv = f.read().splitlines()
    return rv


setup(
    name=__title__.replace(" ", "_").lower(),
    version=__version__,
    long_description=__doc__,
    packages=[p for p in find_packages() if p != "tests"],
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
)
