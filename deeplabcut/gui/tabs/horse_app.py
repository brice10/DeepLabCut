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
import deeplabcut
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QRegularExpression
from deeplabcut.gui.components import (
    DefaultTab,
    VideoCreationWidget,
    _create_label_widget,
)
from deeplabcut import auxiliaryfunctions_horse, auxiliaryfunctions_settings
from deeplabcut.gui.tabs import HorseProjectCreator
from deeplabcut.modelzoo.utils import parse_available_supermodels
from deeplabcut.gui.widgets import TableWidget


class HorseApp(DefaultTab):
    config_loaded = QtCore.Signal()
    
    def __init__(self, root, parent, h1_description):
        super().__init__(root, parent, h1_description)
        self._val_pattern = QRegularExpression(r"(\d{3,5},\s*)+\d{3,5}")
        self.root = root
        self.config = None
        self.loaded = False
        self.recentfiles = []
        self.horse_list_loaded = []
        self.load_settings()
        self._set_page()

    @property
    def files(self):
        return self.video_creation_widget.files
    
    # It should work first
    @property
    def screen_width(self):
        return self.root.screen_width
    
    @property
    def project_folder(self):
        return self.root.project_folder

    def _set_page(self):
        self.main_layout.addWidget(_create_label_widget("Formulaire d'enregistrement des chevaux", "font:bold"))
        self.video_creation_widget = VideoCreationWidget(self.root, self)
        self.main_layout.addWidget(self.video_creation_widget)

        self.table_widget = TableWidget(self, self.table_headers, self.horse_list_loaded, self.table_header_configs, action_btn=True)
        self.main_layout.addWidget(self.table_widget)

    def open_create_video_modal(self):
        dlg = HorseProjectCreator(self.root, self)
        dlg.show()

    def run_video_adaptation(self, video_path, video_type=".mp4", dest_folder=None):
        videos = [video_path]
        if not videos:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Vous devez sélectionner une vidéo pour l'analyse")
            msg.setWindowTitle("Error")
            msg.setMinimumWidth(400)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return

        available_supermodels = parse_available_supermodels()
        available_supermodels_keys_list = list(available_supermodels.keys())
        supermodel_name = available_supermodels_keys_list[0] if available_supermodels_keys_list[0] else 'superanimal_quadruped'

        deeplabcut.video_inference_superanimal(
            videos,
            supermodel_name,
            video_adapt=True,
            videotype=video_type,
            dest_folder=dest_folder
        )
    
    @property
    def cfg(self):
        try:
            cfg = auxiliaryfunctions_horse.read_config_horse(self.config)
        except TypeError:
            cfg = {}
        return cfg
    
    def get_horse_line(self, config_file):
        try:
            line = auxiliaryfunctions_horse.read_config_horse(config_file)
        except TypeError:
            line = {}
        return line
    
    @property
    def settings(self):
        try:
            settings = auxiliaryfunctions_settings.read_config_settings()
        except TypeError:
            settings = {}
        return settings
        
    def load_config(self, config):
        self.config = config
        self.config_loaded.emit()
        print(f'Horse "{self.cfg["horse_name"]}" successfully loaded.')

    def _update_project_state(self, config, loaded):
        self.config = config
        self.loaded = loaded
        if loaded:
            self.add_recent_filename(self.config)
            auxiliaryfunctions_settings.save_settings(self.recentfiles)
            self.table_widget.add_row(len(self.table_widget.table_data), self.get_horse_line(self.config))
            
    def add_recent_filename(self, filename):
        if filename in self.recentfiles:
            return
        self.recentfiles.append(filename)
        
    def load_settings(self):
        filenames = self.settings["recent_files_paths"] or []
        for filename in filenames:
            self.add_recent_filename(filename)
        self.horse_list_loaded = self.build_horse_list()
        
    def build_horse_list(self):
        data = []
        for config_file in self.recentfiles:
            data.append(self.get_horse_line(config_file))
        return data
    
    @property
    def table_headers(self):
        return auxiliaryfunctions_horse.create_headers()
    
    @property
    def table_header_configs(self):
        return auxiliaryfunctions_horse.create_header_configs()
    
    def action_button_clicked(self, row):
        print(f"Analyse du cheval: { row['horse_name'] }")
        self.run_video_adaptation(row['video_path'], row['video_type'], dest_folder=row['project_path'])
    