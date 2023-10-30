import sys
import typing
from PyQt5 import QtGui

import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
from PyQt5.QtWidgets import QWidget

import base
import file_management as file


WINDOW_HEIGHT = 720
WINDOW_WIDTH = 960
PLUS_ICON = file.os.path.join(file.PARENT, "resources\plus.png")
MINUS_ICON = file.os.path.join(file.PARENT, "resources\minus.png")

class OpenRPGDialog(widgets.QDialog):
    def __init__(self, parent: QWidget | None = ...) -> None:

        super().__init__(parent)

        file.update_global_data()

        self.setWindowTitle("Open RPG")
        self.isModal = True
        self.setGeometry(core.QRect(640, 480, 144, 96))
        self.setObjectName("open_rpg_dialog")

        self.central_layout = widgets.QVBoxLayout(self)

        global_data = file.load_global_data()

        games_list: list[dict] = global_data["games"]

        self.game_list = widgets.QTableWidget(len(games_list), 2)
        
        self.game_list.setEditTriggers(widgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.game_list.setHorizontalHeaderLabels(games_list[0].keys())
        self.game_list.setSelectionBehavior(widgets.QAbstractItemView.SelectionBehavior.SelectRows)

        row = 0

        for ele in games_list:
            self.game_list.setItem(row, 0, widgets.QTableWidgetItem(ele["name"]))
            self.game_list.setItem(row, 1, widgets.QTableWidgetItem(ele["path"]))

            row += 1


        btns = widgets.QDialogButtonBox.Ok | widgets.QDialogButtonBox.Cancel

        self.button_box = widgets.QDialogButtonBox(btns)
        self.ok_button = widgets.QPushButton("Ok")
        self.ok_button.setObjectName("ok_button")

        self.cancel_button = widgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")

        self.central_layout.addWidget(self.game_list)
        self.bottom_horizontal_layout_widget = widgets.QWidget()
        self.bottom_horizontal_layout = widgets.QHBoxLayout(self.bottom_horizontal_layout_widget)
        self.central_layout.addWidget(self.bottom_horizontal_layout_widget)


        self.bottom_horizontal_layout.addSpacing(32)
        self.bottom_horizontal_layout.addWidget(self.button_box)

        self.make_connections()

    def make_connections(self):
        self.button_box.accepted.connect(self.ok_button_pressed)
        self.button_box.rejected.connect(self.cancel_button_pressed)
        self.game_list.itemClicked.connect(self.item_clicked)

    def item_clicked(self, item: widgets.QTableWidgetItem):
        self.game_name = self.game_list.item(item.row(), 0).text()
        self.game_path = self.game_list.item(item.row(), 1).text()

    def ok_button_pressed(self):
        self.accept()

    def cancel_button_pressed(self):
        self.reject()


class CreateRPGDialog(widgets.QDialog):
    def __init__(self, parent: QWidget | None = ...) -> None:

        super().__init__(parent)

        self.setWindowTitle("New RPG")
        self.isModal = True
        self.setGeometry(core.QRect(640, 480, 144, 96))
        self.setObjectName("new_rpg_dialog")

        self.central_layout = widgets.QVBoxLayout(self)

        self.rpg_name_label = widgets.QLabel("RPG Name: ")
        self.rpg_name_label.setObjectName("rpg_name_label")

        self.rpg_name_entry = widgets.QLineEdit()
        self.rpg_name_entry.setObjectName("rpg_name_entry")
        

        btns = widgets.QDialogButtonBox.Ok | widgets.QDialogButtonBox.Cancel

        self.button_box = widgets.QDialogButtonBox(btns)
        self.ok_button = widgets.QPushButton("Ok")
        self.ok_button.setObjectName("ok_button")

        self.cancel_button = widgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")

        self.top_horizontal_layout_widget = widgets.QWidget()
        self.top_horizontal_layout = widgets.QHBoxLayout(self.top_horizontal_layout_widget)
        self.central_layout.addWidget(self.top_horizontal_layout_widget)
        self.bottom_horizontal_layout_widget = widgets.QWidget()
        self.bottom_horizontal_layout = widgets.QHBoxLayout(self.bottom_horizontal_layout_widget)
        self.central_layout.addWidget(self.bottom_horizontal_layout_widget)

        self.top_horizontal_layout.addWidget(self.rpg_name_label)
        self.top_horizontal_layout.addWidget(self.rpg_name_entry)
        self.bottom_horizontal_layout.addSpacing(32)
        self.bottom_horizontal_layout.addWidget(self.button_box)

        self.make_connections()

    def make_connections(self):
        self.button_box.accepted.connect(self.ok_button_pressed)
        self.button_box.rejected.connect(self.cancel_button_pressed)

    def ok_button_pressed(self):
        self.rpg_name = self.rpg_name_entry.text()
        self.accept()

    def cancel_button_pressed(self):
        self.reject()


class MainWindow(widgets.QMainWindow):
    def __init__(self):

        super().__init__()

        self.setObjectName("main")
        self.setWindowTitle("RPG Of You")
        self.setGeometry(core.QRect(480, 240, WINDOW_WIDTH, WINDOW_HEIGHT))

        self.menubar = self.menuBar()
    
        self.menuFile = self.menubar.addMenu("File")
        self.menuFile.setObjectName("menuFile")

        self.menuAttributes = self.menubar.addMenu("Attributes")
        self.menuAttributes.setObjectName("menuAttributes")

        self.menuActions = self.menubar.addMenu("Actions")
        self.menuActions.setObjectName("menuActions")

        self.menuEntities = self.menubar.addMenu("Entities")
        self.menuEntities.setObjectName("menuEntities")


        self.new_rpg_action = widgets.QAction("&New RPG")
        self.menuFile.addAction(self.new_rpg_action)

        self.save_rpg_action = widgets.QAction("&Save RPG")
        self.menuFile.addAction(self.save_rpg_action)

        self.open_rpg_action = widgets.QAction("&Open RPG")
        self.menuFile.addAction(self.open_rpg_action)

        self.menuFile.addSeparator()

        self.close_rpg_action = widgets.QAction("&Close RPG")
        self.menuFile.addAction(self.close_rpg_action)

        self.new_attribute_action = widgets.QAction("&New Attribute")
        self.menuAttributes.addAction(self.new_attribute_action)

        self.new_action_action = widgets.QAction("&New Action")
        self.menuActions.addAction(self.new_action_action)

        self.new_entity_action = widgets.QAction("&New Entity")
        self.menuEntities.addAction(self.new_entity_action)

        self.active_game = None

        self.make_connections()

    def create_rpg(self):
        dialog: CreateRPGDialog = CreateRPGDialog(self)
        result = dialog.exec()
        if result == 1:
            new_name = dialog.rpg_name
            print("New game '{}' created.\n".format(new_name))
            self.active_game = base.TRPG(new_name)
            file.save_game(self.active_game)
            self.load_active_game()

        elif result == 0:
            print("Operation cancelled.\n")

    def load_active_game(self):
        print("Attempting to load active game...\n")
        if not isinstance(self.active_game, base.TRPG):
            print("Failure: No active game available.\n")

        else:
            self.loaded_game_tab = TabBarWidget(self.active_game)
            self.setCentralWidget(self.loaded_game_tab)

    def open_rpg(self):
        dialog = OpenRPGDialog(self)
        result = dialog.exec()
        if result == 1:
            path = dialog.game_path

            self.active_game = file.load_game(path)
            self.load_active_game()

        elif result == 0:
            print("Operation cancelled.\n")

    def save_rpg(self):
        print("Attempting save game...\n")
        if not isinstance(self.active_game, base.TRPG):
            print("Failed: No active game available.\n")
        
        else:
            file.save_game(self.active_game)   

    def close_rpg(self):
        self.save_rpg()
        self.active_game = None   

    def make_connections(self):
        self.new_rpg_action.triggered.connect(self.create_rpg)
        self.open_rpg_action.triggered.connect(self.open_rpg)
        self.save_rpg_action.triggered.connect(self.save_rpg)
        self.close_rpg_action.triggered.connect(self.close_rpg)


class TabBarWidget(widgets.QTabWidget):
    def __init__(self, active_game: base.TRPG, parent = None) -> None:

        super().__init__(parent)

        self.active_game = active_game

        self.attribute_tab = AttributeTab(self.active_game)
        self.action_tab = ActionTab(self.active_game)
        self.addTab(self.attribute_tab, "Attributes")
        self.addTab(self.action_tab, "Actions")


class AttributeTab(widgets.QWidget):
    def __init__(self, active_game: base.TRPG, parent = None) -> None:
        super().__init__(parent)

        self.active_game = active_game

        self.layout_widget = widgets.QHBoxLayout(self)

        self.attribute_list_widget = widgets.QListWidget()

        self.attribute_list_widget.clear()

        for ele in self.active_game.attributes:
            self.attribute_list_widget.addItem(ele)

        self.new_attribute_button = widgets.QPushButton(gui.QIcon(PLUS_ICON), None, None)

        self.delete_attribute_button = widgets.QPushButton(gui.QIcon(MINUS_ICON), None, None)


        self.attribute_name_lineedit_widget = widgets.QLineEdit()

        self.attribute_name_label_widget = widgets.QLabel("Attribute Name: ")


        self.attribute_type_combobox_widget = widgets.QComboBox()

        for ele in ["Number", "Word", "Boolean"]:
            self.attribute_type_combobox_widget.addItem(ele)

        self.attribute_type_label_widget = widgets.QLabel("Attribute Type: ")

        self.new_attribute_accept_button = widgets.QPushButton("Ok")

        self.button_layout_widget = widgets.QHBoxLayout()

        self.form_layout_widget = widgets.QFormLayout()

        self.layout_widget.addWidget(self.attribute_list_widget)
        self.layout_widget.addLayout(self.button_layout_widget)
        self.layout_widget.addLayout(self.form_layout_widget)

        self.button_layout_widget.addWidget(self.new_attribute_button)
        self.button_layout_widget.addWidget(self.delete_attribute_button)

        self.form_layout_widget.addRow(self.attribute_name_label_widget, self.attribute_name_lineedit_widget)
        self.form_layout_widget.addRow(self.attribute_type_label_widget, self.attribute_type_combobox_widget)
        self.form_layout_widget.addWidget(self.new_attribute_accept_button)

        self.new_attribute_accept_button.hide()

        self.make_connections()

    def attribute_list_item_clicked(self, item: widgets.QListWidgetItem):
        self.attribute_name_lineedit_widget.clear()
        self.attribute_name_lineedit_widget.insert(item.text())

        if self.active_game.get_attribute(item.text()).get_value_type() == "num":
            self.attribute_type_combobox_widget.setCurrentIndex(0)

        elif self.active_game.get_attribute(item.text()).get_value_type() == "alpha":
            self.attribute_type_combobox_widget.setCurrentIndex(1)

        elif self.active_game.get_attribute(item.text()).get_value_type() == "bool":
            self.attribute_type_combobox_widget.setCurrentIndex(2)

    def new_attribute_button_clicked(self):
        
        self.new_attribute_accept_button.show()

        self.attribute_name_lineedit_widget.clear()
        self.attribute_type_combobox_widget.setCurrentIndex(0)
        
        self.attribute_name_lineedit_widget.focusWidget()

    def new_attribute_accept_button_clicked(self):
        
        attribute_name = self.attribute_name_lineedit_widget.text()
        attribute_type = None

        if self.attribute_type_combobox_widget.currentIndex() == 0:
            attribute_type = "num"
            
        elif self.attribute_type_combobox_widget.currentIndex() == 1:
            attribute_type = "alpha"

        elif self.attribute_type_combobox_widget.currentIndex() == 2:
            attribute_type = "bool"
        
        
        self.active_game.new_attribute(attribute_name, attribute_type)
        self.attribute_list_widget.addItem(attribute_name)

        self.new_attribute_accept_button.hide()

    def make_connections(self):
        self.attribute_list_widget.itemClicked.connect(self.attribute_list_item_clicked)
        self.new_attribute_button.clicked.connect(self.new_attribute_button_clicked)
        self.new_attribute_accept_button.clicked.connect(self.new_attribute_accept_button_clicked)


class ActionTab(widgets.QWidget):
    def __init__(self, active_game: base.TRPG, parent = None) -> None:
        super().__init__(parent)

        self.active_game = active_game

        self.layout_widget = widgets.QHBoxLayout(self)

        self.action_list_widget = widgets.QListWidget()

        self.action_list_widget.clear()

        for ele in self.active_game.actions:
            self.action_list_widget.addItem(ele)

        self.new_action_button = widgets.QPushButton(gui.QIcon(PLUS_ICON), None, None)

        self.delete_action_button = widgets.QPushButton(gui.QIcon(MINUS_ICON), None, None)


        self.action_name_lineedit_widget = widgets.QLineEdit()

        self.action_name_label_widget = widgets.QLabel("Action Name: ")
        
        self.action_effects_label_widget = widgets.QLabel("Action Effect: ")

        self.action_effects_table_widget = widgets.QTableWidget()

        self.action_effects_table_widget.setColumnCount(4)
        self.action_effects_table_widget.setHorizontalHeaderLabels(["Attribute Affected", "Target Type", "Modifier", "Value"])

        self.commit_button = widgets.QPushButton("Ok")

        self.button_layout_widget = widgets.QHBoxLayout()

        self.form_layout_widget = widgets.QFormLayout()
        

        self.layout_widget.addWidget(self.action_list_widget)
        self.layout_widget.addLayout(self.button_layout_widget)
        self.layout_widget.addLayout(self.form_layout_widget)

        self.button_layout_widget.addWidget(self.new_action_button)
        self.button_layout_widget.addWidget(self.delete_action_button)

        self.form_layout_widget.addRow(self.action_name_label_widget, self.action_name_lineedit_widget)
        self.form_layout_widget.addRow(self.action_effects_label_widget, self.action_effects_table_widget)
        self.form_layout_widget.addWidget(self.commit_button)

        self.commit_button.hide()

        self.make_connections()

    def attribute_list_item_clicked(self, item: widgets.QListWidgetItem):
        self.attribute_name_lineedit_widget.clear()
        self.attribute_name_lineedit_widget.insert(item.text())

        effects_list = self.active_game.get_action(item.text()).get_effects()

        self.action_effects_table_widget.setRowCount(len(effects_list))

        row = 0
        for ele in effects_list:
            effect_attribute_combo_box = widgets.QComboBox()
            effect_attribute_combo_box.addItems(self.active_game.attributes.keys())
            effect_attribute_combo_box.setCurrentText(ele.attribute)   

            effect_type_combo_box = widgets.QComboBox()
            effect_type_combo_box.addItems(base.TARGETS)
            effect_type_combo_box.setCurrentText(ele.effect_type)

            effect_modifier_combo_box = widgets.QComboBox()
            effect_modifier_combo_box.addItems(base.OPERATORS)
            effect_modifier_combo_box.setCurrentText(ele.modifier)

            effect_value_line_edit = widgets.QLineEdit()
            if not isinstance(ele.value, base.AttrBasedValStruct):
                effect_value_line_edit.setText(str(ele.value))

            self.action_effects_table_widget.setCellWidget(row, 0, effect_attribute_combo_box)
            self.action_effects_table_widget.setCellWidget(row, 1, effect_type_combo_box)
            self.action_effects_table_widget.setCellWidget(row, 2, effect_modifier_combo_box)
            self.action_effects_table_widget.setCellWidget(row, 3, effect_value_line_edit)

    def delete_action_button_clicked(self):
        current = self.action_list_widget.currentItem()
        self.action_list_widget.removeItemWidget(current)

        self.active_game.remove_action(current.text())

    def action_effect_changed(self, e: widgets.QTableWidgetItem):

        self.commit_button.show()

    def new_action_button_clicked(self):
        
        self.commit_button.show()

        self.action_name_lineedit_widget.clear()
        self.action_effects_table_widget.clearContents()
        
        self.action_name_lineedit_widget.focusWidget()

    #def new_action_accept_button_clicked(self):
        

    def make_connections(self):
        self.new_action_button.clicked.connect(self.new_action_button_clicked)
        self.delete_action_button.clicked.connect(self.delete_action_button_clicked)
        self.action_list_widget.clicked.connect(self.attribute_list_item_clicked)


def test_GUI():
    app = widgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())