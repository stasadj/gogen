from setuptools import setup

setup(
    name="gogen",
    version="0.0.1",
    description="Go code generator for Silvera tool",

    entry_points={
        "silvera_generators": [
            # Java generator is built-in
            "go = gogen.generator:go",
        ],

        "silvera_evaluators": [
            # Java generator is built-in
            "myeval = gogen.evaluator:myeval",
        ]
    },
)