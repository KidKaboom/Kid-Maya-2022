# :coding: utf-8

# Project Modules
from kidqt.__qt__ import *

# Python Modules
import os

# Maya Modules
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import maya.cmds as cmds


class IconDelegate(QStyledItemDelegate):
    def __init__(self, icon_dir, icons, model, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.icons = icons
        self.icon_dir = icon_dir
        self.model = model

    def paint(self, painter, option, index):

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        painter.save()
        index = self.model.mapToSource(index)

        png = str()

        if self.icon_dir == 'Internal Icons':
            png = ':/%s' % self.icons[index.row()]
        else:
            png = os.path.join(str(self.icon_dir), self.icons[index.row()])

        pixmap = QPixmap(png)

        # option.rect.setSize(pixmap.size())

        if pixmap.width() > 32:
            pixmap = pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        rect = option.rect
        offsetX = (rect.width() - pixmap.width()) / 2
        offsetY = (rect.height() - pixmap.height()) / 2

        painter.drawPixmap(rect.x() + offsetX, rect.y() + offsetY, pixmap)

        painter.restore()
        return


class IconModel(QAbstractListModel):
    def __init__(self, icon_dir, icons):
        QAbstractListModel.__init__(self)
        self.icons = icons
        self.icon_dir = icon_dir

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.icons)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            pass
        elif role == Qt.ToolTipRole:
            return self.icons[index.row()]

        elif role == Qt.DecorationRole:
            if self.icon_dir == 'Internal Icons':
                cc = ':/%s' % self.icons[index.row()]
            else:
                cc = os.path.join(str(self.icon_dir), self.icons[index.row()])

            label = QLabel()
            pixmap = QPixmap(cc)

            # pixmap = pixmap.scaled(32,32,Qt.KeepAspectRatio,Qt.SmoothTransformation)

            label.setPixmap(pixmap)
            # return pixmap
            return label

        else:
            return None


class IconDatabaseWidget(MayaQWidgetBaseMixin, QWidget):
    def __init__(self, parent=None):
        MayaQWidgetBaseMixin.__init__(self, parent=parent)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Default Icons
        self.default_icons = cmds.resourceManager(nameFilter="*.png")

        # Search Box
        self.search = QLineEdit()
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText("Search")
        self.search.setFocusPolicy(Qt.ClickFocus)
        layout.addWidget(self.search)

        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search.setCompleter(self.completer)
        self.search_model = QStringListModel()
        self.search_model.setStringList(self.default_icons)
        self.completer.setModel(self.search_model)

        # List View
        self.view = QListView()
        self.view.setUniformItemSizes(True)
        self.view.setViewMode(QListView.IconMode)
        self.view.setResizeMode(QListView.Adjust)
        layout.addWidget(self.view)

        # List Model
        self.model = IconModel("Internal Icons", self.default_icons)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterRole(Qt.ToolTipRole)
        self.view.setModel(self.proxy_model)

        # List Delegate
        self.delegate = IconDelegate("Internal Icons", self.default_icons, self.proxy_model)
        self.view.setItemDelegate(self.delegate)

        # Slots
        self.view.clicked.connect(self.select)
        self.search.textChanged.connect(self.search_changed)

    def select(self, index):
        name = index.model().data(index, Qt.ToolTipRole)
        print(name)
        # self.label.setText(name.toPyObject())
        return

    def search_changed(self, text):
        search = QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp)
        self.proxy_model.setFilterRegExp(search)
        return


if __name__ == '__main__':
    widget = IconDatabaseWidget()
    widget.show()
