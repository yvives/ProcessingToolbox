"""
Main View Controller

@author:    Yolanda Vives

@status:    Sets up the main view, its views and controllers
@todo:

"""
#from PyQt5.QtWidgets import QPushButton
from controller.operations import Operations
from PyQt5.uic import loadUiType, loadUi
import sys
sys.path.append('../marcos_client')
import cgitb 
cgitb.enable(format = 'text')
import pdb
st = pdb.set_trace
import scipy.io
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QLabel, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QTextEdit
from PyQt5.QtCore import pyqtSlot
from utilities import change_axes
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import pyqtgraph.functions as fn
from datetime import date,  datetime 

MainWindow_Form, MainWindow_Base = loadUiType('ui/mainview_v2.ui')

class MainViewController(MainWindow_Form, MainWindow_Base):
    """
    MainViewController Class
    """
   
    def __init__(self):
        super(MainViewController, self).__init__()
        self.ui = loadUi('ui/mainview_v2.ui')
        self.setupUi(self)
        
        self.tab=Operations(self)
        self.layout_operations.addWidget(self.tab)
        
        # Toolbar Actions
        self.action_load.triggered.connect(self.load_file)
        self.action_save.triggered.connect(self.save)
        self.action_close.triggered.connect(self.close)    
        self.action_plot.triggered.connect(self.plot3D) 
        self.action_reload.triggered.connect(self.reload)       
        
        # Status bar
        self.statusBar.showMessage('No file loaded')
        
        # Console
        self.cons = self.generateConsole('')

#        sys.stdout = EmittingStream(textWritten=self.onUpdateText)
        
                
#        sys.stderr = EmittingStream(textWritten=self.onUpdateText)      

              
    @staticmethod
    def generateConsole(text):
        con = QTextEdit()
        con.setText(text)
        return con
        
    def onUpdateText(self, text):
        cursor = self.cons.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.cons.setTextCursor(cursor)
        self.cons.ensureCursorVisible()


    def close(self):
        sys.exit()       
        
    def load_file(self):
    
#        self.clearPlotviewLayout()
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', "/share_vm/results_experiments/")
        self.plot_title='K-Space (abs) loaded data'
        
        if self.file_name:
            self.data_loaded= scipy.io.loadmat(self.file_name)
            
            axes=self.data_loaded["axes"]
            axis1=axes[0, 0]
            axis2=axes[0, 1]
            axis3=axes[0, 2]
            n=self.data_loaded["n"]
            n1=n[0, 0]
            n2=n[0, 1]
            n3=n[0, 2]
            x, y, z, self.n_rd, self.n_ph, self.n_sl = change_axes(axis1,axis2,axis3,n1,n2,n3)
            self.ns = [self.n_rd, self.n_ph, self.n_sl]
            average=self.data_loaded["average"]
            self.data_kS = np.reshape(average, (self.n_sl, self.n_ph, self.n_rd))
            self.data=self.data_kS
            
            self.statusBar.clearMessage()
            self.statusBar.showMessage(self.file_name)
        else:
            self.file=QLabel("No file loaded")
            self.statusBar.addWidget(self.file)

    def save(self):
        
        dt = datetime.now()
        dt_string = dt.strftime("%d-%m-%Y_%H_%M")
#        dict = vars(defaultsequences[self.sequence]) 
#        
#        sequ = '%s' %(self.sequence)
#        sequ = sequ.replace(" ", "")
#        f = open("experiments/parameterisations/%s_params_%s.txt" % (sequ, dt_string),"w")
#        f.write( str(dict) )
#        f.close()
  
        self.messages("Saved")

           
    def reload(self):
        
        self.data_loaded= scipy.io.loadmat(self.file_name)
        average=self.data_loaded["average"]
        self.data_kS = np.reshape(average, (self.n_sl, self.n_ph, self.n_rd))
        self.data=self.data_kS
        self.plot_title='K-Space (abs) loaded data'
        self.plot3D()
        self.messages("Original file reloaded")  

        
           
    #############################################################
    ########################  3D plot ###############################
    #############################################################
         
    def plot3D(self):  
     
        self.clearLayoutPlots()
        
        self.layout_output.addWidget(self.cons)
        
        if hasattr(self, 'data'):
            t=np.iscomplex(self.data)
            if np.any(t):
                self.data3D=np.abs(self.data)
            else:
                self.data3D=self.data
            
            with np.errstate(divide = 'ignore'):
                positive = np.log(fn.clip_array(self.data3D, 0, self.data3D.max())**2)
#                negative = np.log(fn.clip_array(-fft, 0, -fft.min())**2)
            d2 = np.empty(self.data3D.shape + (4,), dtype=np.ubyte)
            d2[..., 0] = positive * (255./positive.max())
            d2[..., 1] = 0
            d2[..., 2] = d2[...,1]
            d2[..., 3] = d2[..., 0]*0.3 + d2[..., 1]*0.3
            d2[..., 3] = (d2[..., 3].astype(float) / 255.) **2 * 255

            d2[:, 0, 0] = [255,0,0,100]
            d2[0, :, 0] = [0,255,0,100]
            d2[0, 0, :] = [0,0,255,100]
            
            self.w = gl.GLViewWidget()
            v = gl.GLVolumeItem(d2)
            self.w.addItem(v)

            self.layout_plots.addWidget(self.w)
            
            #############################################################
            ########################  ImageView Plot ###########################
            #############################################################
            
            self.layout2 = QVBoxLayout()
            self.b1 = QPushButton('Change View', self)
            self.layout2.addWidget(self.b1)
            self.label = QLabel("%s" % (self.plot_title))
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setStyleSheet("background-color: black;color: white")
            self.layout2.addWidget(self.label)
            self.w1 = pg.ImageView()
            self.w1.setImage(self.data3D)
            self.roi = pg.RectROI([0, 0], [5,5], pen='r')
#            
#            value = self.w1.getRoiPlot()
#            print(value)
            self.w1.addItem(self.roi)

            self.layout2.addWidget(self.w1)
            self.layout_plots.addLayout(self.layout2)

            self.b1.clicked.connect(self.button_clicked)
            
            self.w1.roi.sigRegionChanged.connect(self.roi_avg)
            
#            selected = self.w1.roiChanged()
#            selected = self.roi.getArrayRegion(self.data3D, self.w1)
#            print(selected.mean(axis=0))
            
        else:
            self.messages("No data loaded")   
            
    @pyqtSlot()
    def roi_avg(self):
        for i in reversed(range(self.layout_plots.count())):
            if hasattr(self.layout_plots.itemAt(i).widget(), 'roi') :
                selected =self.layout_plots.itemAt(i).widget().roi.getArrayRegion(self.data,self.layout_plots.itemAt(i).widget().getImageItem(), axes=(0,1))
                nonzeroVals = selected[np.nonzero(selected)]
                print(np.mean(nonzeroVals))
            
    def messages(self, text):
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec();
        
    def clearLayoutPlots(self):
    
        for i in reversed(range(self.layout_plots.count())):
            if self.layout_plots.itemAt(i).layout():
                self.layout_plots.itemAt(i).layout().setParent(None)
            else:
                self.layout_plots.itemAt(i).widget().setParent(None)
    
    
    @pyqtSlot()
    def button_clicked(self):
        
        self.clearLayoutPlots()
        im = self.data
        self.data=np.moveaxis(im, 0, -1)
        
        self.b1.setChecked(False)
        self.plot3D()
        
class ImageView(pg.ImageView):

    # constructor which inherit original
    # ImageView
    def __init__(self, *args, **kwargs):
        pg.ImageView.__init__(self, *args, **kwargs)

    # roi changed method
    def roiChanged(self):

        # printing message
        print("ROI Changed")  
#        self.roi = pg.ImageView.getRoiPlot(self)  
#        selected = self.roi.getArrayRegion(self.data, self.w1)
#        print(selected.mean(axis=0))
        
class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


