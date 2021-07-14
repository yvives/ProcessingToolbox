

import numpy as np
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
import ast
from datetime import date,  datetime 
#from plotview.plotData import plot



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
#        self.buttPlot.clicked.connect()
  
    def generateButtons(self, text):
        qbtn = QPushButton(text, self)
        return qbtn
        
    def load_file(self):
    
#        self.clearPlotviewLayout()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', "experiments/")
        
        if file_name:
            data = np.loadtxt(file_name).view(complex).reshape(-1)
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

    def messages(self, text):
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec();
