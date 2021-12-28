from setuptools import setup, find_packages

setup(
    name="kid-maya-2022",
    version="0.0.1",
    description="A collection of tools for Maya 2022",
    author="Justin Tirado",
    author_email="jt.tirado@gmail.com",
    url="https://github.com/KidKaboom/Kid-Maya-2022",
    extras_require=dict(tests=["pytest"]),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    )

