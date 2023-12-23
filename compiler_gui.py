from typing import List

from tiny_parser import Parser
from scanner import scan
import gui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys


class appGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.run_app)
        self.ui.pushButton_2.clicked.connect(self.upload_file)
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setText("Error")

    def showdialog(self, text):
        self.error_dialog.setInformativeText(text)
        self.error_dialog.exec_()

    def upload_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QtCore.QDir.Files)
        if dialog.exec():
            files = dialog.selectedFiles()
            if files[0].endswith('.txt'):
                with open(files[0], 'r') as file:
                    tokens_list = file.read()
                    self.ui.textEdit.setPlainText(tokens_list)
                    file.close()
            else:
                self.ui.textEdit.setText("")
                self.showdialog('Wrong File Format!')

    def run_app(self):
        text = self.ui.textEdit.toPlainText()
        if text == '':
            self.showdialog('No tokens found!')
        else:
            try:
                if self.ui.radioButton.isChecked():
                    tokens_list = scan(text)

                elif self.ui.radioButton_2.isChecked():
                    tokens = text.split('\n')
                    tokens_list = []
                    for i in tokens:
                        row = i.split(',')
                        row[0] = row[0].strip()
                        row[1] = row[1].strip()
                        tokens_list.append(row)

                parser = Parser(tokens_list)
                parser.stmt_sequence()
                if parser.counter < parser.max_counter:
                    raise Exception("error")

                self.ui.openWindow()

            except Exception as e:
                if str(e) == "No match found":
                    self.showdialog("Grammar Error!")
                else:
                    self.showdialog("Syntax Error!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    styleSheet = "styles.css"
    with open(styleSheet, "r") as f:
        app.setStyleSheet(f.read())
    gui = appGui()
    gui.show()
    sys.exit(app.exec_())
