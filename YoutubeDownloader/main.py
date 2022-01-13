#========================================================================================================================
# pytube version used is 10.8.5
#========================================================================================================================

from pytube import YouTube
from PyQt5 import uic, QtWidgets
from os import getcwd
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('gui.ui', self) # load gui made in PyQt5
        self.setWindowTitle("Youtube Downloader") # add title
        self.show() # open window
        self.button = self.findChild(QtWidgets.QPushButton, 'accept') # gets button
        self.button.clicked.connect(self.download) # sets action on click
        self.findChild(QtWidgets.QLineEdit, 'location').setText(getcwd()) # sets 'location' field with directory path
        self.progress = self.findChild(QtWidgets.QProgressBar, 'progress') # gets progress bar

    def download(self):
        label = self.findChild(QtWidgets.QLabel, 'info') #gets label
        link = self.findChild(QtWidgets.QLineEdit, 'link').text() #gets input field text - link to video
        location = self.findChild(QtWidgets.QLineEdit, 'location').text() #gets input field text - directory path

        try:
            results = YouTube(link) # tries to get all available streamings
            label.setText("Downloading") # sets label
        except:
            label.setText("Error") # sets label
            return
        
        self.best_res = results.streams.get_highest_resolution() # chooses stream with best resolution
        self.progress.setValue(0) # sets progress bar value
        self.best_res.download(location) # downloads video to location
        self.progress.setValue(100) # sets progress bar value
        label.setText("Succes") # sets label


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
