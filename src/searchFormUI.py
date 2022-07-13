import os
import sys
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import *
from WaitingScreenUI import WaitingScreenUI

from filterDB import filterDB


class Window(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MDB files Search")

        self.setGeometry(200, 100, 400, 400)

        self.formGroupBox = QGroupBox("Search Form")

        self.useBirthDateCheckBox = QCheckBox("Use Birth Date")
        self.useBirthDateCheckBox.toggled.connect(self.useBirthDateCheckBoxOnClicked)

        self.birthDateGroupBox = QGroupBox("Birth Date")
        self.birthDateGroupBox.setEnabled(False)

        self.fromBirthDate = QDateEdit()
        self.fromBirthDate.setDate(QDate(1900, 1, 1))
        self.toBirthDate = QDateEdit()
        self.toBirthDate.setDate(QDate(2100, 12, 31))

        self.useSIMActivationDateCheckBox = QCheckBox("Use SIM Activation Date")
        self.useSIMActivationDateCheckBox.toggled.connect(self.useSIMActivationDateCheckBoxOnClicked)

        self.SIMActivationDateGroupBox = QGroupBox("SIM Activation Date")
        self.SIMActivationDateGroupBox.setEnabled(False)

        self.fromSIMActivationDate = QDateEdit()
        self.fromSIMActivationDate.setDate(QDate(1900, 1, 1))
        self.toSIMActivationDate = QDateEdit()
        self.toSIMActivationDate.setDate(QDate(2100, 12, 31))

        self.genderComboBox = QComboBox()

        self.genderComboBox.addItems(["", "Male", "Female"])

        self.subscriberNameEdit = QLineEdit()
        self.subscriberStatusEdit = QLineEdit()
        self.conectionStatusEdit = QLineEdit()
        self.fatherHusbandNameEdit = QLineEdit()
        self.localAddressEdit = QLineEdit()
        self.permanentAddressEdit = QLineEdit()
        self.emailEdit = QLineEdit()

        self.telephoneNumberEdit = QLineEdit()

        self.telephoneNumberEdit.setValidator(QIntValidator())

        self.alternateTelephoneNumberEdit = QLineEdit()

        self.alternateTelephoneNumberEdit.setValidator(QIntValidator())

        self.addressNumberEdit = QLineEdit()

        self.addressNumberEdit.setValidator(QIntValidator())

        self.createForm()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok
                                          | QDialogButtonBox.Cancel)

        self.buttonBox.accepted.connect(self.getInfo)

        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.formGroupBox)

        mainLayout.addWidget(self.buttonBox)

        self.setLayout(mainLayout)


    def useBirthDateCheckBoxOnClicked(self):
        self.birthDateGroupBox.setEnabled(self.useBirthDateCheckBox.isChecked())

    def useSIMActivationDateCheckBoxOnClicked(self):
        self.SIMActivationDateGroupBox.setEnabled(self.useSIMActivationDateCheckBox.isChecked())

    def getInfo(self):

        info = {"addressNumber": self.addressNumberEdit.text(),
                "alternateTelephoneNumber": self.alternateTelephoneNumberEdit.text(),
                "toBirthDate": self.toBirthDate.text(),
                "fromBirthDate": self.fromBirthDate.text(),
                "conectionStatus": self.conectionStatusEdit.text(),
                "email": self.emailEdit.text(),
                "fatherHusbandName": self.fatherHusbandNameEdit.text(),
                "fromSIMActivationDate": self.fromSIMActivationDate.text(),
                "toSIMActivationDate": self.toSIMActivationDate.text(),
                "gender": self.genderComboBox.currentText(),
                "localAddress": self.localAddressEdit.text(),
                "permanentAddress": self.permanentAddressEdit.text(),
                "subscriberName": self.subscriberNameEdit.text(),
                "telephoneNumber": self.telephoneNumberEdit.text(),
                "subscriberStatus": self.subscriberStatusEdit.text(),
                "useBirthDate": self.useBirthDateCheckBox.isChecked(),
                "useSIMActivationDate": self.useSIMActivationDateCheckBox.isChecked()}

        self.waitingScreen = WaitingScreenUI()
        self.hide()
        self.waitingScreen.show()
        filterDB(info)
        self.selectDirectory()
        self.waitingScreen.hide()
        self.show()

    def selectDirectory(self):
        outputFileExists = os.path.exists("../Data/query result/results.csv")

        if(outputFileExists):
            dir_path = QFileDialog.getExistingDirectory(
                self, "Choose Directory")

            if dir_path:
                if(outputFileExists):
                    shutil.copy("../Data/query result/results.csv",
                                f'{dir_path}/results.csv')

        else:
            self.waitingScreen.hide()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("your inputs has no result")
            msgBox.setWindowTitle("No Data Found")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()

    def createForm(self):

        layout = QFormLayout()

        layout.addRow(QLabel("Subscriber Name"), self.subscriberNameEdit)
        layout.addRow(QLabel("Subscriber Status"), self.subscriberStatusEdit)
        layout.addRow(QLabel("Conection Status"), self.conectionStatusEdit)
        layout.addRow(QLabel("Telephone Number"), self.telephoneNumberEdit)
        layout.addRow(QLabel("Alternate Telephone Number"),
                      self.alternateTelephoneNumberEdit)
        layout.addRow(QLabel("Email"), self.emailEdit)
        layout.addRow(QLabel("Address Number"), self.addressNumberEdit)
        layout.addRow(QLabel("Local Address"), self.localAddressEdit)
        layout.addRow(QLabel("Permanent Address"), self.permanentAddressEdit)

        layout.addRow(QLabel("Gender"), self.genderComboBox)
        layout.addRow(self.useBirthDateCheckBox)

        boxLayout = QHBoxLayout()
        boxLayout.addWidget(QLabel("From"))
        boxLayout.addWidget(self.fromBirthDate)
        boxLayout.addWidget(QLabel("To"))
        boxLayout.addWidget(self.toBirthDate)
        self.birthDateGroupBox.setLayout(boxLayout)

        layout.addRow(self.birthDateGroupBox)
        
        layout.addRow(self.useSIMActivationDateCheckBox)


        boxLayout = QHBoxLayout()
        boxLayout.addWidget(QLabel("From"))
        boxLayout.addWidget(self.fromSIMActivationDate)
        boxLayout.addWidget(QLabel("To"))
        boxLayout.addWidget(self.toSIMActivationDate)
        self.SIMActivationDateGroupBox.setLayout(boxLayout)

        layout.addRow(self.SIMActivationDateGroupBox)

        self.formGroupBox.setLayout(layout)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec())
