# :coding: utf-8

# Project Modules
from kid.core import KObject, KDebug
from kidqt.__qt__ import *


# Python Modules


class ToolbarButton(QWidget, KObject):
    ICON_DEFAULT = ":/mayaIcon.png"
    ICON_SHELF = ":/saveToShelf.png"
    ICON_HELP = ":/help.png"

    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self._name = str()
        self._command = None

        # Layout
        layout = QHBoxLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Buttons
        self.button = QPushButton("Test")
        self.button.setStyleSheet("text-align:left;")
        self.button.setIcon(QIcon(self.ICON_DEFAULT))
        self.button.setContextMenuPolicy(Qt.CustomContextMenu)
        layout.addWidget(self.button)

        self.shelf_button = QPushButton()
        self.shelf_button.setIcon(QIcon(self.ICON_SHELF))
        self.shelf_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.shelf_button)

        self.help_button = QPushButton()
        self.help_button.setIcon(QIcon(self.ICON_HELP))
        self.help_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(self.help_button)

        # Slots
        self.button.clicked.connect(self.command_callback)
        self.button.customContextMenuRequested.connect(self.pop_menu_callback)
        self.shelf_button.clicked.connect(self.shelf_callback)
        self.help_button.clicked.connect(self.help_callback)

    def name(self):
        return self.button.text()

    def set_name(self, value):
        self.button.setText(value)
        self.help_button.setToolTip("Help {}.".format(value))
        self.shelf_button.setToolTip("Add {} to shelf.".format(value))
        return

    def description(self):
        return self.button.toolTip()

    def set_description(self, value):
        self.button.setToolTip(value)
        return

    def command(self):
        return self._command

    def set_command(self, value):
        self._command = value
        return

    def as_dict(self):
        result = {
            "name"       : self.name(),
            "description": self.description(),
            "command"    : self.command(),
            }
        return result

    def is_valid(self):
        if self.name():
            if self._command != str() or self._command is not None:
                return True

        return False

    def command_callback(self):
        if not self.is_valid():
            KDebug.error("Command not found.")
            return

        if callable(self._command):
            try:
                self._command()
            except Exception as _error:
                KDebug.error(_error)
                return
        elif isinstance(self._command, str):
            try:
                eval(self._command)
            except Exception as _error:
                KDebug.error(_error)
                return
        else:
            KDebug.error("Unable to run command.")
        return

    def shelf_callback(self):
        if not self.is_valid():
            KDebug.error("Command not found.")
            return
        return

    def help_callback(self):
        return

    def pop_menu_callback(self, position):
        """ Context Menu for the button.

        Args:
            position(int)

        Returns:
            None
        """
        menu = QMenu()

        hide_action = menu.addAction('Hide')
        # hide_action.setIcon(QIcon(self.ICON_DEFAULT))
        menu.addSeparator()
        shelf_action = menu.addAction('Add {} To Shelf'.format(self.name()))
        shelf_action.setIcon(QIcon(self.ICON_SHELF))
        help_action = menu.addAction('{} Help'.format(self.name()))
        help_action.setIcon(QIcon(self.ICON_HELP))

        action = menu.exec_(self.mapToGlobal(position))

        if action == hide_action:
            pass
        elif action == shelf_action:
            self.shelf_callback()
        elif action == help_action:
            self.help_callback()

        return
