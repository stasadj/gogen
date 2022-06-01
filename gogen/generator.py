import os
from jinja2 import Environment, FileSystemLoader
from silvera.generator.registration import GeneratorDesc
from gogen.utils import get_templates_path


def generate_service(service, output_dir):
    templates_path = get_templates_path()
    env = Environment(loader=FileSystemLoader(templates_path))

    main_path = os.path.join(output_dir, service.name)
    if not os.path.exists(main_path):
        os.mkdir(main_path)

    main_template = env.get_template("main.template")
    main_template.stream({}).dump(os.path.join(main_path, "main.go"))


def generate(decl, output_dir, debug):
    print("Called!")
    print(decl, output_dir)
    generate_service(decl, output_dir)


# Create Go generator.
go = GeneratorDesc(
    language_name="go",
    language_ver="1.18.2",
    description="Go 1.18.2 code generator",
    gen_func=generate
)
