function movie_plot(nodes,Ug,tspan,speed,scale,view_pos,figid)
    count=1;
    %ºÏÊÊµÄ×ø±êÖá·¶Î§
    maxx=max(nodes(:,1));
    maxy=max(nodes(:,2));
    maxz=max(nodes(:,3));
    minx=min(nodes(:,1));
    miny=min(nodes(:,2));
    minz=min(nodes(:,3));
    for i=1:size(Ug,1)
        maxx=max([maxx,max(nodes(:,1)+Ug(1:5:end,i)*scale)]);
        maxy=max([maxy,max(nodes(:,2)+Ug(2:5:end,i)*scale)]);
        maxz=max([maxz,max(nodes(:,3)+Ug(3:5:end,i))]);
        minx=min([minx,min(nodes(:,1)+Ug(1:5:end,i)*scale)]);
        miny=min([miny,min(nodes(:,2)+Ug(2:5:end,i)*scale)]);
        minz=min([minz,min(nodes(:,3)+Ug(3:5:end,i))]);
    end
    lenx=maxx-minx;
    leny=maxy-miny;
    lenz=maxz-minz;
    axisscale=0.3;
    axislim=[minx-lenx*axisscale,maxx+lenx*axisscale,...
             miny-leny*axisscale,maxy+leny*axisscale,...
             minz-lenz*axisscale,maxz+lenz];
    figure(figid)
    view(view_pos)
    while count<=size(Ug,1)
        plot3(nodes(:,1)+Ug(1:5:end,count)*scale,...
             nodes(:,2)+Ug(2:5:end,count)*scale,...
             nodes(:,3)+Ug(3:5:end,count)*scale,'r','LineWidth',2)
        axis(axislim)
        xlabel('X')
        ylabel('Y')
        zlabel('Z')
        title(['t=',num2str(tspan(count))])
        set(gcf,'Color',[1,1,1])
        count=count+speed;
        pause(0.00001)
        if count<=size(Ug,1)
            clf(figid)
        end
        
    end
end