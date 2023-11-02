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
import os
from datetime import datetime

import deeplabcut
from deeplabcut.utils import auxiliaryfunctions
from deeplabcut.gui import BASE_DIR
from deeplabcut.gui.dlc_params import DLCParams
from deeplabcut.gui.widgets import ClickableLabel
from deeplabcut.gui.components import SingleVideoSelectionWidget

from deeplabcut.gui.components import (
    _create_button_widget,
)

from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QIcon


class HorseProjectCreator(QtWidgets.QDialog):
    video_type_ = QtCore.Signal(str)
    video_file_ = QtCore.Signal(str)
    
    def __init__(self, root: QtWidgets.QMainWindow, parent: QtWidgets.QWidget):
        super(HorseProjectCreator, self).__init__(parent)
        self.root = root
        self.parent = parent
        
        self.videotype = "mp4"
        self.files = ""
        
        self.setWindowTitle("Enregistrer un cheval")
        self.setModal(True)
        self.setMinimumWidth(parent.screen_width // 2)
        today = datetime.today().strftime("%Y-%m-%d")
        self.name_default = "-".join(("{}", "{}", today))
        self.horse_name_default = ""
        self.horse_father_default = ""
        self.horse_mother_default = ""
        self.horse_owner_default = ""
        self.horse_owner_default = ""
        self.horse_seller_default = ""
        self.horse_buyer_default = ""
        self.loc_default = parent.project_folder

        main_layout = QtWidgets.QVBoxLayout(self)
        self.horse_frame = self.lay_out_horse_frame()
        self.video_frame = self.lay_out_video_frame()
        self.create_button = self.create_video_button = _create_button_widget("Enregistrer", height=20, width=155)
        self.create_button.setDefault(True)
        self.create_button.clicked.connect(self.finalize_project)
        main_layout.addWidget(self.horse_frame)
        main_layout.addWidget(self.video_frame)
        main_layout.addWidget(self.create_button, alignment=QtCore.Qt.AlignRight)

    def lay_out_horse_frame(self):
        horse_frame = QtWidgets.QFrame(self)
        horse_frame.setFrameShape(horse_frame.Shape.StyledPanel)
        horse_frame.setLineWidth(0)

        horse_name_label = QtWidgets.QLabel("Nom:", horse_frame)
        self.horse_name_line = QtWidgets.QLineEdit(self.horse_name_default, horse_frame)
        self.horse_name_line.setPlaceholderText("le nom du cheval")
        self._default_style = self.horse_name_line.styleSheet()
        self.horse_name_line.textEdited.connect(self.update_horse_name)

        horse_owner_label = QtWidgets.QLabel("Propriétaire:", horse_frame)
        self.horse_owner_line = QtWidgets.QLineEdit(self.horse_owner_default, horse_frame)
        self.horse_owner_line.setPlaceholderText("le nom de son propriétaire")
        self.horse_owner_line.textEdited.connect(self.update_owner_name)
        
        horse_father_label = QtWidgets.QLabel("Père:", horse_frame)
        self.horse_father_line = QtWidgets.QLineEdit(self.horse_father_default, horse_frame)
        self.horse_father_line.setPlaceholderText("le nom de son père")
        self.horse_father_line.textEdited.connect(self.update_horse_father_name)
        
        horse_mother_label = QtWidgets.QLabel("Mère:", horse_frame)
        self.horse_mother_line = QtWidgets.QLineEdit(self.horse_mother_default, horse_frame)
        self.horse_mother_line.setPlaceholderText("le nom de sa mère")
        self.horse_mother_line.textEdited.connect(self.update_horse_mother_name)
        
        horse_seller_label = QtWidgets.QLabel("Vendeur:", horse_frame)
        self.horse_seller_line = QtWidgets.QLineEdit(self.horse_seller_default, horse_frame)
        self.horse_seller_line.setPlaceholderText("le nom de son vendeur")
        self.horse_seller_line.textEdited.connect(self.update_horse_seller_name)
        
        horse_buyer_label = QtWidgets.QLabel("Acheteur:", horse_frame)
        self.horse_buyer_line = QtWidgets.QLineEdit(self.horse_buyer_default, horse_frame)
        self.horse_buyer_line.setPlaceholderText("le nom de son acheteur")
        self.horse_buyer_line.textEdited.connect(self.update_horse_buyer_name)

        loc_label = ClickableLabel("Emplacement des résultats:", parent=horse_frame)
        loc_label.signal.connect(self.on_click)
        self.loc_line = QtWidgets.QLineEdit(self.loc_default, horse_frame)
        self.loc_line.setReadOnly(True)
        action = self.loc_line.addAction(
            QIcon(os.path.join(BASE_DIR, "assets", "icons", "open2.png")),
            QtWidgets.QLineEdit.TrailingPosition,
        )
        action.triggered.connect(self.on_click)

        vbox = QtWidgets.QVBoxLayout(horse_frame)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(horse_name_label, 0, 0)
        grid.addWidget(self.horse_name_line, 0, 1)
        grid.addWidget(horse_owner_label, 1, 0)
        grid.addWidget(self.horse_owner_line, 1, 1)
        grid.addWidget(horse_father_label, 2, 0)
        grid.addWidget(self.horse_father_line, 2, 1)
        grid.addWidget(horse_mother_label, 3, 0)
        grid.addWidget(self.horse_mother_line, 3, 1)
        grid.addWidget(horse_seller_label, 4, 0)
        grid.addWidget(self.horse_seller_line, 4, 1)
        grid.addWidget(horse_buyer_label, 5, 0)
        grid.addWidget(self.horse_buyer_line, 5, 1)
        grid.addWidget(loc_label, 6, 0)
        grid.addWidget(self.loc_line, 6, 1)
        vbox.addLayout(grid)

        return horse_frame

    def lay_out_video_frame(self):
        video_frame = QtWidgets.QFrame(self)

        self.horse_video_type_combo = QtWidgets.QComboBox(video_frame)
        self.horse_video_type_combo.addItems(map(str, (DLCParams.HORSETYPES[0], DLCParams.HORSETYPES[1], DLCParams.HORSETYPES[2])))
        self.horse_video_type_combo.currentTextChanged.connect(self.check_horse_video_type)
        horse_video_type_label = QtWidgets.QLabel("Catégorie de parcour:", video_frame)
        horse_video_type_label.setBuddy(self.horse_video_type_combo)

        self.copy_box = QtWidgets.QCheckBox("Copier la vidéo dans le dossier des résultats d'analyse ?", video_frame)
        self.copy_box.setChecked(False)

        vbox = QtWidgets.QVBoxLayout(video_frame)
        layout1 = QtWidgets.QHBoxLayout()
        layout1.addWidget(horse_video_type_label)
        layout1.addWidget(self.horse_video_type_combo)
        vbox.addLayout(layout1)

        self.video_selection_widget = SingleVideoSelectionWidget(self.root, self)
        vbox.addWidget(self.video_selection_widget)

        vbox.addWidget(self.copy_box)

        return video_frame

    def finalize_project(self):
        fields = [self.horse_name_line, self.owner_line]
        empty = [i for i, field in enumerate(fields) if not field.text()]
        for i, field in enumerate(fields):
            if i in empty:
                field.setStyleSheet("border: 1px solid red;")
            else:
                field.setStyleSheet(self._default_style)
        if empty:
            return

        horse_video_type = self.horse_video_type_combo.currentText()
        try:
            videos = list(self.video_frame.selected_items)
            if not len(videos):
                print("Add at least a video to the project.")
                self.video_frame.fancy_list.setStyleSheet("border: 1px solid red")
                return
            else:
                self.video_frame.fancy_list.setStyleSheet(
                    self.video_frame.fancy_list._default_style
                )
                """ config = deeplabcut.create_new_project(
                    self.proj_default,
                    self.exp_default,
                    videos,
                    self.loc_default,
                    to_copy,
                    multianimal=is_madlc,
                )
                self.parent.load_config(config)
                self.parent._update_project_state(
                    config=config,
                    loaded=True,
                ) """ 
        except FileExistsError:
            print('Project "{}" already exists!'.format(self.horse_name_default))
            return

        msg = QtWidgets.QMessageBox(text=f"New project created")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.exec_()

        self.close()

    def on_click(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Veuillez choisir un dossier", self.loc_default
        )
        if not dirname:
            return
        self.loc_default = dirname
        self.update_project_location()

    def check_horse_video_type(self, text):
        self.horse_video_type = text

    def update_horse_name(self, text):
        self.horse_name_default = text
        self.update_project_location()

    def update_owner_name(self, text):
        self.horse_owner_default = text
        self.update_project_location()
        
    def update_horse_father_name(self, text):
        self.horse_father_default = text
        
    def update_horse_mother_name(self, text):
        self.horse_mother_default = text
        
    def update_horse_seller_name(self, text):
        self.horse_seller_default = text
    
    def update_horse_buyer_name(self, text):
        self.horse_buyer_default = text

    def update_project_location(self):
        full_name = self.name_default.format(self.horse_name_default, self.horse_owner_default)
        full_path = os.path.join(self.loc_default, full_name)
        self.loc_line.setText(full_path)
        
    @property
    def video_type(self):
        return self.videotype

    @video_type.setter
    def video_type(self, ext):
        self.videotype = ext
        self.video_type_.emit(ext)
    
    @property
    def video_file(self):
        return self.file

    @video_file.setter
    def video_file(self, video_file):
        self.file = video_file
        self.video_file_.emit(self.file)
    
