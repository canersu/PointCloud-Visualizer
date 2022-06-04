import sys, os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLineEdit
from PyQt5.QtCore import QSize
import helper

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(400, 400))    
        self.setWindowTitle("Depth Map Visualizer") 

    ################### Buttons ###################

        modelbtn = QPushButton('Import', self)
        modelbtn.clicked.connect(self.launchModelDialog)
        modelbtn.resize(100,32)
        modelbtn.move(170, 50)

        importcsvbtn = QPushButton('Import', self)
        importcsvbtn.clicked.connect(self.launchCSVDialog)
        importcsvbtn.resize(100,32)
        importcsvbtn.move(170,100)

        exportcsvbtn = QPushButton('Export', self)
        exportcsvbtn.clicked.connect(self.exportCSV)
        exportcsvbtn.resize(100,32)
        exportcsvbtn.move(290,100)   

        importcsvbtn = QPushButton('Import', self)
        importcsvbtn.clicked.connect(self.launchYAMLDialog)
        importcsvbtn.resize(100,32)
        importcsvbtn.move(170,200)

        showbtn = QPushButton('Show', self)
        showbtn.clicked.connect(self.showDiagram)
        showbtn.resize(100,32)
        showbtn.move(50,320)

    ################### Labels ###################

        label_head = QLabel("Data", self)
        label_head.move(50, 10)

        config_head = QLabel("Configuration", self)
        config_head.move(50, 160)

        label_model = QLabel("Depth Map(.hdf5)", self)
        label_model.resize(200,30)
        label_model.move(10, 50)

        label_csv = QLabel("Point Cloud File(.csv)", self)
        label_csv.resize(200,30)
        label_csv.move(10, 100)

        config_data = QLabel("Config file(.yaml)", self)
        config_data.resize(200,30)
        config_data.move(10, 200)

        self.l_thresh_label = QLabel("Lower Thresh", self)
        self.l_thresh_label.move(170, 280)

        self.u_thresh_label = QLabel("Upper Thresh", self)
        self.u_thresh_label.move(290, 280)

    ################### Text Boxes ###################

        self.l_thresh_text = QLineEdit(self)
        self.l_thresh_text.move(170, 250)
        self.l_thresh_text.setReadOnly(True)

        self.u_thresh_text = QLineEdit(self)
        self.u_thresh_text.move(290, 250)
        self.u_thresh_text.setReadOnly(True)

    def launchModelDialog(self):
        self.response_model = self.getModelFile()
    
    def launchCSVDialog(self):
        self.response_csv = self.getCSVFile()

    def launchYAMLDialog(self):
        self.response_yaml = self.getYAMLFile()
        
    def getModelFile(self):
        file_filter = 'Model File (**.hdf5)'
        self.response_model = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Depth Map File',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Model File (*.hdf5)'
        )
        print(self.response_model[0])
        return self.response_model[0]

    def getCSVFile(self):
        file_filter = 'csv File (**.csv)'
        self.response_csv = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV File',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='csv File (*.csv)'
        )
        print(self.response_csv[0])
        return self.response_csv[0]

    def getYAMLFile(self):
        file_filter = 'Config File (**.yaml)'
        self.response_yaml = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select Configuration File',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Config File (*.yaml)'
        )
        print(self.response_yaml[0])
        self.yaml_file = self.response_yaml[0]
        self.upper_thresh, self.lower_thresh = helper.yaml_reader(self.yaml_file)
        self.l_thresh_text.setText(str(self.lower_thresh))
        self.u_thresh_text.setText(str(self.upper_thresh))
        return self.response_yaml[0]


    def showDiagram(self):
        try:
            h5py_file = self.response_model
            csv_file = self.response_csv
            yaml_file = self.response_yaml[0]
            depth_map, intensity_map, horizontal_fov, vertical_fov = helper.h5py_parser(h5py_file)
            helper.csv_saver(depth_map, horizontal_fov, vertical_fov, csv_file)
            helper.show_depth_map(csv_file, self.upper_thresh, self.lower_thresh)
        except:
            QtWidgets.QMessageBox.about(self, "Error", "Please import configuration(.yaml), \nmodel(.hdf5) and pcl(.csv) files !!!")
    
    def exportCSV(self):
        csv_file = self.response_csv
        helper.export_csv(csv_file, self.upper_thresh, self.lower_thresh)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )