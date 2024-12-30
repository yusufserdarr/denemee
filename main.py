import sys
from PyQt5.QtWidgets import QApplication
from ui_setup import UiMainWindow
import matplotlib
matplotlib.use('Qt5Agg')

def main():
    app = QApplication(sys.argv)
    window = UiMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 