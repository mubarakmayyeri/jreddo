from setuptools import find_namespace_packages, setup

setup(
  name='jreddo',
  version='1.0.0',
  packages=find_namespace_packages(),
  include_package_data=True,
  install_requires = [
    'flask',
  ]
)