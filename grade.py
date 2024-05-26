import sys
from PyQt6.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QIntValidator

# Importing the UI and database connection classes
from main_ui import Ui_Form
from connect_database import ConnectDatabase

# Create a main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the UI from a separate UI file (created using Qt Designer)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Create a database connection object
        self.db = ConnectDatabase()

        # Connect UI elements to class variables
        self.grade = self.ui.lineEdit_4
        self.subject = self.ui.comboBox

        self.add_btn = self.ui.add_btn
        self.update_btn = self.ui.update_btn
        self.search_btn = self.ui.search_btn
        self.clear_btn = self.ui.clear_btn
        self.delete_btn = self.ui.delete_btn

        self.result_table = self.ui.tableWidget
        self.result_table.setSortingEnabled(False)
        self.buttons_list = self.ui.function_frame.findChildren(QPushButton)

        # Initialize signal-slot connections
        self.init_signal_slot()

        # Populate the initial data in the table and subject dropdown
        self.search_info()
        self.update_subject()

    def init_signal_slot(self):
        # Connect buttons to their respective functions
        self.add_btn.clicked.connect(self.add_info)
        self.search_btn.clicked.connect(self.search_info)
        self.clear_btn.clicked.connect(self.clear_form_info)
        self.delete_btn.clicked.connect(self.delete_info)

    def disable_buttons(self):
        # Disable all buttons
        for button in self.buttons_list:
            button.setDisabled(True)

    def enable_buttons(self):
        # Enable all buttons
        for button in self.buttons_list:
            button.setDisabled(False)

    def add_info(self):
        # Function to add grade information
        self.disable_buttons()

        grade_info = self.get_grade_info()

        if grade_info["grade"] and grade_info["subject"]:
            add_result = self.db.add_info(grade=grade_info["grade"],
                                          subject=grade_info["subject"])

            if add_result:
                QMessageBox.information(self, "Warning", f"Add fail: {add_result}, Please try again.",
                                        QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please input grade and subject.",
                                    QMessageBox.StandardButton.Ok)

        self.search_info()
        self.enable_buttons()

    def search_info(self):
        # Function to search for grade information and populate the table
        self.update_subject()
        grade_info = self.get_grade_info()

        search_result = self.db.search_info(
            grade=grade_info["grade"],
            subject=grade_info["subject"]
        )

        self.show_data(search_result)

    def clear_form_info(self):
        # Function to clear the form
        self.update_subject()
        self.grade.clear()
        self.subject.setCurrentText("")

    def delete_info(self):
        # Function to delete grade information
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Warning", "Are you Sure to delete it?",
                                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                subject = self.result_table.item(select_row, 0).text().strip()
                grade = self.result_table.item(select_row, 1).text().strip()

                delete_result = self.db.delete_info(subject, grade)

                if not delete_result:
                    self.search_info()
                else:
                    QMessageBox.information(self, "Warning",
                                            f"Fail to delete the information: {delete_result}. Please try again.",
                                            QMessageBox.StandardButton.Ok)

        else:
            QMessageBox.information(self, "Warning", "Please select one grade information to delete",
                                    QMessageBox.StandardButton.Ok)

    def show_data(self, result):
        # Function to populate the table with grade information
        if result:
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info["subject"],
                    info["grade"],
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)

        else:
            self.result_table.setRowCount(0)
            return

    def get_grade_info(self):
        # Function to retrieve grade information from the form
        grade = self.grade.text().strip()
        subject = self.subject.currentText().strip()

        grade_info = {
            "grade": grade,
            "subject": subject,
        }

        return grade_info

    def update_subject(self):
        # Function to populate the subject dropdown
        subject_result = self.db.get_all_subjects()

        self.subject.clear()

        subject_list = [""]
        for item in subject_result:
            for k, v in item.items():
                if v != "":
                    subject_list.append(v)

        if len(subject_list) > 1:
            self.subject.addItems(subject_list)

# Application entry point
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
