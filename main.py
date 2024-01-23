from PyQt5 import QtWidgets as qt
from app import Window
import PyQt5
import sys
import os

from PyQt5.QtCore import QLibraryInfo

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())