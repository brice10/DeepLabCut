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

def create_config_template_horse():
    """
    Creates a template for config.yaml file. This specific order is preserved while saving as yaml file.
    """
    yaml_str = """\
    # Project definitions (do not edit)
        horse_name:
        horse_father:
        horse_mother:
        horse_owner:
        horse_seller:
        horse_buyer:
        horse_type:
        date:
        \n
    # Project path (change when moving around)
        project_path:
        \n
    # Video to analyse (change when moving around)
        video_path:
        video_type:
        \n
    """
    ruamelFile = YAML()
    cfg_file = ruamelFile.load(yaml_str)
    return cfg_file, ruamelFile
        
def read_config_horse(configname):
    """
    Reads structured config file defining a project.
    """
    ruamelFile = YAML()
    path = Path(configname)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = ruamelFile.load(f)
                curr_dir = os.path.dirname(configname)
                if cfg["project_path"] != curr_dir:
                    cfg["project_path"] = curr_dir
                    write_config_horse(configname, cfg)
        except Exception as err:
            if len(err.args) > 2:
                if (
                    err.args[2]
                    == "could not determine a constructor for the tag '!!python/tuple'"
                ):
                    with open(path, "r") as ymlfile:
                        cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
                        write_config_horse(configname, cfg)
                else:
                    raise

    else:
        raise FileNotFoundError(
            "Config file is not found. Please make sure that the file exists and/or that you passed the path of the config file correctly!"
        )
    return cfg

def write_config_horse(configname, cfg):
    """
    Write structured config file.
    """
    with open(configname, "w") as cf:
        cfg_file, ruamelFile = create_config_template_horse()
        for key in cfg.keys():
            cfg_file[key] = cfg[key]
            
        ruamelFile.dump(cfg_file, cf)

def create_header_configs():
    return {
        "Nom": "horse_name",
        "Père": "horse_father",
        "Mère": "horse_mother",
        "Propriétaire": "horse_owner",
        "Vendeur": "horse_seller",
        "Acheteur": "horse_buyer",
        "Type de Parcours": "horse_type",
        "Date": "date",
        "Emplacement": "project_path",
        "Video": "video_path",
        "Type de video": "video_type"
    }
    
def create_headers():
    return ["Nom", "Père", "Mère", "Propriétaire", "Vendeur", "Acheteur", "Type de Parcours", "Date", "Emplacement", "Video", "Type de video"]