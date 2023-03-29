from dynaconf import Dynaconf
from pathlib import Path
import os

# get current file location, then add settings.toml and .secrets.toml
cwd = os.path.dirname(os.path.realpath(__file__))
settings_files = []
potential_file_names = ["settings.toml", ".secrets.toml", ".env"]

home_dir = Path(os.path.expanduser("~"))
clillm_dir = Path(os.path.join(home_dir, "clillm"))

dirs_to_search = [cwd, os.path.join(cwd, ".."), os.path.join(cwd, "..", ".."), clillm_dir]

for potential_file_name in potential_file_names:
    for d in dirs_to_search:
        file = os.path.join(d, potential_file_name)
        # test if the file exists
        if os.path.exists(file):
            settings_files.append(file)
            
        
print("settings_files: ", settings_files)
settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=settings_files,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
