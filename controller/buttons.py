import initExample
import numpy as np
from manager.datamanager import DataManager
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
#import ast
#from datetime import date,  datetime 
import scipy.io

#from plotview.plotData import plot
import pyqtgraph as pg
from utilities import change_axes
import pyqtgraph.opengl as gl
import pyqtgraph.functions as fn


class Buttons(QPushButton):
    
    def __init__(self, parent=None):
         
        super(Buttons, self).__init__(parent)
        # Make parent reachable from outside __init__
        self.parent = parent  

    # Generate buttons
        self.buttLoad = self.generateButtons('Load')
        self.parent.layout_buttons.addWidget(self.buttLoad) 
        self.buttSave = self.generateButtons('Save')
        self.parent.layout_buttons.addWidget(self.buttSave)
        self.buttPlot = self.generateButtons('Plot')
        self.parent.layout_buttons.addWidget(self.buttPlot)
        
        self.buttLoad.clicked.connect(self.load_file)
        self.buttSave.clicked.connect(self.save)
        self.buttPlot.clicked.connect(self.plot)

    def generateButtons(self, text):
        qbtn = QPushButton(text, self)
        return qbtn
        
    def load_file(self):
    
#        self.clearPlotviewLayout()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', "/share_vm/results_experiments/")
        
        if file_name:
#            self.data = np.loadtxt(file_name).view(complex).reshape(-1)
            self.data_loaded= scipy.io.loadmat(file_name)
            self.messages("Data loaded")
            

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
        
    def plot(self):
        
        if hasattr(self, 'data_loaded'):
            
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
            lo_freq=self.data_loaded["lo_freq"]
            BW=self.data_loaded["BW"]

            self.dataobject: DataManager = DataManager(average[0, :], lo_freq, len(average[0, :]),self.ns, BW)
           
            fft = self.dataobject.f_fft2Magnitude
            with np.errstate(divide = 'ignore'):
                positive = np.log(fn.clip_array(fft, 0, fft.max())**2)
#                negative = np.log(fn.clip_array(-fft, 0, -fft.min())**2)
            d2 = np.empty(fft.shape + (4,), dtype=np.ubyte)
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
            self.parent.layout_plots.addWidget(self.w)
            
            self.w1 = pg.ImageView()
            self.w1.setImage(self.dataobject.f_fft2Magnitude)
            self.parent.layout_plots.addWidget(self.w1)
#            
#            im2=np.moveaxis(self.dataobject.f_fft2Magnitude, 0, -1)
#            self.w2 = pg.ImageView()
#            self.w2.setImage(im2)
#            self.parent.layout_plots.addWidget(self.w2) 
#   
#            im3=np.moveaxis(im2, 0, -1)
#            self.w3 = pg.ImageView()
#            self.w3.setImage(im3)
#            self.parent.layout_plots.addWidget(self.w3)      

             
        else:
            self.messages("No data loaded")
            

    def messages(self, text):
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec();
