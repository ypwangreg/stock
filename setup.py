from setuptools import setup
from setuptools import find_packages
def _requires_from_file(filename):
    return open(filename).read().splitlines()
setup(
    name="db_operation",
    version="0.1.0",
    description="stock",
    author='yp wang',
    packages=find_packages('src'),
    package_dir={"": "src"},
    install_requires=_requires_from_file('requirements.txt'),
    python_requires='>=3.9.0',
    include_package_data=True,
)