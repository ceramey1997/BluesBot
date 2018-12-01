import os
from setuptools import setup, find_packages

package = 'BluesBot'
setup_dir = os.path.dirname(os.path.abspath(__file__))
version_file = os.path.join(setup_dir, 'VERSION')

with open(version_file) as version_file:
    version = version_file.read().strip()
requirements = (
    open(os.path.join(setup_dir,'requirements.txt')).read().splitlines()
)
required = [line for line in requirements if not line.startswith('-')]

setup(name=package,
      version=version,
      description="Discord Music Bot",
      url="https://github.com/pypa/sampleproject",
      author="The World",
      author_email="author@example.com",
      packages=find_packages(),
      install_requires=[required],
      include_package_data=True
     )