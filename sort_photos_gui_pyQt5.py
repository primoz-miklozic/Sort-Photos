from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.button_get_dir = QtWidgets.QPushButton(self.centralwidget)
        self.button_get_dir.setGeometry(QtCore.QRect(100, 10, 100, 25))
        self.button_get_dir.setObjectName("button_get_dir")
        self.button_get_dir.clicked.connect(self.get_Dir)

        self.label_dir = QtWidgets.QLabel(self.centralwidget)
        self.label_dir.setGeometry(QtCore.QRect(100, 40, 291, 21))
        self.label_dir.setObjectName("label_dir")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(90, 150, 830, 140))
        self.textBrowser.setObjectName("textBrowser")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 320, 830, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.button_start_sort = QtWidgets.QPushButton(self.centralwidget)
        self.button_start_sort.setGeometry(QtCore.QRect(100, 100, 75, 23))
        self.button_start_sort.setObjectName("button_start_sort")
        self.button_start_sort.clicked.connect(self.sort_dir)
        self.button_start_sort.setEnabled(False)

        self.label_newdir = QtWidgets.QLabel(self.centralwidget)
        self.label_newdir.setGeometry(QtCore.QRect(100, 70, 501, 21))
        self.label_newdir.setObjectName("label_newdir")


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sort Photos by Date 0.2"))
        self.button_get_dir.setText(_translate("MainWindow", "select folder"))
        self.label_dir.setText(_translate("MainWindow", "selected folder"))
        self.button_start_sort.setText(_translate("MainWindow", "start"))
        self.label_newdir.setText(_translate("MainWindow", "destination folder"))
        self.statusbar.showMessage("Select folder to be sorted.")

    def get_Dir(self):
        Tk().withdraw()
        path = filedialog.askdirectory()
        # if not clicked cancel:
        if path !="":
            self.label_dir.setText(path)
            self.label_newdir.setText(path + "/[year]-[month]")
            self.statusbar.showMessage("Press Start to sort photos.")
            self.button_start_sort.setEnabled(True)
        return path

    def sort_dir(self):

        def get_files(path):
            files = []
            for file in os.listdir(path):
                if file.endswith('.jpg'):
                    files.append(file)
                if file.endswith('.JPG'):
                    files.append(file)
            return files

        def get_date_metaData(img_name):
            try:
                metaData = {}
                img_file = Image.open(img_name)
                info = img_file._getexif()
                if info:
                    for (tag, value) in info.items():
                        tagname = TAGS.get(tag, tag)
                        metaData[tagname] = value
                        # Preberem datum iz metaData
                        if tagname == "DateTimeOriginal" or tagname == "DateTime":
                            date_original = metaData[tagname]

                    # izluščim leto in mesec
                    date_list = date_original.split()
                    date_list = ":".join(date_list)
                    date_list = date_list.split(":")
                    year = date_list[0]
                    month = date_list[1]
                    return year, month
            except:
                print("error")

        def make_dir(path, year, month):
            dirname = path + "/" + year + "-" + month
            if os.path.exists(dirname):
                print("Že obstaja!")
            else:
                os.makedirs(dirname)


        path = self.label_dir.text()
        jpg_files = get_files(path)
        i = 1
        for file in jpg_files:
            # izpis števca
            self.statusbar.showMessage(str(i) + " of " + str(len(jpg_files)))
            self.statusbar.update()
            old_path = path + "/" + file
            try:
                # get year and month from jpg file
                year, month = get_date_metaData(old_path)
                # create directory
                make_dir(path, year, month)

                new_path = path + "/" + year + "-" + month + "/" + file
                # copy file (copy2 ohrani metadata!)
                print(file)
                print(old_path)
                print(new_path)
                self.textBrowser.append(file + "\t" + "-->"+ "\t" + new_path)
                shutil.copy2(old_path, new_path)
                # delete copied file
                os.remove(old_path)
                self.progressBar.setValue(round(i / len(jpg_files) * 100))
                self.progressBar.update()
            except  Exception as e:
                print(e)
                print("Napaka pri datoteki " + file)
            i += 1
            # sleep za upočasnitev, za test sliderja
            #time.sleep(3)
        self.statusbar.showMessage("Done.")

if __name__ == "__main__":
    import sys
    import os
    import time
    import shutil
    from PIL.ExifTags import TAGS
    from PIL import Image
    from tkinter import filedialog





    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


