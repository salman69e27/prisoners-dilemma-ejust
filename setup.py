import os.path
import setuptools

setuptools.setup(
    name="prisoners-dilemma-ejust",
    version="0.1.0",
    author="Ahmed Salman Abdelziz <salman69e27@tutanota.com>",
    description=(
        "A Python implemetation of a judge system for iterated prisoner's"
        " dilemma competition at E-JUST "
    ),
    long_description=open(
        os.path.join(os.path.dirname(__file__), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    license="GPL-3.0+",
    keywords="iterated prisoner's dilemma contest",
    url="https://github.com/salman69e27/prisoners-dilemma-ejust",
    packages=["prisoners_dilemma"],
    zip_safe=False,
    python_requires="=3.9.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later"
        " (GPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Typing :: Typed",
    ],
)
