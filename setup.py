from setuptools import setup, find_packages

with open('README.md', "r") as f:
    descrioption = f.read()


setup(
    name="egygeo",
    version="1.1.0",
    author="Sara Habib",
    author_email="sara.habib48@gmail.com",
    description="A Python package designed to provide easy access to the geographic coordinates (latitude and longitude) of various Egyptian subdivisions.",
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package requires
    ],
    long_description=descrioption,
    long_description_content_type="text/markdown"
)
