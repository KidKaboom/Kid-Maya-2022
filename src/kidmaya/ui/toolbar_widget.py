# :coding: utf-8

# Project Modules
from kid.__version__ import VERSION
from kid.core import KObject, KDebug
from kidmaya.ui.dock import Dock, MayaQWidgetDockableMixin
from kidqt.__qt__ import *
from kidmaya.tools.command_test import CommandTest


# Python Modules


class ToolbarWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Menu
        self.menubar = QMenuBar()
        self.file_menu = QMenu("File")
        self.menubar.addMenu(self.file_menu)
        self.edit_menu = QMenu("Edit")
        self.menubar.addMenu(self.edit_menu)
        self.help_menu = QMenu("Help")
        self.menubar.addMenu(self.help_menu)
        layout.setMenuBar(self.menubar)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.add_tab("Test")

        # Slots
        pass

    def add_tab(self, title):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        widget.setLayout(layout)
        scroll.setWidget(widget)

        self.tabs.addTab(scroll, title)

        # button = QPushButton()
        # button.setText("Test")
        # button.setIcon(QIcon(CommandTest.icon()))
        # # button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # # button.setSizePolicy( QSizePolicy( QSizePolicy.Policy.Expanding, button.sizePolicy().verticalPolicy() ) )
        # button.clicked.connect(CommandTest.do_it)
        # layout.addWidget(button)

        # button = ToolbarButton()
        # button.set_name(CommandTest.name())
        # button.set_description(CommandTest.description())
        # button.set_command(CommandTest.do_it)
        # layout.addWidget(button)
        return
