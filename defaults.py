from PTnamespace import Namespace as op_nms

class FFT:
    def __init__(self, op_recon:str):
        self.op_recon:str=op_recon

class ART:
    def __init__(self,
                 op_recon: str,
                 niter: int=None,
                 lambda0: int=None,
                 delta: float=None,
                 ):
        self.op_recon:str=op_recon
        self.niter:int=niter
        self.lambda0:int=lambda0
        self.delta:float=delta

    @property
    def inputs(self) -> dict:

        return {
            op_nms.niter: [int(self.niter)],
            op_nms.lambda0: [int(self.lambda0)],
            op_nms.delta:[float(self.delta)], 
            }
            
            
class ZeroPadding:
    def __init__(self,
                op_zeroPad: str,
                factor: float=None,
                 ):
        self.op_zeroPad:str=op_zeroPad
        self.factor:float=factor

    @property
    def inputs(self) -> dict:

        return {
            op_nms.factor: [int(self.factor)],
            }
            
class Nothing:
    def __init__(self, op_nothing: str):
        self.op_nothing:str=op_nothing

class Pchip:
    def __init__(self, op_pchip: str):
        self.op_pchip:str=op_pchip
        
class Spline:
    def __init__(self, op_spline: str):
        self.op_spline:str=op_spline
        
class GridData:
    def __init__(self, op_gridData: str):
        self.op_gridData:str=op_gridData
        
class BM4D_G:
    def __init__(self, op_BM4D_G: str):
        self.op_BM4D_G:str=op_BM4D_G        
        
class BM4D_R:
    def __init__(self, op_BM4D_R: str):
        self.op_BM4D_R:str=op_BM4D_R      

class PeronaMalik:
    def __init__(self, op_PeronaMalik: str):
        self.op_PeronaMalik:str=op_PeronaMalik    

default_recons={
    'FFT':FFT('FFT'), 
    'ART':ART('ART',1, 1, 0.0 ),
}

default_imregrid={
    'None':Nothing('None'), 
    'Pchip':Pchip('Pchip'), 
    'Spline':Spline('Spline'), 
    'GridData':GridData('GridData') 
}

default_ksregrid={
    'None':Nothing('None'), 
    'ZeroPadding':ZeroPadding('ZeroPadding', 2), 
} 
    
default_filter={
    'None':Nothing('None'), 
    'BM4D Gauss':BM4D_G('BM4D Gauss'), 
    'BM4D Rice':BM4D_R('BM4D Rice'), 
    'PeronaMalik':PeronaMalik('Perona Malik')
}
