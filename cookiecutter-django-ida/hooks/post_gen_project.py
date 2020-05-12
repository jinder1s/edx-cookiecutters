from cookiecutter.main import cookiecutter
import shutil
import os

from edx_lint.cmd.write import write_main

# cookiecutter can import a template from either github or from a location on local disk.
# If someone is debugging this repository locally, the below block is necessary to pull in
#   local versions of the templates
EDX_COOKIECUTTER_ROOTDIR=os.getenv('EDX_COOKIECUTTER_ROOTDIR')
import_template_from_github = True
if EDX_COOKIECUTTER_ROOTDIR is not None and isinstance(EDX_COOKIECUTTER_ROOTDIR, str):
    if len(EDX_COOKIECUTTER_ROOTDIR) > 0:
        import_template_from_github = False

def move(src, dest):
    """
    Used to move files or folders without replacement
    """
    if os.path.isfile(dest):
        os.remove(src)
        return
    if os.path.isdir(src) and os.path.isdir(dest):
        files = os.listdir(src)
        for f in files:
            move(os.path.join(src,f), os.path.join(dest,f))
        os.rmdir(src)
    else:
        shutil.move(src, dest)

def combine_templates(layer1, layer2, output_dest):
    """
    Used to move all files in two layers into one folder, layer2 will overwrite files in layer1
    """
    move(layer2, output_dest)
    move(layer1, output_dest)

def remove(path):
    full_path = os.path.join(os.getcwd(), path)
    if os.path.isfile(full_path):
        os.remove(full_path)
    elif os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        print("{path} not in cookiecutter output".format(path=full_path))


# output location for django-template cookiecutter
python_placeholder_repo_name = "placeholder_repo_name_0"

# Use Python template to get python files
extra_context = {}
extra_context["repo_name"] = "{{cookiecutter.repo_name}}"
extra_context["sub_dir_name"] = "{{cookiecutter.repo_name}}"
extra_context["project_name"] = "{{cookiecutter.project_name}}"
extra_context["project_short_description"] = "{{cookiecutter.project_short_description}}"
extra_context["version"] = "{{cookiecutter.version}}"
extra_context["owner_type"] = "{{cookiecutter.owner_name}}"
extra_context["author_name"] = "{{cookiecutter.author_name}}"
extra_context["author_email"] = "{{cookiecutter.author_email}}"
extra_context["owner_name"] = "{{cookiecutter.owner_name}}"
extra_context["open_source_license"] = "{{cookiecutter.open_source_license}}"

extra_context["placeholder_repo_name"] = python_placeholder_repo_name

#  get template from github
if import_template_from_github:
    directory = "python-template"
    cookiecutter('git@github.com:edx/edx-cookiecutters.git', extra_context=extra_context, no_input=True, directory=directory)
else:
    cookiecutter(os.path.join(EDX_COOKIECUTTER_ROOTDIR,'python-template'), extra_context=extra_context, no_input=True)

project_root_dir = os.getcwd()
python_template_cookiecutter_output_loc = os.path.join(project_root_dir, python_placeholder_repo_name)
files = os.listdir(python_template_cookiecutter_output_loc)

for f in files:
    move(os.path.join(python_template_cookiecutter_output_loc,f), os.path.join(project_root_dir, f))

os.rmdir(python_template_cookiecutter_output_loc)

# Removing unecessary files from python and django templates:
remove("setup.py")
remove("tox.ini")
remove("MANIFEST.in")

write_main(['pylintrc'])
