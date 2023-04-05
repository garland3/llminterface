from dynaconf import Dynaconf
from pathlib import Path
import os

# get current file location, then add settings.toml and .secrets.toml
cwd = os.path.dirname(os.path.realpath(__file__))
settings_files = []
potential_file_names = ["settings.toml", ".secrets.toml", ".env"]

home_dir = Path(os.path.expanduser("~"))
clillm_dir = Path(os.path.join(home_dir, ".llminterface"))

dirs_to_search = [cwd, os.path.join(cwd, ".."), os.path.join(cwd, "..", ".."), clillm_dir]

for potential_file_name in potential_file_names:
    for d in dirs_to_search:
        file = os.path.join(d, potential_file_name)
        # test if the file exists
        if os.path.exists(file):
            settings_files.append(file)

# if one of the files is not .secrets.toml, then print a big warning
for f in settings_files:
    # get the file name
    file_name = os.path.basename(f)
    if file_name == ".secrets.toml":
        break
else:
    print("----------------------------------------")
    Warning("WARNING: .secrets.toml not found. Likely you are missing the openai api key!")          
    print("----------------------------------------")

        
# print("settings_files: ", settings_files)
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=settings_files,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
