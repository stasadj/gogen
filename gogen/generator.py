import os
from jinja2 import Environment, FileSystemLoader
from silvera.generator.registration import GeneratorDesc
from gogen.utils import get_templates_path, timestamp, create_if_missing, convert_complex_type, unfold_function_params


def generate_service(service, output_dir):
    """Creates Go project with following folder structure:
      {{ServiceName}}:
          - api
            - controllers
            - server.go
          - models
          - services
          - repositories
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
        env.filters["converttype"] = lambda x: convert_complex_type(x)
        env.filters["return_type"] = lambda fnc: convert_complex_type(fnc.ret_type)
        env.filters["unfold_function_params"] = lambda fnc: unfold_function_params(fnc, False)

        return env

    def get_typedefs(self, service):
        """For given service returns type with typedef names and type of the
        ID attribute
        Args:
            service (ServiceDecl): service declaration
        Returns:
            tuple
        """
        typedefs = []
        for t in service.api.typedefs:
            if not t.crud:
                continue
            # if ID is not specified, the type of generated key will be str
            id_datatype = "str"
            for field in t.fields:
                if field.isid:
                    id_datatype = field.type

            typedefs.append((t.name, id_datatype, t.crud_dict))
        return typedefs

    def generate_main(self, env, root, d):
        """
        Generates main file: main.go
               Args:
                   env (Environment): jinja2 environment used during generation.
                   root (str): path to the dir where application root is located
                   d (dict): dict with variables for templates
        """
        main_template = env.get_template("main.template")
        main_template.stream(d).dump((os.path.join(root, "main.go")))

    def generate_mod(self, env, root, d):
        """
        Generates mod file: go.mod
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

        d = {"service_name": self.service.name.lower()}
        for template_name, ext in [("run_sh", "sh"), ("run_cmd", "cmd")]:
            run_template = env.get_template("%s.template" % template_name)

            out = os.path.join(output_dir, self.service.name, "run.%s" % ext)

            run_template.stream(d).dump(out)

    def generate_server(self, env, root, d):
        """
        Generates api/server.go
               Args:
                   env (Environment): jinja2 environment used during generation.
                   root (str): path to the dir where application root is located
                   d (dict): dict with variables for templates
        """
        d['typedefs'] = self.get_typedefs(self.service)
        d['api'] = self.service.api
        api_path = create_if_missing(os.path.join(root, "api"))
        server_template = env.get_template("api/server.template")
        server_template.stream(d).dump((os.path.join(api_path, "server.go")))

    def generate_models(self, env, root):
        """
        Generates models folder
                Args:
                    env (Environment): jinja2 environment used during generation.
                    root (str): path to the dir where application root is located
         """
        models_path = create_if_missing(os.path.join(root, "models"))
        model_template = env.get_template("models/model.template")

        api = self.service.api

        for typedef in api.typedefs:

            attrs = typedef.fields
            id_attr = None
            for attr in attrs:
                if attr.isid:
                    id_attr = {"name": attr.name,
                               "type": attr.type}

            data = {
                "dependency": False,
                "service_name": self.service.name.lower(),
                "name": typedef.name,
                "attributes": attrs,
                "id_attr": id_attr,
                "timestamp": timestamp()
            }
            model_template.stream(data).dump(os.path.join(models_path, typedef.name.lower() + ".go"))

    def generate_repositories(self, env, root):
        """
        Generates repositories folder
                Args:
                    env (Environment): jinja2 environment used during generation.
                    root (str): path to the dir where application root is located
         """
        repos_path = create_if_missing(os.path.join(root, "repositories"))

        api = self.service.api

        for typedef in api.typedefs:

            id_datatype = "str"
            for field in typedef.fields:
                if field.isid:
                    id_datatype = field.type

            data = {
                "service_name": self.service.name.lower(),
                "timestamp": timestamp(),
                "typedef": typedef.name,
                "id_datatype": id_datatype
            }
            repo_template = env.get_template("repositories/repository.template")
            repo_template.stream(data).dump(os.path.join(repos_path, typedef.name.lower() + "_repository.go"))

    def generate_services(self, env, root):
        """
        Generates services folder
                Args:
                    env (Environment): jinja2 environment used during generation.
                    root (str): path to the dir where application root is located
         """
        services_path = create_if_missing(os.path.join(root, "services"))
        service = self.service
        service_name = service.name.lower()

        typedefs = self.get_typedefs(service)

        service_data = {
            "service_name": service_name,
            "functions": service.api.functions,
            "typedefs": typedefs,
            "dep_names": [s.name for s in service.dependencies],
            "timestamp": timestamp(),
            "consumers": service.f_consumers,
        }

        service_template = env.get_template("services/service.template")
        service_template.stream(service_data).dump(os.path.join(services_path, service_name + "_service.go"))

    def generate_controllers(self, env, root):
        """
        Generates api/controllers folder
                Args:
                    env (Environment): jinja2 environment used during generation.
                    root (str): path to the dir where application root is located
         """
        controllers_path = create_if_missing(os.path.join(root, 'api', "controllers"))
        service = self.service
        service_name = service.name.lower()

        controller_data = {
            "service_name": self.service.name.lower(),
            "api": self.service.api,
            "timestamp": timestamp(),
            "typedefs": self.get_typedefs(self.service),
        }

        controller_template = env.get_template("api/controllers/controller.template")
        controller_template.stream(controller_data).dump(os.path.join(controllers_path, service_name + "_controller.go"))


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
            "service_port": service.port,
            "service_version": service.version,
            "use_circuit_breaker": len(service.dependencies) > 0,
            "timestamp": timestamp(),
            "uses_registry": service.service_registry is not None,
            "reg_port": service.service_registry.port,
            "reg_url": service.service_registry.url,
        }

        # Generate root files
        self.generate_mod(env, root, d)
        self.generate_main(env, root, d)
        self.generate_run_script(output_dir)

        # Generate api/server.go
        self.generate_server(env, root, d)

        # Generate models
        self.generate_models(env, root)

        # Generate repositories
        self.generate_repositories(env, root)

        # Generate services
        self.generate_services(env, root)

        # Generate api/controllers
        self.generate_controllers(env, root)


def generate(decl, output_dir, debug):
    print(decl, output_dir)
    generate_service(decl, output_dir)


# Create Go generator.
go = GeneratorDesc(
    language_name="go",
    language_ver="1.18.2",
    description="Go 1.18.2 code generator",
    gen_func=generate
)
