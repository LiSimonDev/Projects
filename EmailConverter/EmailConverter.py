import sys
import imaplib
import email
from email.header import decode_header
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIntValidator, QTextCursor

class Help(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
        self.text = QtWidgets.QTextEdit("")
        self.text.setReadOnly(True)
        with open("help.html", 'r') as f:
            self.text.textCursor().insertHtml(f.read())
        self.text.setFont(QFont(self.font().family(), 13))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.setGeometry(0, 0, 600, 500)
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.text.moveCursor(QTextCursor.Start)

class IMAP(QObject):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(list)
    def __init__(self, username, password, imap_server, folder, number_of_messages, fields, content_field):
        super().__init__()
        self.username = str(username)
        self.password = str(password)
        self.imap_server = str(imap_server)
        self.folder = str(folder)
        self.number_of_messages = int(number_of_messages)
        self.fields = fields
        self.content_field = bool(content_field)

    def get_data(self):
        imap = imaplib.IMAP4_SSL(self.imap_server)
        imap.login(self.username, self.password)
        status, messages = imap.select(self.folder)
        messages = int(messages[0])
        n = 5

        if self.number_of_messages != "":
            n = int(self.number_of_messages)
        if n > messages:
            n = messages
        data = {}

        for i in range(messages, messages - n, -1):
            data[str(i)] = {}
            try:
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # parse from bytes to object
                        msg = email.message_from_bytes(response[1])
                        # save data from message
                        for name in self.fields:
                            value, encoding = decode_header(str(msg.get(name)))[0]
                            # if value is in bytes decode
                            if isinstance(value, bytes):
                                value = value.decode(encoding)
                            data[str(i)][name] = value
                        # if message content is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode("utf-8", "replace")
                                except Exception as a:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # save text and ignore attachments
                                    if self.content_field:
                                        data[str(i)]["Content"] = body
                        # if message is one part
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode("utf-8", "replace")
                            if content_type == "text/plain":
                                # save text and ignore attachments
                                if self.content_field:
                                    data[str(i)]["Content"] = body
                    # send signal to main thread, to increase progress bar
                    self.progress.emit([messages+1-i,n])

            except Exception as e:
                #login again in case of lost connection or timeout
                imap = imaplib.IMAP4_SSL(self.imap_server)
                imap.login(self.username, self.password)
                status, messages = imap.select(self.folder)
                messages = int(messages[0])
                continue

        # close the connection and logout
        imap.close()
        imap.logout()
        # send extracted data to main thread
        self.finished.emit(data)


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # decides if content of e-mail should be download as well
        self.content_field = False
        self.setWindowTitle("EmailConverter")

        self.info_objects = []
        self.fields_objects = []

        styles_file = "styles.css"

        self.fields = []
        self.folder = "INBOX"

        self.cr = ""
        self.br = ""

        self.help_window = Help()

        # login objects
        self.website_text = QtWidgets.QLabel("IMAP server")
        self.website = QtWidgets.QLineEdit("")
        self.username_text = QtWidgets.QLabel("Username")
        self.username = QtWidgets.QLineEdit("")
        self.password_text = QtWidgets.QLabel("Password")
        self.password = QtWidgets.QLineEdit("")
        self.proceed = QtWidgets.QPushButton("Login")
        self.number_of_messages_text = QtWidgets.QLabel("No. of messages (max: 0)")
        self.number_of_messages = QtWidgets.QLineEdit()
        self.download = QtWidgets.QPushButton("Download")
        self.progress = QtWidgets.QProgressBar()

        # main layout
        self.for_menu = QtWidgets.QVBoxLayout(self)
        self.menubar = QtWidgets.QMenuBar()
        self.help = self.menubar.addMenu("Help")
        self.help.addAction("Open")
        self.help.triggered[QtWidgets.QAction].connect(self.activate_help)
        self.menubar.setMaximumHeight(22)
        self.for_menu.addWidget(self.menubar)
        self.background_layout = QtWidgets.QHBoxLayout(self)
        self.for_menu.addLayout(self.background_layout)

        self.login_layout = QtWidgets.QVBoxLayout(self)
        self.login_layout.setAlignment(Qt.AlignTop)
        self.background_layout.addLayout(self.login_layout)

        # login layout
        self.login_layout.addWidget(self.website_text)
        self.login_layout.addWidget(self.website)
        self.login_layout.addWidget(self.username_text)
        self.login_layout.addWidget(self.username)
        self.login_layout.addWidget(self.password_text)
        self.login_layout.addWidget(self.password)
        self.login_layout.addWidget(self.proceed)
        self.login_layout.addWidget(self.number_of_messages_text)
        self.login_layout.addWidget(self.number_of_messages)
        self.login_layout.addWidget(self.download)
        self.login_layout.addWidget(self.progress)


        # info objects
        self.info1 = QtWidgets.QLabel("------------------------------FOLDERS------------------------------")

        # info layout
        self.realmScroll2 = QtWidgets.QScrollArea(self)
        self.realmScroll2.setWidgetResizable(True)

        labelsContainer2 = QtWidgets.QWidget()
        self.realmScroll2.setWidget(labelsContainer2)
        self.info_layout = QtWidgets.QVBoxLayout(labelsContainer2)
        self.info_layout.setAlignment(Qt.AlignTop)
        self.background_layout.addWidget(self.realmScroll2)
        self.info_layout.addWidget(self.info1)

        # options objects
        self.option1 = QtWidgets.QLabel("------------------------------FIELDS------------------------------")

        # fields layout
        self.realmScroll = QtWidgets.QScrollArea(self)
        self.realmScroll.setWidgetResizable(True)

        labelsContainer = QtWidgets.QWidget()
        self.realmScroll.setWidget(labelsContainer)
        self.options_layout = QtWidgets.QVBoxLayout(labelsContainer)
        self.options_layout.setAlignment(Qt.AlignTop)
        self.background_layout.addWidget(self.realmScroll)

        self.options_layout.addWidget(self.option1)

        self.proceed.clicked.connect(self.login)
        self.download.clicked.connect(self.start_download)
        self.download.setDisabled(True)
        self.onlyInt = QIntValidator()
        self.number_of_messages.setValidator(self.onlyInt)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.number_of_messages_text_original = "No. of messages"


        with open(styles_file, "r") as f:
            self.setStyleSheet(f.read())

    def start_download(self):
        self.download.setDisabled(True)
        # make new thread
        self.thread = QThread()
        # create object of imap download class
        self.worker = IMAP(self.username.text(), self.password.text(), self.website.text(), self.folder, self.number_of_messages.text(), self.fields, self.content_field)
        # move object to new thread
        self.worker.moveToThread(self.thread)
        # connect progress and finished signals
        self.thread.started.connect(self.worker.get_data)
        self.worker.finished.connect(self.backup_to_csv)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_bar)
        # start thread
        self.thread.start()


    def update_bar(self, data):
        self.progress.setValue(int((data[0] / data[1]) * 100))

    def backup_to_csv(self, data):
        self.download.setDisabled(False)
        export = ""
        # make columns names in csv
        for msg in data:
            for column in data[msg].keys():
                export += column
                export += ";"
            export = export[:-1]
            export += "\n"
            break

        # insert saved data into csv
        for msg in data:
            for field in data[msg].keys():
                txt = str(data[msg][field]).replace("\n", self.br)
                txt = txt.replace("\r", self.cr)
                txt = txt.replace(";", ",")
                export += txt
                export += ";"
            export = export[:-1]
            export += "\n"
        try:
            # make text file with utf-8 encoding
            with open("saved.txt", 'w', encoding='utf-8') as f:
                f.write(export)
                self.operation_successful("converting to csv file")
        except Exception as a:
            self.raise_error(a)
        self.download.setDisabled(False)

    def login(self):
        # try/except in case of connection error
        try:
            print(1)
            username = self.username.text()
            password = self.password.text()
            imap_server = self.website.text()
            imap = imaplib.IMAP4_SSL(imap_server)
            imap.login(username, password)
            status, messages = imap.select("INBOX")
            print(2)
            fields = []
            folders = imap.list()
            messages = int(messages[0])
            n = 1
            print(3)
            # download 1 (n) message to check what fields inbox messages has
            for i in range(messages, messages - n, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
                print(4)
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        fields = msg.keys()
            self.set_info(folders, fields)
            self.operation_successful("login")
            self.download.setDisabled(False)
            self.proceed.setDisabled(True)
            self.website.setDisabled(True)
            self.username.setDisabled(True)
            self.password.setDisabled(True)
            print(5)
        except Exception as e:
            print("e")
            self.raise_error(e)

    # make folders buttons and delete old ones
    def set_info(self, folders, fields):
        # delete old buttons
        for i in reversed(range(self.info_layout.count())):
            widget_to_remove = self.info_layout.itemAt(i).widget()
            self.info_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        self.info1 = QtWidgets.QLabel("------------------------------FOLDERS------------------------------")
        self.info_layout.addWidget(self.info1)
        # index of folder name in imap.list() split with \
        index = None
        for f in folders[1]:
            text = str(f)
            chunks = text.split("\" ")
            # if index does not exist, find that index
            if index is None:
                for i in range(len(chunks)):
                    text = chunks[i]
                    # delete ' and " from end
                    while text[-1] == '\"' or text[-1] == '\'':
                        text = text[:-1]
                    # delete ' and " from start
                    while text[0] == '\"' or text[0] == '\'':
                        text = text[1:]
                    # check if folder is accessible
                    if self.check_folder(text):
                        index = i
                        # index found, stop looking
                        break
            text = chunks[index]
            while text[-1] == '\"' or text[-1] == '\'':
                text = text[:-1]
            while text[0] == '\"' or text[0] == '\'':
                text = text[1:]
            text = "\"" + text + "\""
            if not self.check_folder(text):
                continue
            # make new folder button
            new_folder_info = QtWidgets.QRadioButton(text)
            new_folder_info.pressed.connect(self.set_folder)
            self.info_objects.append(new_folder_info)
            self.info_layout.addWidget(new_folder_info)

        self.show_fields(fields)

    # make fields buttons and delete old ones
    def show_fields(self, fields):
        self.fields = []
        # delete old buttons
        for i in reversed(range(self.options_layout.count())):
            widget_to_remove = self.options_layout.itemAt(i).widget()
            self.options_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)
        self.option1 = QtWidgets.QLabel("------------------------------FIELDS------------------------------")
        self.options_layout.addWidget(self.option1)
        # make new buttons and activate some of them
        for f in fields:
            new_fields_info = QtWidgets.QCheckBox(str(f))
            new_fields_info.pressed.connect(self.set_fields)
            self.fields_objects.append(new_fields_info)
            self.options_layout.addWidget(new_fields_info)
            # buttons to activate
            if f in ["Date", "From", "To", "Subject", "Organization"]:
                new_fields_info.click()

        # add content buttons at last
        new_fields_info = QtWidgets.QCheckBox(str("Content"))
        new_fields_info.pressed.connect(self.set_fields)
        self.fields_objects.append(new_fields_info)
        self.options_layout.addWidget(new_fields_info)
        new_fields_info.click()

    # answers field buttons signal and adds that field to "fields" or deletes it
    def set_fields(self):
        new = self.sender().text()
        if new == "Content":
            self.content_field = not self.sender().isChecked()
        else:
            if new in self.fields:
                self.fields.remove(new)
            else:
                self.fields.append(new)

    # answers folders buttons signal and chooses new folder and sets new fields
    def set_folder(self):
        new = self.sender().text()
        self.folder = new
        fields = []
        try:
            username = self.username.text()
            password = self.password.text()
            imap_server = self.website.text()
            imap = imaplib.IMAP4_SSL(imap_server)
            imap.login(username, password)
            status, messages = imap.select(new)
            messages = int(messages[0])
            n = 1
            for i in range(messages, messages - n, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1])
                        fields = msg.keys()
            self.number_of_messages_text.setText(self.number_of_messages_text_original + " (max: " + str(messages) + ")")
        except Exception as e:
            self.raise_error(e)
        self.show_fields(fields)

    # check if folder can be accessed
    def check_folder(self, new):
        try:
            username = self.username.text()
            password = self.password.text()
            imap_server = self.website.text()
            imap = imaplib.IMAP4_SSL(imap_server)
            imap.login(username, password)
            status, messages = imap.select(new)
            messages = int(messages[0])
            n = 1
            for i in range(messages, messages - n, -1):
                res, msg = imap.fetch(str(i), "(RFC822)")
            return True
        except Exception as e:
            return False

    # display error on screen as message box
    def raise_error(self, error):
        QtWidgets.QMessageBox.about(self, "Error", "An error (" + str(error) + ") occured, please try again")

    # display success on screen as message box
    def operation_successful(self, out):
        QtWidgets.QMessageBox.about(self, "Done", "An operation " + str(out) + " was performed successfully")

    # opens help/info window
    def activate_help(self):
        self.help_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
