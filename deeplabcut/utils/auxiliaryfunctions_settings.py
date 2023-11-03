#
# DeepLabCut Toolbox (deeplabcut.org)
# © A. & M.W. Mathis Labs
# https://github.com/DeepLabCut/DeepLabCut
#
# Please see AUTHORS for contributors.
# https://github.com/DeepLabCut/DeepLabCut/blob/master/AUTHORS
#
# Licensed under GNU Lesser General Public License v3.0
#
"""
DeepLabCut2.0 Toolbox (deeplabcut.org)
© A. & M. Mathis Labs
https://github.com/DeepLabCut/DeepLabCut
Please see AUTHORS for contributors.

https://github.com/DeepLabCut/DeepLabCut/blob/master/AUTHORS
Licensed under GNU Lesser General Public License v3.0
"""

import os
from pathlib import Path
import yaml
from ruamel.yaml import YAML

from deeplabcut.utils.auxiliaryfunctions import get_deeplabcut_path

projsettingsfile = os.path.join(str(get_deeplabcut_path()), "recents-horse-projects.yaml")

def create_config_template_settings():
    """
    Creates a template for settings.yaml file. This specific order is preserved while saving as yaml file.
    """
    yaml_str = """\
    # Recents Projects configuration files (do not edit)
        recent_files_paths:
        \n
    """
    ruamelFile = YAML()
    cfg_file = ruamelFile.load(yaml_str)
    return cfg_file, ruamelFile
        
def read_config_settings():
    """
    Reads structured config file defining a project.
    """
    ruamelFile = YAML()
    path = Path(projsettingsfile)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = ruamelFile.load(f)
        except Exception as err:
            if len(err.args) > 2:
                if (
                    err.args[2]
                    == "could not determine a constructor for the tag '!!python/tuple'"
                ):
                    with open(path, "r") as ymlfile:
                        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
                else:
                    raise

    else:
        """
        Create an empty setting file if not exist
        """
        cfg = { "recent_files_paths": [] }
    return cfg

def save_settings(recent_files):
    if recent_files and len(recent_files):
        cfg_file, ruamelFile = create_config_template_settings()
        # common parameters:
        cfg_file["recent_files_paths"] = recent_files
        write_config_settings(cfg_file)

def write_config_settings(cfg):
    """
    Write structured config file.
    """
    with open(projsettingsfile, "w") as cf:
        cfg_file, ruamelFile = create_config_template_settings()
        for key in cfg.keys():
            cfg_file[key] = cfg[key]
            
        ruamelFile.dump(cfg_file, cf)

