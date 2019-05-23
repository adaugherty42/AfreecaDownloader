import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import afreecadl
import datetime
import logging
import re

class QTextEditLogger(logging.Handler):
	def __init__(self, parent):
		super().__init__()
		self.widget = QtWidgets.QPlainTextEdit(parent)
		self.widget.setReadOnly(True)

	def emit(self, record):
		msg = self.format(record)
		self.widget.appendPlainText(msg)

# Downloads run on their own thread to prevent the UI from hanging
class DownloadThread(QtCore.QThread):
	def __init__(self, videos):
		super().__init__()
		self.videos = videos

	def run(self):
		for video in self.videos:
			afreecadl.download_video(video)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMaximumSize(QtCore.QSize(16777186, 16777215))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mainFrame = QtWidgets.QWidget(self.centralwidget)
        self.mainFrame.setObjectName("mainFrame")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.mainFrame)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.topLeftTabs = QtWidgets.QTabWidget(self.mainFrame)
        self.topLeftTabs.setEnabled(True)
        self.topLeftTabs.setObjectName("topLeftTabs")
        self.tab1_2 = QtWidgets.QWidget()
        self.tab1_2.setObjectName("tab1_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab1_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout1_tab1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout1_tab1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1_tab1.setObjectName("horizontalLayout1_tab1")
        self.tab1_label1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.tab1_label1.setObjectName("tab1_label1")
        self.horizontalLayout1_tab1.addWidget(self.tab1_label1)
        self.selectStreamerBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.selectStreamerBox.setObjectName("selectStreamerBox")
        self.horizontalLayout1_tab1.addWidget(self.selectStreamerBox)
        self.streamerSelected_tab1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.streamerSelected_tab1.setObjectName("streamerSelected_tab1")
        self.horizontalLayout1_tab1.addWidget(self.streamerSelected_tab1)
        self.horizontalLayout1_tab1.setStretch(0, 30)
        self.horizontalLayout1_tab1.setStretch(1, 50)
        self.horizontalLayout1_tab1.setStretch(2, 20)
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.tab1_2)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(10, 60, 351, 32))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout2_tab1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout2_tab1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout2_tab1.setObjectName("horizontalLayout2_tab1")
        self.tab1_label2 = QtWidgets.QLabel(self.horizontalLayoutWidget_7)
        self.tab1_label2.setObjectName("tab1_label2")
        self.tab1_label2.hide()
        self.horizontalLayout2_tab1.addWidget(self.tab1_label2)
        self.selectStreamBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_7)
        self.selectStreamBox.setObjectName("selectStreamBox")
        self.selectStreamBox.hide()
        self.horizontalLayout2_tab1.addWidget(self.selectStreamBox)
        self.streamSelected_tab1 = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.streamSelected_tab1.setObjectName("streamSelected_tab1")
        self.streamSelected_tab1.hide()
        self.horizontalLayout2_tab1.addWidget(self.streamSelected_tab1)
        self.horizontalLayout2_tab1.setStretch(0, 30)
        self.horizontalLayout2_tab1.setStretch(1, 50)
        self.horizontalLayout2_tab1.setStretch(2, 20)
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.tab1_2)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 110, 351, 32))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout3_tab1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout3_tab1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout3_tab1.setObjectName("horizontalLayout3_tab1")
        self.tab1_label3 = QtWidgets.QLabel(self.horizontalLayoutWidget_8)
        self.tab1_label3.setObjectName("tab1_label3")
        self.tab1_label3.hide()
        self.horizontalLayout3_tab1.addWidget(self.tab1_label3)
        self.selectHoursBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_8)
        self.selectHoursBox.setObjectName("selectHoursBox")
        self.selectHoursBox.hide()
        self.horizontalLayout3_tab1.addWidget(self.selectHoursBox)
        self.hoursSelected_tab1 = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.hoursSelected_tab1.setObjectName("hoursSelected_tab1")
        self.hoursSelected_tab1.hide()
        self.horizontalLayout3_tab1.addWidget(self.hoursSelected_tab1)
        self.horizontalLayout3_tab1.setStretch(0, 30)
        self.horizontalLayout3_tab1.setStretch(1, 50)
        self.horizontalLayout3_tab1.setStretch(2, 20)
        self.topLeftTabs.addTab(self.tab1_2, "")
        self.tab2_2 = QtWidgets.QWidget()
        self.tab2_2.setObjectName("tab2_2")
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(self.tab2_2)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(10, 10, 351, 33))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.tab2_label1 = QtWidgets.QLabel(self.horizontalLayoutWidget_9)
        self.tab2_label1.setObjectName("tab2_label1")
        self.horizontalLayout_17.addWidget(self.tab2_label1)
        self.enterUrlBox = QtWidgets.QLineEdit(self.horizontalLayoutWidget_9)
        self.enterUrlBox.setObjectName("enterUrlBox")
        self.horizontalLayout_17.addWidget(self.enterUrlBox)
        self.urlEntered_tab2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_9)
        self.urlEntered_tab2.setObjectName("urlEntered_tab2")
        self.horizontalLayout_17.addWidget(self.urlEntered_tab2)
        self.horizontalLayoutWidget_10 = QtWidgets.QWidget(self.tab2_2)
        self.horizontalLayoutWidget_10.setGeometry(QtCore.QRect(10, 50, 351, 32))
        self.horizontalLayoutWidget_10.setObjectName("horizontalLayoutWidget_10")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.tab2_label2 = QtWidgets.QLabel(self.horizontalLayoutWidget_10)
        self.tab2_label2.setObjectName("tab2_label2")
        self.tab2_label2.hide()
        self.horizontalLayout_18.addWidget(self.tab2_label2)
        self.selectHoursBox_tab2 = QtWidgets.QComboBox(self.horizontalLayoutWidget_10)
        self.selectHoursBox_tab2.setObjectName("selectHoursBox_tab2")
        self.selectHoursBox_tab2.hide()
        self.horizontalLayout_18.addWidget(self.selectHoursBox_tab2)
        self.hoursSelected_tab2 = QtWidgets.QPushButton(self.horizontalLayoutWidget_10)
        self.hoursSelected_tab2.setObjectName("hoursSelected_tab2")
        self.hoursSelected_tab2.hide()
        self.horizontalLayout_18.addWidget(self.hoursSelected_tab2)
        self.horizontalLayout_18.setStretch(0, 30)
        self.horizontalLayout_18.setStretch(1, 50)
        self.horizontalLayout_18.setStretch(2, 20)
        self.topLeftTabs.addTab(self.tab2_2, "")
        self.horizontalLayout_19.addWidget(self.topLeftTabs)
        self.selectedVods = QtWidgets.QListWidget(self.mainFrame)
        self.selectedVods.setObjectName("selectedVods")
        self.selectedVods.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.horizontalLayout_19.addWidget(self.selectedVods)
        self.startSelected = QtWidgets.QPushButton(self.mainFrame)
        self.startSelected.setObjectName("startSelected")
        self.horizontalLayout_19.addWidget(self.startSelected)
        self.progressWindow = QtWidgets.QPlainTextEdit(self.mainFrame)
        self.progressWindow.setObjectName("progressWindow")
        self.progressWindow.setReadOnly(True)
        self.horizontalLayout_19.addWidget(self.progressWindow)
        self.horizontalLayout_19.setStretch(0, 54)
        self.horizontalLayout_19.setStretch(1, 20)
        self.horizontalLayout_19.setStretch(2, 6)
        self.horizontalLayout_19.setStretch(3, 20)
        self.gridLayout.addWidget(self.mainFrame, 3, 0, 1, 1)

        # Logging Window
        self.logWindow = QTextEditLogger(self.centralwidget)
        self.logWindow.setFormatter(logging.Formatter("%(message)s"))
        logging.getLogger().addHandler(self.logWindow)
        logging.getLogger().setLevel(logging.DEBUG)
        self.logWindow.widget.setObjectName("logWindow")
        self.gridLayout.addWidget(self.logWindow.widget, 5, 0, 1, 2)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.gridLayout.setRowStretch(3, 70)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.topLeftTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Afreeca VOD Downloader"))
        self.tab1_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Find VOD</p></body></html>"))
        self.tab1_label1.setText(_translate("MainWindow", "Select Streamer"))
        self.streamerSelected_tab1.setText(_translate("MainWindow", "Search"))
        self.tab1_label2.setText(_translate("MainWindow", "Select Stream"))
        self.streamSelected_tab1.setText(_translate("MainWindow", "Confirm"))
        self.tab1_label3.setText(_translate("MainWindow", "Select Hours"))
        self.hoursSelected_tab1.setText(_translate("MainWindow", "Confirm"))
        self.topLeftTabs.setTabText(self.topLeftTabs.indexOf(self.tab1_2), _translate("MainWindow", "Find VOD"))
        self.tab2_label1.setText(_translate("MainWindow", "Enter Stream URL"))
        self.urlEntered_tab2.setText(_translate("MainWindow", "Go"))
        self.tab2_label2.setText(_translate("MainWindow", "Select Hours"))
        self.hoursSelected_tab2.setText(_translate("MainWindow", "Confirm"))
        self.topLeftTabs.setTabText(self.topLeftTabs.indexOf(self.tab2_2), _translate("MainWindow", "Enter URL"))
        self.startSelected.setText(_translate("MainWindow", "Start"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

class AfreecaUI(Ui_MainWindow):
	def __init__(self, MainWindow):
		self.setupUi(MainWindow)
		self.setupSlots()
		self.video_queue = {}
		self.selectStreamerBox.addItems(
			sorted(afreecadl.get_streamer_list(nickname_as_key=True).keys()))

    # Connections:
    #   selectStreamerBox -> streamerSelected_tab1
    #   selectStreamBox -> streamSelected_tab1
    #   selectHoursBox -> hoursSelected_tab1
    #   enterUrlBox -> urlEntered_tab2
    #   selectHoursBox_tab2 -> hoursSelected_tab2
    #   selectedVods -> startSelected
	def setupSlots(self):
    #     self.streamerSelected_tab1.pressed.connect(self.loadVodsForStreamer())
		self.urlEntered_tab2.pressed.connect(self.loadVodFromUrl)
		self.hoursSelected_tab2.pressed.connect(self.addVod_tab2)
		self.startSelected.pressed.connect(self.startDownload)

    # def loadVodsForStreamer(self):
    #     vodList = afreecadl.findVods()

	def loadVodFromUrl(self):
		url = self.enterUrlBox.text()
		self.video_list, streamer, self.date = afreecadl.grab_video_info(url)
		self.nickname = afreecadl.get_streamer_list(nickname_as_key=False)[streamer]
		hours_list = [str(i) for i in range(1, len(self.video_list)+1)]
		self.selectHoursBox_tab2.addItems(hours_list)
		self.tab2_label2.show()
		self.selectHoursBox_tab2.show()
		self.hoursSelected_tab2.show()

	def addVod_tab2(self):
		hour = self.selectHoursBox_tab2.currentText()
		vod = self.nickname + "_" + self.date.strftime("%m%d%y") + "_" + hour
		if not self.selectedVods.findItems(vod, Qt.Qt.MatchExactly):
			self.selectedVods.addItem(vod)
			#self.video_queue[vod] = self.video_list[int(hour)-1]

	def startDownload(self):
		selected = []
		for item in self.selectedVods.selectedItems():
			i = int(re.search("([0-9]+)$", item.text()).group(1))
			selected.append(self.video_list[i-1])
		#self.video_queue[self.selectedVods.selectedItems()]
		self.thread = DownloadThread(videos=selected)
		self.thread.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AfreecaUI(MainWindow)
    #ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

#streamerBox.addItems(
#			sorted(afreecadl.get_streamer_list().keys()))