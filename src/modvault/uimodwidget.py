
import urllib.request, urllib.error, urllib.parse

from PyQt5 import QtCore, QtWidgets

import modvault
import util

FormClass, BaseClass = util.THEME.loadUiType("modvault/uimod.ui")


class UIModWidget(FormClass, BaseClass):
    FORMATTER_UIMOD = str(util.THEME.readfile("modvault/uimod.qthtml"))

    def __init__(self, parent, *args, **kwargs):
        BaseClass.__init__(self, *args, **kwargs)

        self.setupUi(self)
        self.parent = parent

        util.THEME.stylesheets_reloaded.connect(self.load_stylesheet)
        self.load_stylesheet()

        self.setWindowTitle("Ui Mod Manager")

        self.doneButton.clicked.connect(self.doneClicked)
        self.modList.itemEntered.connect(self.hoverOver)
        allmods = modvault.getInstalledMods()
        self.uimods = {}
        for mod in allmods:
            if mod.ui_only:
                self.uimods[mod.totalname] = mod
                self.modList.addItem(mod.totalname)

        names = [mod.totalname for mod in modvault.getActiveMods(uimods=True)]
        for name in names:
            l = self.modList.findItems(name, QtCore.Qt.MatchExactly)
            if l:
                l[0].setSelected(True)

        if len(self.uimods) != 0:
            self.hoverOver(self.modList.item(0))

    def load_stylesheet(self):
        self.setStyleSheet(util.THEME.readstylesheet("client/client.css"))

    @QtCore.pyqtSlot()
    def doneClicked(self):
        selected_mods = [self.uimods[str(item.text())] for item in self.modList.selectedItems()]
        succes = modvault.setActiveMods(selected_mods, False)
        if not succes:
            QtWidgets.QMessageBox.information(None, "Error", "Could not set the active UI mods. Maybe something is "
                                                             "wrong with your game.prefs file. Please send your log.")
        self.done(1)

    @QtCore.pyqtSlot(QtWidgets.QListWidgetItem)
    def hoverOver(self, item):
        mod = self.uimods[str(item.text())]
        self.modInfo.setText(self.FORMATTER_UIMOD.format(name=mod.totalname, description=mod.description))
