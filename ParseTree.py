from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class Ui_ParseTree(object):
    def setupUi(self, ParseTree):
        # Set up the main window
        ParseTree.setWindowTitle("Parse Tree")
        ParseTree.setGeometry(100, 100, 400, 300)

        # Create a central widget and set the layout
        central_widget = QWidget(ParseTree)
        ParseTree.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a QLabel to display the image
        ParseTree.image_label = QLabel(ParseTree)
        layout.addWidget(ParseTree.image_label)

        # Load and set the image
        self.load_image("syntax_tree.png", ParseTree)  # Replace with the path to your image file

    def load_image(self, path, ParseTree):
        # Load the image using QPixmap
        pixmap = QPixmap(path)

        # Set the image to the QLabel
        ParseTree.image_label.setPixmap(pixmap)
        ParseTree.image_label.setScaledContents(True)

    def retranslateUi(self, ParseTree):
        _translate = QtCore.QCoreApplication.translate
        ParseTree.setWindowTitle(_translate("ParseTree", "MainWindow"))
        self.label.setText(_translate("ParseTree", "graphiz photo"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParseTree = QtWidgets.QMainWindow()
    ui = Ui_ParseTree()
    ui.setupUi(ParseTree)
    ParseTree.show()
    sys.exit(app.exec_())
