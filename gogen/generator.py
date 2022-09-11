import os
from jinja2 import Environment, FileSystemLoader
from silvera.generator.registration import GeneratorDesc
from gogen.utils import get_templates_path, timestamp, create_if_missing


def generate_service(service, output_dir):
    """Creates Go project with following folder structure:
      {{ServiceName}}:
          - api
          - models
          - controllers
          - go.mod
          - main.go
      """
    generator = ServiceGenerator(service)
    generator.generate(output_dir)


class ServiceGenerator:
    """Base class for service generators
    Attributes:
        service (Service): core service object
        _templates_path (str): path to templates used during code generation
    """
    def __init__(self, service):
        super().__init__()

        self.service = service
        self._templates_path = get_templates_path()
        self.model = service.parent.model

    def _get_env(self):
        env = Environment(loader=FileSystemLoader(self._templates_path))
        env.filters["firstupper"] = lambda x: x[0].upper() + x[1:]
        env.filters["firstlower"] = lambda x: x[0].lower() + x[1:]

        return env

    def generate_main(self, env, root, d):
        """
        Generate main file: main.go
               Args:
                   env (Environment): jinja2 environment used during generation.
                   root (str): path to the dir where application root is located
                   d (dict): dict with variables for templates
        """
        main_template = env.get_template("main.template")
        main_template.stream(d).dump((os.path.join(root, "main.go")))

    def generate_mod(self, env, root, d):
        """
        Generate mod file: go.mod
               Args:
                   env (Environment): jinja2 environment used during generation.
                   root (str): path to the dir where application root is located
                   d (dict): dict with variables for templates
        """
        mod_template = env.get_template("mod.template")
        mod_template.stream(d).dump((os.path.join(root, "go.mod")))

    def generate_run_script(self, output_dir):
        """
        Generates run.sh script for application in its root folder
        Args:
            output_dir (str): path to the dir where application root is located
        Returns:
            None
        """
        templates_path = get_templates_path()
        env = Environment(loader=FileSystemLoader(templates_path))

        d = {"name": self.service.name}
        for template_name, ext in [("run_sh", "sh"), ("run_cmd", "cmd")]:
            run_template = env.get_template("%s.template" % template_name)

            out = os.path.join(output_dir, self.service.name, "run.%s" % ext)

            run_template.stream(d).dump(out)

    def generate_api(self, env, root, d):
        """
        Generate api: server.go
               Args:
                   env (Environment): jinja2 environment used during generation.
                   root (str): path to the dir where application root is located
                   d (dict): dict with variables for templates
        """
        api_path = create_if_missing(os.path.join(root, "api"))
        server_template = env.get_template("api/server.template")
        server_template.stream(d).dump((os.path.join(api_path, "server.go")))

    def generate_models(self, env, root, d):
        """
        Generate models: models.go
                Args:
                    env (Environment): jinja2 environment used during generation.
                    root (str): path to the dir where application root is located
                    d (dict): dict with variables for templates
         """
        models_path = create_if_missing(os.path.join(root, "models"))
        model_template = env.get_template("models/model.template")
        model_template.stream(d).dump((os.path.join(models_path, self.service.name.lower()+".go")))

    def generate(self, output_dir):
        """
        Generate service application.
        Args:
            output_dir (str): path to the output dir
        """
        env = self._get_env()

        service = self.service
        service_name = service.name
        root = os.path.join(output_dir, service_name)

        create_if_missing(root)

        d = {
            "service_name": service.name.lower(),
            "service_port": ":%s" % service.port,
            "service_version": service.version,
            "use_circuit_breaker": len(service.dependencies) > 0,
            "timestamp": timestamp(),
            "uses_registry": service.service_registry is not None
        }

        # Generate root files
        self.generate_mod(env, root, d)
        self.generate_main(env, root, d)
        self.generate_run_script(output_dir)

        # Generate api
        self.generate_api(env, root, d)

        # Generate models
        self.generate_models(env, root, d)


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
