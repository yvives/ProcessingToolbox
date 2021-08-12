


def change_axes(axis1, axis2, axis3, n1, n2, n3):

    axes_x:int=axis1
    axes_y:int=axis2
    axes_z:int=axis3
    
# Change the axes
    if axes_x==1 and axes_y==2 and axes_z==3:
        x='readout'
        y='phase'
        z='slice'
        n_rd=n1
        n_ph=n2
        n_sl=n3
    elif axes_x==1 and axes_y==3 and axes_z==2:
        x='readout'
        y='slice'
        z='phase'
        n_rd=n1
        n_ph=n3
        n_sl=n2
    elif axes_x==2 and axes_y==1 and axes_z==3:
        x='phase'
        y='readout'
        z='slice'
        n_rd=n2
        n_ph=n1
        n_sl=n3
    elif axes_x==3 and axes_y==1 and axes_z==2:
        x='slice'
        y='readout'
        z='phase' 
        n_rd=n2
        n_ph=n3
        n_sl=n1 
    elif axes_x==3 and axes_y==2 and axes_z==1:
        x='slice'
        y='phase'
        z='readout' 
        n_rd=n3
        n_ph=n2
        n_sl=n1
    elif axes_x==2 and axes_y==3 and axes_z==1:
        x='phase'
        y='slice'
        z='readout'      
        n_rd=n3
        n_ph=n1
        n_sl=n2
    
    return x, y, z, n_rd, n_ph, n_sl
