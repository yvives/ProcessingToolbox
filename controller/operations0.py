
import initExample
import numpy as np
from manager.datamanager import DataManager
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout,  QLabel, QComboBox, QSpacerItem, QSizePolicy, QPushButton, QTextEdit
from defaults import default_recons, default_artifacts, default_regrid, default_filter 
from PyQt5.uic import loadUiType

#import ast
#from datetime import date,  datetime 

Parameter_Form, Parameter_Base = loadUiType('ui/inputparameter.ui')

class Operations(QTabWidget):
    
    
    def __init__(self, parent=None):
         
        super(QTabWidget, self).__init__(parent)
        # Make parent reachable from outside __init__
        self.parent = parent  

        self.build_GUI()
            
        self.C2.activated.connect(self.triggeredReconsChanged)
        self.C10.activated.connect(self.triggeredRegridChanged)
        self.C11.activated.connect(self.triggeredFilterChanged)
        self.C3.activated.connect(self.triggeredArtifactChanged)    
#        self.setParametersUI("Turbo Spin Echo")

        self._currentRegrid = "None"
        self._currentFilter= "None"
        self._currentRecons="FFT"
        self._currentArts= "Gauss"

    def triggeredArtifactChanged(self):
        self._currentArts = artifact

    def triggeredRegridChanged(self):
        self._currentRegrid = regridding
        
    def triggeredFilterChanged(self):
        self._currentFilter = filtering    

    def triggeredReconsChanged(self):
        self._currentRecons = reconstruction
        self.setParametersReconsUI(recons)

    def getCurrentArts(self) -> str:
        return self._currentArts
        
    def getCurrentRegrid(self) -> str:
        return self._currentRegrid
        
    def getCurrentFilter(self) -> str:
        return self._currentFilter

    def getCurrentRecons(self) -> str:
        print(self._currentRecons)
        return self._currentRecons

    def build_GUI(self):
    
#        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
#        self.tabs.resize(300, 200)
  
        # Add tabs
        self.addTab(self.tab1, "Refinement")
        self.addTab(self.tab2, "Reconstruction")
        self.addTab(self.tab3, "Gauss Artifact")
  
       
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.label1=QLabel("Regridding")
        self.tab1.layout.addWidget(self.label1)
        self.C10 = QComboBox()
        self.C10.addItems(list(default_regrid))
        self.C10.setCurrentIndex(0)
        self.tab1.layout.addWidget(self.C10)
        self.label2=QLabel("Scale Factor")
        self.text1=QTextEdit('1')
        self.tab1.layout.addWidget(self.label2)
        self.tab1.layout.addWidget(self.text1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab1.layout.addItem(self.verticalSpacer)

       
        self.label3=QLabel("Filtering")
        self.tab1.layout.addWidget(self.label3)
        self.C11 = QComboBox()
        self.C11.addItems(list(default_filter))
        self.C11.setCurrentIndex(0)
        self.tab1.layout.addWidget(self.C11)
        self.label4=QLabel("Scale Factor")
        self.text2=QTextEdit('1')
        self.tab1.layout.addWidget(self.label4)
        self.tab1.layout.addWidget(self.text2)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab1.layout.addItem(self.verticalSpacer)
        
        self.butt_refin=QPushButton('Run refinement', self)
        self.tab1.layout.addWidget(self.butt_refin)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        self.C2 = QComboBox()
        print(list(default_recons.keys()))
        self.C2.addItems(list(default_recons.keys()))
        self.tab2.layout.addWidget(self.C2)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab2.layout.addItem(self.verticalSpacer)
        self.butt_recon=QPushButton('Run reconstruction', self)
        self.tab2.layout.addWidget(self.butt_recon)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab2.layout.addItem(self.verticalSpacer)
        self.tab2.setLayout(self.tab2.layout)

        # Create third tab
        self.tab3.layout = QVBoxLayout(self)
        self.C3 = QComboBox()
        self.C3.addItems(list(default_artifacts.keys()))
        self.tab3.layout.addWidget(self.C3)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tab3.layout.addItem(self.verticalSpacer)
        self.tab3.setLayout(self.tab3.layout)

    
