from setuptools import setup, find_packages

with open('README.md', "r", encoding="utf-8") as f:
    descrioption = f.read()


setup(
    name="egygeo",
    version="1.3.1",
    author="Sara Habib",
    author_email="sara.habib48@gmail.com",
    description="A Python package for Egyptian governorate centroids, boundaries, reverse geocoding, and map visualization.",
    packages=find_packages(),
    package_data={"egygeo": ["data/*.json"]},
    include_package_data=True,
    install_requires=[
        "requests",
        "shapely",
    ],
    extras_require={
        "map": ["folium"],
    },
    long_description=descrioption,
    long_description_content_type="text/markdown"
)
