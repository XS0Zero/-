import numpy as np
import matplotlib.pyplot as plt
    
def movie_plot(nodes = None,Ug = None,tspan = None,speed = None,scale = None,view_pos = None,figid = None): 
    count = 1
    #ºÏÊÊµÄ×ø±êÖá·¶Î§
    maxx = np.amax(nodes(:,1))
    maxy = np.amax(nodes(:,2))
    maxz = np.amax(nodes(:,3))
    minx = np.amin(nodes(:,1))
    miny = np.amin(nodes(:,2))
    minz = np.amin(nodes(:,3))
    for i in np.arange(1,Ug.shape[1-1]+1).reshape(-1):
        maxx = np.amax(np.array([maxx,np.amax(nodes(:,1) + Ug(np.arange(1,end()+5,5),i) * scale)]))
        maxy = np.amax(np.array([maxy,np.amax(nodes(:,2) + Ug(np.arange(2,end()+5,5),i) * scale)]))
        maxz = np.amax(np.array([maxz,np.amax(nodes(:,3) + Ug(np.arange(3,end()+5,5),i))]))
        minx = np.amin(np.array([minx,np.amin(nodes(:,1) + Ug(np.arange(1,end()+5,5),i) * scale)]))
        miny = np.amin(np.array([miny,np.amin(nodes(:,2) + Ug(np.arange(2,end()+5,5),i) * scale)]))
        minz = np.amin(np.array([minz,np.amin(nodes(:,3) + Ug(np.arange(3,end()+5,5),i))]))
    
    lenx = maxx - minx
    leny = maxy - miny
    lenz = maxz - minz
    axisscale = 0.3
    axislim = np.array([minx - lenx * axisscale,maxx + lenx * axisscale,miny - leny * axisscale,maxy + leny * axisscale,minz - lenz * axisscale,maxz + lenz])
    plt.figure(figid)
    view(view_pos)
    while count <= Ug.shape[1-1]:

        plot3(nodes(:,1) + Ug(np.arange(1,end()+5,5),count) * scale,nodes(:,2) + Ug(np.arange(2,end()+5,5),count) * scale,nodes(:,3) + Ug(np.arange(3,end()+5,5),count) * scale,'r','LineWidth',2)
        plt.axis(axislim)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.zlabel('Z')
        plt.title(np.array(['t=',num2str(tspan(count))]))
        set(gcf,'Color',np.array([1,1,1]))
        count = count + speed
        pause(1e-05)
        if count <= Ug.shape[1-1]:
            clf(figid)

    
    return
    