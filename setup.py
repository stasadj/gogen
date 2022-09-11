from setuptools import setup

setup(
    name="gogen",
    version="0.0.1",
    description="Go code generator for Silvera tool",
    packages=['gogen'],
    entry_points={
        "silvera_generators": [
            "go = gogen.generator:go",
        ],

        "silvera_evaluators": [
            "myeval = gogen.evaluator:myeval",
        ]
    },
    install_requires=["silvera", "Jinja2"]
)