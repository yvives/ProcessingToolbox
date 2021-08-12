"""
Startup Code

"""

import sys
sys.path.append('../marcos_client')
sys.path.append('../pyqtgraph/examples')
from PyQt5.QtWidgets import QApplication
from controller.mainviewcontroller import MainViewController
import cgitb 
cgitb.enable(format = 'text')


VERSION = "0.1.0"
AUTHOR = "Yolanda Vives"

if __name__ == '__main__':
    print("Processing Toolbox for Magnetic Resonance Imaging")
    
   
    app = QApplication(sys.argv)
    gui = MainViewController()
    gui.show()
    sys.exit(app.exec_())

        
