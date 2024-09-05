import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QPushButton
import re

class FileScannerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python File Scanner")
        self.setGeometry(100, 100, 800, 600)
        self.keylogger_found = []
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        self.browse_button = QtWidgets.QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_button_clicked)
        layout.addWidget(self.browse_button)

        self.text = QtWidgets.QTextEdit(self)
        layout.addWidget(self.text)

        self.status_label = QtWidgets.QLabel(self)
        layout.addWidget(self.status_label)

        self.progress_bar = QtWidgets.QProgressBar(self)
        layout.addWidget(self.progress_bar)

    def scan_python_files(self, directory):
        scanned_files = []
        total_size = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    scanned_files.append(file_path)
                    #print(scanned_files)
                    total_size += os.path.getsize(file_path)

        for file_path in scanned_files:
            self.text.append(f"{file_path}")
            print(file_path)
            self.call_check(file_path)

        self.status_label.setText(f"Scanning complete. Total Size: {total_size / (1024 * 1024):.2f} MB")
        self.progress_bar.setValue(100)
        self.open_second_window()

    def browse_button_clicked(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.text.clear()
            self.status_label.clear()

            self.progress_bar.setValue(0)
            self.scan_python_files(directory)

    def detect_keylogger_code(self,script_content):
        keylogger_patterns = [
            r'import\s+pynput\.keyboard',
            r'import\s+smtplib\b',
            r'server\s*=\s*smtplib\.SMTP\("smtp\.gmail\.com"\)'
        ]
        matches = [re.search(pattern, script_content) for pattern in keylogger_patterns]
        return all(match is not None for match in matches)

    def call_check(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.script_content = file.read()

            if self.detect_keylogger_code(self.script_content):
                print("Keylogger code detected!")
                self.keylogger_found.append(file_path)
            else:
                print("Keylogger code not found.")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading the file: {e}")

    def open_second_window(self):
        # Create an instance of the second window
        second_window = SecondWindow(self.keylogger_found)
        second_window.exec_()

class SecondWindow(QDialog):
    def __init__(self,keylog):
        super(SecondWindow, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.keylog_list = keylog
        layout = QVBoxLayout()
        self.text = QtWidgets.QTextEdit(self)
        layout.addWidget(self.text)
        self.button = QtWidgets.QPushButton("Keep", self)
        self.button.clicked.connect(self.keep)
        layout.addWidget(self.button)
        self.button_1 = QtWidgets.QPushButton("Delete", self)
        self.button_1.clicked.connect(self.cont)
        layout.addWidget(self.button_1)
        self.setLayout(layout)
        self.print()

    def print(self):
        i = int(len(self.keylog_list))
        j = int(0)
        while j<i:
            self.text.append(self.keylog_list[j])
            j=j+1

    def cont(self):
        i = int(len(self.keylog_list))
        j = int(0)
        while j < i:
            self.delete(self.keylog_list[j])
            j = j + 1

    def delete(self,file_path):
        print(file_path)
        try:
            os.remove(file_path)
            print(f"File '{file_path}' deleted successfully.")
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def keep(self):
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = FileScannerApp()
    window.show()
    app.exec_()
