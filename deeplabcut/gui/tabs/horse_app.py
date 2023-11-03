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
from functools import cached_property


class HorseApp(DefaultTab):
    config_loaded = QtCore.Signal()
    
    def __init__(self, root, parent, h1_description):
        super().__init__(root, parent, h1_description)
        self._val_pattern = QRegularExpression(r"(\d{3,5},\s*)+\d{3,5}")
        self.root = root
        self.config = None
        self.loaded = False
        self.recentfiles = []
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

        self.run_button = QtWidgets.QPushButton("Démarrer l'analyse")
        self.run_button.clicked.connect(self.run_video_adaptation)
        self.main_layout.addWidget(self.run_button, alignment=Qt.AlignRight)
        
    def open_create_video_modal(self):
        dlg = HorseProjectCreator(self.root, self)
        dlg.show()

    def run_video_adaptation(self):
        videos = list(self.files)
        if not videos:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("You must select a video file")
            msg.setWindowTitle("Error")
            msg.setMinimumWidth(400)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return

        supermodel_name = parse_available_supermodels().keys()[0] if parse_available_supermodels().keys()[0] else 'superanimal_quadruped'

        deeplabcut.video_inference_superanimal(
            videos,
            supermodel_name,
            video_adapt=True
        )
    
    @property
    def cfg(self):
        try:
            cfg = auxiliaryfunctions_horse.read_config_horse(self.config)
        except TypeError:
            cfg = {}
        return cfg
    
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
            
    def add_recent_filename(self, filename):
        if filename in self.recentfiles:
            return
        self.recentfiles.append(filename)
        
    def load_settings(self):
        print('Load settings...')
        filenames = self.settings["recent_files_paths"] or []
        print(f'Load settings { filenames }')
        for filename in filenames:
            self.add_recent_filename(filename)
        print(f"settings loaded : { self.recentfiles }")