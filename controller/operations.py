
import initExample
import numpy as np
from manager.datamanager import DataManager
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout,  QLabel, QComboBox, QSpacerItem, QSizePolicy, QPushButton, QTextEdit, QGroupBox
from defaults import default_recons, default_imregrid, default_ksregrid, default_filter 
from PyQt5.uic import loadUiType
from PyQt5.QtCore import pyqtSlot

#import ast
#from datetime import date,  datetime 

Parameter_Form, Parameter_Base = loadUiType('ui/inputparameter.ui')

class Operations(QTabWidget):
    
    
    def __init__(self, parent=None):
         
        super(QTabWidget, self).__init__(parent)
        # Make parent reachable from outside __init__
        self.parent = parent  

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
  
        # Add tabs
        self.addTab(self.tab1, "KSpace Refinement")
        self.addTab(self.tab2, "Reconstruction")
        self.addTab(self.tab3, "ImageSpace Refinement")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        
    def tab1UI(self):
        
        self.tab1.layout1 = QVBoxLayout(self)
        
        # Combobox 1
        self.label1=QLabel("KSpace Regridding")
        self.C10 = QComboBox()
        self.C10.addItems(list(default_ksregrid.keys()))
        self.C10.setItemText(0,"None")
        self.kSRegrid = self.C10.currentText()
        self.C10.currentIndexChanged.connect(self.kSRegridchange)
        
        # TextEdit
        self.label2=QLabel("Scale Factor")     
        self.text1=QTextEdit('')      
        if self.C10.currentText() == 'None':
            self.label2.setDisabled(True) 
            self.text1.setReadOnly(True)           
        else:
            self.label2.setDisabled(False) 
            self.text1.setReadOnly(False) 
            
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.tab1.layout1.addWidget(self.label1)
        self.tab1.layout1.addWidget(self.C10)
        self.tab1.layout1.addWidget(self.label2)
        self.tab1.layout1.addWidget(self.text1)
        self.tab1.layout1.addItem(self.verticalSpacer)

        # Button run
        self.butt_refin=QPushButton('Run kSpace refinement', self)
        self.butt_refin.clicked.connect(self.buttonKSRefin_clicked)
        self.tab1.layout1.addWidget(self.butt_refin)

        # Set Layout
        self.tab1.setLayout(self.tab1.layout1)

    def tab2UI(self):
        
        self.tab2.layout2 = QVBoxLayout(self)
        
        # Combobox
        self.C2 = QComboBox()
        self.C2.addItems(list(default_recons.keys()))
        self.C2.setItemText(0,"FFT")
        self._currentRecons = "FFT"
        recon = self.C2.currentText()
        self.C2.currentIndexChanged.connect(self.reconschange)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)            
                
        # GroupBox
        self.gBox = QGroupBox("Parameters")
        self.vbox = QVBoxLayout()

        listRecWid=self.addReconWidgets(recon)
        if listRecWid:
            for item in listRecWid:
                self.vbox.addWidget(item)
             
            self.gBox.setLayout(self.vbox)           

        # Button
        self.butt_recon=QPushButton('Run reconstruction', self)        
    
        self.tab2.layout2.addWidget(self.C2)
#        self.tab2.layout2.addItem(self.verticalSpacer)
        if listRecWid:
            self.tab2.layout2.addWidget(self.gBox)
        self.tab2.layout2.addWidget(self.butt_recon)
        
        # Set Layout
        self.tab2.setLayout(self.tab2.layout2)

        # Button connection
        self.butt_recon.clicked.connect(self.buttonRecon_clicked)

    def tab3UI(self):
        
        self.tab3.layout3 = QVBoxLayout(self)
        
        # Combobox 1
        self.label3=QLabel("Image Space Regridding")
        self.C30 = QComboBox()
        self.C30.addItems(list(default_imregrid))
        self.C30.setItemText(0,"None")
        self._currentRegrid = "None"
        self.C30.currentIndexChanged.connect(self.ImRegridchange)
        
        # TextEdit
        self.label4=QLabel("Scale Factor")
        self.text2=QTextEdit('1')     
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.tab3.layout3.addWidget(self.label3)
        self.tab3.layout3.addWidget(self.C30)
        self.tab3.layout3.addWidget(self.label4)
        self.tab3.layout3.addWidget(self.text2)
        self.tab3.layout3.addItem(self.verticalSpacer)

        # Combobox 2
        self.label5=QLabel("Filtering")
        self.C31 = QComboBox()
        self.C31.addItems(list(default_filter))
        self.C31.setItemText(0,"None")
        self._currentFilter = "None"
        self.C31.currentIndexChanged.connect(self.filterchange)
        
        # TextEdit
        self.label6=QLabel("Scale Factor")
        self.text3=QTextEdit('1')        
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)        
        
        self.tab3.layout3.addWidget(self.label5)
        self.tab3.layout3.addWidget(self.C31)
        self.tab3.layout3.addWidget(self.label6)
        self.tab3.layout3.addWidget(self.text3)
        self.tab3.layout3.addItem(self.verticalSpacer)
        
        # Button run
        self.butt_refin=QPushButton('Run ImageSpace refinement', self)
        self.butt_refin.clicked.connect(self.buttonImRefin_clicked)
        self.tab3.layout3.addWidget(self.butt_refin)

        # Set Layout
        self.tab3.setLayout(self.tab3.layout3)

    def kSRegridchange(self,i):
        self._currentkSRegrid = self.C10.currentText()
        if self.C10.currentText() == 'None':
            self.label2.setDisabled(True) 
            self.text1.setReadOnly(True)       
            self.text1.setText('')
        else:
            self.label2.setDisabled(False) 
            self.text1.setReadOnly(False) 
            self.text1.setText(str(default_ksregrid[self._currentkSRegrid].factor))
        
    def filterchange(self,i):
        self._currentFilter = self.C11.currentText()
    
    def ImRegridchange(self,i):
        self._currentImRegrid = self.C30.currentText()    
        
    def reconschange(self,i):
        recon = self.C2.currentText()
        self._currentRecons = recon
        if self.tab2.layout2.itemAt(2):
            self.tab2.layout2.itemAt(1).widget().setParent(None)
#            self.tab2.layout2.itemAt(2).widget().setParent(None)
            for i in reversed(range(self.vbox.count())): 
                self.vbox.itemAt(i).widget().setParent(None)
        
        listRecWid=self.addReconWidgets(recon)
        if listRecWid:
            for item in listRecWid:
                self.vbox.addWidget(item)
             
            self.gBox.setLayout(self.vbox)   
             
        self.tab2.layout2.addWidget(self.gBox)
        self.tab2.layout2.addWidget(self.butt_recon)

            
    def addReconWidgets(self, recon) :
        inputwidgets: list = []
        if hasattr(default_recons[recon], 'inputs'):
            art_prop = default_recons[recon].inputs
            inputwidgets += self.generateWidgetsFromDict(art_prop, recon)
        
            return inputwidgets


    def getCurrentkSRegrid(self) -> str:
        return self._currentkSRegrid
        
    def getCurrentImRegrid(self) -> str:
        return self._currentImRegrid
        
    def getCurrentFilter(self) -> str:
        return self._currentFilter

    def getCurrentRecons(self) -> str:
        return self._currentRecons

    @pyqtSlot()
    def buttonImRefin_clicked(self):

        ImRegrid = self.getCurrentImRegrid()
        ImFilter = self.getCurrentFilter()
        if hasattr(self.parent,'data'):
            if ImRegrid == 'Pchip':
                self.fft2Data = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(self.parent.data)))
                self.pchiped = abs(self.fft2Data)
                self.parent.data = self.pchiped
                self.parent.plot_title='Pchip interpolated image'
                self.parent.plot3D()
            
            elif recon == 'ART':
                print('recons')

        else:
            self.parent.messages("Load data first...")
        
    @pyqtSlot()
    def buttonKSRefin_clicked(self):
        if hasattr(self.parent,'data'):
            dims = self.parent.data.shape
            width=np.empty(3,dtype=object)
            print(self.parent.data.shape)
            for i in range(3):
                width[i] = np.rint((dims[i]*default_ksregrid[self._currentkSRegrid].factor-dims[i])/2)
               
            width=width.astype(int)
            self.parent.data=np.pad(self.parent.data,((width[0], width[0]), (width[1], width[1]), (width[2], width[2])),'constant', constant_values=(0))
            print(self.parent.data.shape)
            self.parent.messages('Zero padded')

        else:
            self.parent.messages("Load data first...")
            
      
    @pyqtSlot()  
    def buttonRecon_clicked(self):
        recon = self.getCurrentRecons()
        
        if recon == 'FFT':
            self.fft2Data = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(self.parent.data)))
            self.fft2Mag = abs(self.fft2Data)
            self.parent.data = self.fft2Mag
            self.parent.plot_title='FFT of the loaded data'
            self.parent.plot3D()
            
        elif recon == 'ART':
            print('recons')

    @pyqtSlot()
    def buttonArtifact_clicked(self):
        print("dins filter")
       
    @staticmethod
    def generateWidgetsFromDict(obj: dict = None, action: str = None) -> list:
        widgetlist: list = []
        for key in obj:
            widget = ActionParameter(key, obj[key], action)
            widgetlist.append(widget)
        return widgetlist

class ActionParameter(Parameter_Base, Parameter_Form):
    """
    Operation Parameter Widget-Class
    """
    # Get reference to position in operation object
    def __init__(self, name, parameter, action):
        super(ActionParameter, self).__init__()
        self.setupUi(self)

        # Set input parameter's label and value
        self.action = action
        self.parameter = parameter
        self.label_name.setText(name)
        
        self.input_value.setText(str(parameter[0]))
        
        
        # Connect text changed signal to getValue function
#        self.input_value.textChanged.connect(self.get_value)
#        
#    def get_value(self) -> None:
#
#        temp = vars(defaultsequences[self.sequence])
#        for item in temp:
#            lab = 'nmspc.%s' %(item)
#            res=eval(lab)
#            if (res == self.label_name.text()):
#                t = type(getattr(defaultsequences[self.sequence], item))     
#                inV = 'tlt_inV.%s' %(item)
#                if (hasattr(tlt_inV, item)):
#                    res3 = eval(inV)
#                    if res3 == 'Value between 0 and 1':  
#                        val=self.validate_input()
#                        if val == 1:           
#                            if (t is float): 
#                                value: float = float(self.input_value.text())
#                                setattr(defaultsequences[self.sequence], item, value)
#                            elif (t is int): 
#                                value: int = int(self.input_value.text())
#                                setattr(defaultsequences[self.sequence], item, value)  
#                else:
#                    if (t is float): 
#                        value: float = float(self.input_value.text())
#                        setattr(defaultsequences[self.sequence], item, value)
#                    elif (t is int): 
#                        value: int = int(self.input_value.text())
#                        setattr(defaultsequences[self.sequence], item, value)
#                    else:
#                        v = self.input_value.text()
#                        v=v.replace("[", "")
#                        v=v.replace("]", "")
#                        v2 = list(v.split(","))
#                        if item=='shim':
#                            value: list = list([float(v2[0]), float(v2[1]), float(v2[2])])
#                        else:
#                            if (v2[0] != ''):
#                                value: list = list([int(v2[0]), int(v2[1]), int(v2[2])])
#                        setattr(defaultsequences[self.sequence], item, value)
#
#                
#    def validate_input(self):
#        reg_ex = QRegExp('^(?:0*(?:\.\d+)?|1(\.0*)?)$')
#        input_validator = QRegExpValidator(reg_ex, self.input_value)
#        self.input_value.setValidator(input_validator)
#        state = input_validator.validate(self.input_value.text(), 0)
#        if state[0] == QRegExpValidator.Acceptable:
#            return 1
#        else:
#            return 0
#        
#    def set_value(self, key, value: str) -> None:
#        print("{}: {}".format(self.label_name.text(), self.input_value.text()))
        
