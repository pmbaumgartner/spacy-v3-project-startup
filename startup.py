import hashlib
from pathlib import Path

import questionary
import srsly

WELCOME = """Welcome to the spaCy project transfer script.

The intent of this walkthrough script is to create a spaCy v3 project.yml file for an existing NLP project.

You don't even have to be using a spaCy model (yet) - there are many features like assets and remotes
 that are helpful before your project is in a final state.
 
For more on spaCy projects: https://spacy.io/usage/projects"""

ORDER = """The order of this walkthrough is:

1. Project Information (Title + Description)
2. Add project directories
2. Add project assets/data Location
3. Templates/Placeholders
"""

project_yaml = {}

questionary.print("Welcome!", style="bold")
questionary.print(WELCOME, style="italic")
questionary.print(ORDER)

title = questionary.text("What's the title of the project?").ask()
project_yaml["title"] = title
description = questionary.text(
    "Please provide a short description of the project."
).ask()
project_yaml["description"] = description


project_directory = questionary.path(
    "What's the path to the current project directory?", only_directories=True
).ask()

questionary.print(f"Great, we'll be using: {project_directory}")

add_directories = questionary.confirm(
    f"Would you like to add current subdirectories of {project_directory} as project directories? (To ensure they exist for future commands and workflows)"
).ask()
if add_directories:
    directories = list(
        p.name
        for p in Path(project_directory).glob("*")
        if p.is_dir() and not p.name.startswith(".")
    )
    project_yaml["directories"] = directories
    print(f"{len(directories)} directories added.")


assets_exist = questionary.confirm(
    "Is there an existing folder of data or assets the project uses you'd like to add?"
).ask()
if assets_exist:
    assets = questionary.path(
        "Where is this directory located?", default=str(project_directory), only_directories=True
    ).ask()
    assets_files = list(p for p in Path(assets).rglob("*") if p.is_file())
    questionary.print(f"{len(assets_files)} asset files found.")
    add_md5 = questionary.confirm(
        "Would you like to add the md5 checksums to current asset files? (this can prevent future unnecessary redownloading)"
    ).ask()
    if add_md5:
        asset_md5s = [
            hashlib.md5(Path(path).read_bytes()).hexdigest() for path in assets_files
        ]
        asset_data = [
            {
                "dest": str(path.relative_to(project_directory)),
                "description": "",
                "checksum": md5,
            }
            for path, md5 in zip(assets_files, asset_md5s)
        ]
        project_yaml["assets"] = asset_data

    else:
        asset_data = [
            {"dest": str(path.relative_to(project_directory)), "description": ""}
            for path in assets_files
        ]
        project_yaml["assets"] = asset_data
else:
    asset_example = questionary.confirm("Would you like to add an example asset?").ask()
    if asset_example:
        asset_data = [
            {
                "dest": "path/to/asset",
                "description": "Description of asset.",
                "url": "url to asset source",
            }
        ]
        project_yaml["assets"] = asset_data


var_example = questionary.confirm(
    "Would you like to add an example variable? (For consistent argument or path use across multiple commands)"
).ask()
if var_example:
    project_vars = {"example": "example1", "other_example": "another-example"}
    project_yaml["vars"] = project_vars


command_example = questionary.confirm("Would you like to add example commands?").ask()
if command_example:
    commands = [
        {
            "name": "make_temporary_file",
            "help": "make a temporary file  (EXAMPLE)",
            "script": ["touch temporaryfile"],
            "outputs": ["temporaryfile"],
        },
        {
            "name": "delete_temporary_file",
            "help": "Print listed files (EXAMPLE)",
            "script": ["rm -f temporaryfile"],
            "deps": ["temporaryfile"],
        },
    ]
    project_yaml["commands"] = commands

workflow_example = questionary.confirm(
    "Would you like to add a workflow example?"
).ask()
if workflow_example:
    workflow = {"all": ["make_temporary_file", "delete_temporary_file"]}
    project_yaml["workflows"] = workflow

output_path = Path(project_directory) / "project.yml"
srsly.write_yaml(output_path, project_yaml)
with output_path.open("a") as output_yaml:
    output_yaml.write("\n")
    output_yaml.write("\n# This project.yml generated with https://github.com/pmbaumgartner/spacy-v3-project-startup")
    output_yaml.write("\n# For more on spaCy projects, see: https://spacy.io/usage/projects and https://spacy.io/api/cli#project")
    output_yaml.write("\n# And see the templates at: https://github.com/explosion/projects")
questionary.print(f"Project yml output to {output_path}.")
