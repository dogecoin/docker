#!/usr/bin/env python3

"""
Clean and generate all files for Dogecoin Core images using Dockerfile
templates, copying entrypoint.py. Use a manifest (version.json)
to create images tree structure.

Use python variables in templates using DockerfileTemplate.delimiter `%`.
Regular Dockerfile variable subsitution symbol `$` won't be alterate.

Template instruction example:

RUN FOO=%{bar}
RUN FILENAME=%{var_1}-%var2
"""

from string import Template
import shutil
import json
import os

class DockerfileTemplate(Template):
    """
    Interface to generate Dockerfiles from base templates.

    Enable 2 type of variable in Dockerfiles templates,
    variables with `%` are used by python templates,
    variable with `$` are regular variable used by Dockerfiles.

    Example: `%version` or `%{version}`
    """
    delimiter = "%"

def release_files(version_info):
    """
    Format version release files for all architectures with
    respective checksum.

    Prepare dictionnary for template arguments.
    """
    archs_list = version_info["arches"]

    files = {}
    for architecture, asset in archs_list.items():
        #Remove 'arm/v7' slash, to use armv7 as python variable
        architecture = architecture.replace("/", "")

        #Store tar filename and checksum
        files[f"file_{architecture}"] = asset['file']
        files[f"shasum_{architecture}"] = asset['shasum']

    return files

def load_template(base):
    """Load a Dockerfile base template"""
    with open(base, encoding="utf8") as dockerfile_stream:
        return DockerfileTemplate(dockerfile_stream.read())

def render_dockerfile(template_vars):
    """
    Generate Dockerfile & entrypoint for a single image.
    Save result in `version/variant` directory.
    """
    #Load base template used by the variant
    template = load_template("Dockerfile")

    #Replace python variable in the base template
    dockerfile_content = template.substitute(template_vars)

    #Define destination files
    version = template_vars['version']
    variant = template_vars['variant']

    directory = os.path.join(version, variant)
    dockerfile_path = os.path.join(directory, "Dockerfile")
    entrypoint_path = os.path.join(directory, "entrypoint.py")

    #Write Dockerfile and entrypoint for the image
    os.makedirs(directory)

    shutil.copy("entrypoint.py", entrypoint_path)
    with open(dockerfile_path, "w", encoding="utf8") as dockerfile:
        dockerfile.write(dockerfile_content)

def generate_images_files():
    """
    Generate Dockerfile and entrypoint for all images according to
    a manifest.
    """
    # Get manifest file for images versions/variant/architectures
    with open("version.json", encoding="utf8") as versions_json:
        manifest = json.load(versions_json)

    for version in manifest:
        #Clean previous images
        shutil.rmtree(version, ignore_errors=True)

        #Prepate template variables
        template_vars = {"version" : version}
        template_vars.update(release_files(manifest[version]))

        #Generate image files for each variant of the version
        for variant in manifest[version]['variants']:
            template_vars['variant'] = variant
            render_dockerfile(template_vars)

if __name__ == "__main__":
    generate_images_files()
