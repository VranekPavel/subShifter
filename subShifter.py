from PyQt5 import QtCore, QtGui, QtWidgets
import pysrt
from datetime import datetime
from functools import partial 
import os

class Engine():
    def __init__(self, path, encoding):
        self.path = path
        self.encoding = encoding
        self.error = ''
        self.file = self.open_file(path, encoding)
        self.part = self.file
        self.firtLoad = True

    def open_file(self, path, encoding):
        try:
            file = pysrt.open(path, encoding)
            return file
        except Exception as error:
            self.error = error
            return False

    def save_file(self):
        self.file.save(self.path, encoding=self.encoding)

    def shifter(self, file, seconds):
        file.shift(seconds=int(seconds))

    def rationizer(self, id):
        if id==23:
            self.file.shift(ratio=25/23.9)
        else:
            self.file.shift(ratio=23.9/25)

    def slice(self, fr, to):
        self.part = self.file.slice(starts_after={'hours':fr.hours,'minutes':fr.minutes, 'seconds':fr.seconds, 'milliseconds': fr.milliseconds-1}, 
            ends_before={'hours':to.hours,'minutes':to.minutes, 'seconds':to.seconds, 'milliseconds': to.milliseconds+1})

    def updater(self, val, index, column):
        if column == 0:
            self.file.data[index].index = val
        elif column == 1:
            self.file.data[index].start = val
        elif column == 2:
            self.file.data[index].end = val
        elif column == 3:
            self.file.data[index].text_without_tags = val


class Ui_MainWindow():
    def __init__(self):
        self.engine = None
        self.slicePos = []
        self.openEditor = None
        self.encodings = ["ASCII","UTF-8","ISO 8859-1","ISO 8859-15","cp1252", "cp1250"]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setColumnCount(3)
        self.treeWidget.setHeaderLabels(['       #', 'From', 'To', 'Text'])
        self.treeWidget.setColumnWidth(0, 90)
        self.treeWidget.setColumnWidth(1, 120)
        self.treeWidget.setColumnWidth(2, 120)
        self.gridLayout.addWidget(self.treeWidget, 3, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.shift = QtWidgets.QPushButton(self.groupBox)
        self.shift.setObjectName("shift")
        self.gridLayout_3.addWidget(self.shift, 2, 1, 1, 1)
        self.ratio_25 = QtWidgets.QPushButton(self.groupBox)
        self.ratio_25.setObjectName("ratio_25")
        self.gridLayout_3.addWidget(self.ratio_25, 2, 2, 1, 1)
        self.sl_from = QtWidgets.QLineEdit(self.groupBox)
        self.sl_from.setObjectName("sl_from")
        self.gridLayout_3.addWidget(self.sl_from, 1, 0, 1, 1)
        self.ratio_23 = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ratio_23.sizePolicy().hasHeightForWidth())
        self.ratio_23.setSizePolicy(sizePolicy)
        self.ratio_23.setObjectName("ratio_23")
        self.gridLayout_3.addWidget(self.ratio_23, 1, 2, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_3.addWidget(self.comboBox, 1, 3, 1, 1)
        self.enc_in = QtWidgets.QLineEdit(self.groupBox)
        self.enc_in.setObjectName("enc_in")
        self.gridLayout_3.addWidget(self.enc_in, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 3, 1, 1)
        self.shift_in = QtWidgets.QLineEdit(self.groupBox)
        self.shift_in.setObjectName("shift_in")
        self.gridLayout_3.addWidget(self.shift_in, 1, 1, 1, 1)
        self.sl_to = QtWidgets.QLineEdit(self.groupBox)
        self.sl_to.setObjectName("sl_to")
        self.gridLayout_3.addWidget(self.sl_to, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 629, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #adding signals and slots
        self.actionOpen.triggered.connect(self.initEngine)
        self.treeWidget.itemClicked.connect(self.item_click)
        self.treeWidget.itemChanged.connect(self.treeEdit)
        self.shift.clicked.connect(self.do_shift)
        self.actionSave_As.triggered.connect(self.save_As)
        self.actionSave.triggered.connect(self.save)
        self.ratio_23.clicked.connect(partial(self.change_ratio, 23))
        self.ratio_25.clicked.connect(partial(self.change_ratio, 25))
        self.comboBox.currentTextChanged.connect(self.enc_changed)
        self.enc_in.editingFinished.connect(partial(self.enc_changed, 1))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sub Shifter"))
        self.groupBox.setTitle(_translate("MainWindow", "Edit"))
        self.label_2.setText(_translate("MainWindow", "Shifting"))
        self.label.setText(_translate("MainWindow", "Slicing"))
        self.shift.setText(_translate("MainWindow", "Shift"))
        self.ratio_25.setText(_translate("MainWindow", "From 23.9 to 25"))
        self.ratio_23.setText(_translate("MainWindow", "From 25 to 23.9"))
        for i in range(len(self.encodings)):
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, _translate('MainWindow', self.encodings[i]))
        self.label_3.setText(_translate("MainWindow", "Change Ratio"))
        self.label_4.setText(_translate("MainWindow", "Change Encoding"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
    
    def reinitialize(self):
        self.slicePos = []
        self.openEditor = None

    def enc_changed(self,enc):
        if self.engine.firtLoad == False:
            if enc == 1:
                enc = self.enc_in.text()
                self.enc_in.setText('')
            engine = Engine(self.engine.path, enc)
            if engine.file != False:
                self.engine = engine
                self.updateVisual()
                self.comboBox.setCurrentText(self.engine.encoding)
                self.updateStatusBar('Encoding was changed to {}'.format(self.engine.encoding))
            else:
                self.updateStatusBar('Encoding {} did not fit current file'.format(enc))
        self.engine.firtLoad = False
        self.reinitialize()

    def treeEdit(self, item, column):
        val = self.treeWidget.currentItem().text(column)
        index = int(self.treeWidget.currentItem().text(0)) - 1
        self.engine.updater(val, index, column)
        self.treeWidget.closePersistentEditor(item, column)
        self.updateStatusBar('Cell in row:{} and column:{} was changed'.format(index, column))
    
    def change_ratio(self, id):
        if id == 23:
            self.engine.rationizer(23)
            self.updateStatusBar('Ratio was changed to 23.9 FPS')
        else:
            self.engine.rationizer(25)
            self.updateStatusBar('Ratio was changed to 25 FPS')
        self.updateVisual()

    def save(self):
        self.engine.save_file()
        self.updateStatusBar('File was saved')

    def save_As(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(caption='Save File', directory=os.path.dirname(self.engine.path), filter=("Srt Files (*.srt)"))
        self.updateStatusBar('File was saved as a {}'.format(fileName[0]))

    def item_click(self, item, column):
        if column == 0:
            self.updateSlice(self.treeWidget.currentItem().text(0))
        else:
            if self.openEditor != None:
                self.treeWidget.closePersistentEditor(self.openEditor[0], self.openEditor[1])
            self.openEditor = [item, column]
            self.treeWidget.openPersistentEditor(item,column)

    def updateSlice(self, pos):
        self.slicePos.append(pos)
        if len(self.slicePos) > 2:
            self.slicePos.pop(0)
        sort = sorted(self.slicePos)
        if len(sort) == 2:
            self.sl_from.backspace()
            self.sl_to.backspace()
            self.sl_from.insert(sort[0])
            self.sl_to.insert(sort[1])

    def do_shift(self):
        fr = self.sl_from.text()
        to = self.sl_to.text()
        try:
            shift = int(self.shift_in.text())
            if (fr != '') & (to != ''):
                self.engine.slice(self.engine.file.data[int(fr)-1].start, self.engine.file.data[int(to)-1].end)
                self.engine.shifter(self.engine.part, shift)
                self.updateStatusBar('Subtitles were updated based on slice selection.')
            else:
                self.engine.shifter(self.engine.file, shift)
                self.updateStatusBar('Subtitles were shifted.')
            self.updateVisual()
        except Exception:
            self.updateStatusBar('Insert number of seconds to shif')

    def initEngine(self):
        dia = QtWidgets.QFileDialog.getOpenFileName(caption = 'Open File', directory=os.path.dirname(os.path.abspath(__file__)) ,filter=("Srt Files (*.srt)"))
        try:
            for enc in self.encodings:
                self.engine = Engine(dia[0], enc)
                if self.engine.file:
                    break
            self.engine.firtLoad = True
            self.comboBox.setCurrentText(self.engine.encoding)
            self.updateVisual()
            self.engine.firtLoad = False
            self.updateStatusBar(self.engine.path)
        except Exception:
            self.updateStatusBar('File does\'t match any encoding')
        self.reinitialize()

    def updateStatusBar(self, message):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(message)        

    def updateVisual(self):
        self.treeWidget.clear()
        for row in self.engine.file.data:
            self.treeWidget.addTopLevelItem(QtWidgets.QTreeWidgetItem(self.treeWidget, [str(row.index),str(row.start), str(row.end), row.text_without_tags.replace('\n', ' ')]))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())