import sys
from datetime import datetime

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from pyqtgraph.dockarea import *

from src.application_tracker.classes.application import ApplicationStatus, Application


class ApplicationModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data
        self._cols = dict(zip([xx for xx in range(len(self._data[0]))], list(self._data[0].keys())))

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return 14

    def data(self, index, role=QtCore.Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.ItemDataRole.DisplayRole:
                return str(self._data[index.row()][self._cols[index.column()]])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Orientation.Horizontal and role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._cols[col].replace("_"," ").title().replace("Poc","Point of Contact").replace("Id","ID")
        return None


class LoginPopup(QtWidgets.QWidget):
    def __init__(self, parent, application: Application, update: bool):
        super().__init__(parent)
        self.application = application
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_StyledBackground)
        self.setAutoFillBackground(True)
        self.setStyleSheet(
            """
            LoginPopup {
                background: rgba(64, 64, 64, 64);
            }
            QWidget#container {
                border: 2px solid darkGray;
                border-radius: 4px;
                background: rgb(64, 64, 64);
            }
            QWidget#container > QLabel {
                color: white;
            }
            QLabel#title {
                font-size: 20pt;
            }
            QPushButton#close {
                color: white;
                font-weight: bold;
                background: none;
                border: 1px solid gray;
            }
        """
        )

        full_layout = QtWidgets.QVBoxLayout(self)

        self.container = QtWidgets.QWidget(
            autoFillBackground=True, objectName="container"
        )
        full_layout.addWidget(self.container, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.container.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum
        )

        button_size = self.fontMetrics().height()
        self.close_button = QtWidgets.QPushButton(
            "×", self.container, objectName="close"
        )
        self.close_button.setFixedSize(button_size, button_size)
        self.close_button.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self.container)
        layout.setContentsMargins(
            button_size * 2, button_size, button_size * 2, button_size
        )

        title = QtWidgets.QLabel(
            "Enter New Application" if not update else "Update Existing Application",
            objectName="title",
            alignment=QtCore.Qt.AlignmentFlag.AlignCenter,
        )
        layout.addWidget(title)

        # Fields
        # Application ID
        layout.addWidget(QtWidgets.QLabel("Application ID"))
        self.app_id = QtWidgets.QLineEdit()
        self.app_id.setText(self.application.application_id)
        layout.addWidget(self.app_id)

        # Company
        layout.addWidget(QtWidgets.QLabel("Company"))
        self.company = QtWidgets.QLineEdit()
        self.company.setText(self.application.company)
        layout.addWidget(self.company)

        # Hiring Manager
        layout.addWidget(QtWidgets.QLabel("Hiring Manager"))
        self.hiring_manager = QtWidgets.QLineEdit()
        self.hiring_manager.setText(self.application.hiring_manager)
        layout.addWidget(self.hiring_manager)

        # POC
        layout.addWidget(QtWidgets.QLabel("Point of Contact"))
        self.poc = QtWidgets.QLineEdit()
        self.poc.setText(self.application.poc)
        layout.addWidget(self.poc)

        # Job Description Link
        layout.addWidget(QtWidgets.QLabel("Job Description Link"))
        self.job_desc_link = QtWidgets.QLineEdit()
        self.job_desc_link.setText(self.application.job_description_link)
        layout.addWidget(self.job_desc_link)

        # Application Portal Link
        layout.addWidget(QtWidgets.QLabel("Application Portal Link"))
        self.app_portal = QtWidgets.QLineEdit()
        self.app_portal.setText(self.application.application_portal_link)
        layout.addWidget(self.app_portal)

        # Application Date
        layout.addWidget(QtWidgets.QLabel("Application Date"))
        self.app_date = QtWidgets.QDateEdit()
        self.app_date.setDate(self.application.application_date if self.application.application_date is not None
                                  else QtCore.QDate.currentDate())
        layout.addWidget(self.app_date)

        # Follow-up Date
        layout.addWidget(QtWidgets.QLabel("Application Date"))
        self.follow_up_date = QtWidgets.QDateEdit()
        self.follow_up_date.setDate(self.application.follow_up_date if self.application.follow_up_date is not None
                              else QtCore.QDate.currentDate().addDays(3))
        layout.addWidget(self.follow_up_date)

        # Status
        layout.addWidget(QtWidgets.QLabel("Status"))
        self.status = QtWidgets.QComboBox()
        self.status.addItems([e.value for e in ApplicationStatus])
        layout.addWidget(self.status)

        # Interviewed bool
        layout.addWidget(QtWidgets.QLabel("Interviewed"))
        self.interviewed = QtWidgets.QComboBox()
        self.interviewed.addItems(["True", "False"])
        self.interviewed.setCurrentText(str(self.application.interviewed) if self.application.interviewed is not None
                                         else "False")
        layout.addWidget(self.interviewed)

        # Number of Interviews
        layout.addWidget(QtWidgets.QLabel("Number of Interviews"))
        self.no_interviews = QtWidgets.QLineEdit()
        self.no_interviews.setText(self.application.no_interviews)
        layout.addWidget(self.no_interviews)

        # Salary Range
        layout.addWidget(QtWidgets.QLabel("Salary Range"))
        self.salary_range = QtWidgets.QLineEdit()
        self.salary_range.setText(self.application.salary_range)
        layout.addWidget(self.salary_range)

        # Proposed Salary
        layout.addWidget(QtWidgets.QLabel("Proposed Salary"))
        self.prop_salary = QtWidgets.QLineEdit()
        self.prop_salary.setText(self.application.proposed_salary)
        layout.addWidget(self.prop_salary)

        # Buttons
        # Okay/Cancel Buttons
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Access the OK button directly
        ok_button = button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Accept")

        # Access the Cancel button directly
        cancel_button = button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("Decline")

        # Add the button box to the dialog layout
        layout.addWidget(button_box)

        parent.installEventFilter(self)

        self.loop = QtCore.QEventLoop(self)
        self.app_id.setFocus()

    def ret_fields(self):
        return self.application

    def accept(self):
        self.application.application_id = self.app_id.text()
        self.application.company = self.company.text()
        self.application.hiring_manager = self.hiring_manager.text()
        self.application.poc = self.poc.text()
        self.application.job_description_link = self.job_desc_link.text()
        self.application.application_portal_link = self.app_portal.text()
        self.application.application_date = datetime.strptime(
            self.app_date.text(), "%m/%d/%Y"
        ).date()
        self.application.follow_up_date = datetime.strptime(
            self.follow_up_date.text(), "%m/%d/%Y"
        ).date()
        self.application.status = ApplicationStatus(self.status.currentText()).name
        self.application.interviewed = (
            True if self.interviewed.currentText() == "True" else False
        )
        self.application.no_interviews = self.no_interviews.text()
        self.application.salary_range = self.salary_range.text()
        self.application.proposed_salary = self.prop_salary.text()
        self.application.save_application()
        self.loop.exit(True)

    def reject(self):
        self.loop.exit(False)

    def close(self):
        self.loop.quit()

    def showEvent(self, event):
        self.setGeometry(self.parent().rect())

    def exec_(self):
        self.show()
        self.raise_()
        res = self.loop.exec()
        self.hide()
        return res


class DockArea(DockArea):
    def makeContainer(self, typ):
        new = super(DockArea, self).makeContainer(typ)
        new.setChildrenCollapsible(False)
        return new


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Initial Setup
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.applications = Application.load_applications()

        # Add Table
        self.table = QtWidgets.QTableView()
        self.update_table_model()

        # Buttons
        # Add Application
        self.add_app = QtWidgets.QPushButton(self)
        self.add_app.setText("Add Application")
        self.add_app.clicked.connect(self.add_application)

        # Update Application
        self.up_app = QtWidgets.QPushButton(self)
        self.up_app.setText("Update Application")
        self.up_app.clicked.connect(self.update_application)

        # Delete Application
        self.del_app = QtWidgets.QPushButton(self)
        self.del_app.setText("Delete Application")
        self.del_app.clicked.connect(self.delete_application)

        # Exit Button
        self.exit_b = QtWidgets.QPushButton(self)
        self.exit_b.setText("Exit")
        self.exit_b.clicked.connect(self.close)

        # Formatting Dock Area
        layout.addWidget(self.table)
        layout.addWidget(self.add_app)
        layout.addWidget(self.up_app)
        layout.addWidget(self.del_app)
        layout.addWidget(self.exit_b)
        self.setGeometry(100, 100, 900, 600)

    def update_table_model(self):
        self.model = ApplicationModel([app.as_dict() for app in self.applications.values()])
        self.table.setModel(self.model)

    def add_application(self):
        self.show_dialog(update=False)

    def update_application(self):
        row_index = self.table.currentIndex().siblingAtColumn(0)
        internal_app_id = row_index.data()
        temp_app = self.applications[internal_app_id]
        self.show_dialog(application=temp_app,update=True)

    def delete_application(self):
        row_index = self.table.currentIndex().siblingAtColumn(0)
        internal_app_id = row_index.data()
        del self.applications[internal_app_id]
        Application().save_applications(applications=self.applications)
        self.update_table_model()

    def show_dialog(self, application: Application = Application(), update: bool = False):
        dialog = LoginPopup(self, application=application, update=update)
        if dialog.exec_():
            output = dialog.ret_fields()
            self.applications[output.internal_app_id] = output
            self.update_table_model()


def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.setWindowTitle("Application Tracker")
    win.show()
    sys.exit(app.exec())
