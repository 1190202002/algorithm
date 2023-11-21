import math
import numpy as np
import matplotlib.pyplot as plt
class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.F=0
        self.G=0
        self.H=0
        self.wall=False
        self.parent=None

class Map(object):
    def __init__(self,xsize,ysize,wall):
        self.map=[]
        self.path=[]
        for i in range(xsize):
            linemap=[]
            for j in range(ysize):
               linemap.append(Point(i,j))
            self.map.append(linemap)
        for i in range(len(wall)):
            x=wall[i][0]
            y=wall[i][1]
            self.map[x][y].wall=True
    def searchminF(self,inlist):
        minF=1000
        index=0
        for i in range(len(inlist)):
            if(inlist[i].F<minF):
                minF=inlist[i].F
                index=i
        return inlist[index]
    def asingle(self,start,end):
        dir=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        openlist=[]
        closelist=[]
        openlist.append(start)
        while(len(openlist)>0):
            minfP=self.searchminF(openlist)
            openlist.remove(minfP)
            closelist.append(minfP)
            for i in range(8):
                x=minfP.x+dir[i][0]
                y=minfP.y+dir[i][1]
                if(0<=x<len(self.map) and 0<=y<len(self.map[0]) and self.map[x][y].wall!=True and self.map[x][y] not in closelist):
                    if(self.map[x][y] not in openlist):
                        if minfP.x==x or minfP.y==y:
                            self.map[x][y].G=minfP.G+1
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)
                        self.map[x][y].H=min(abs(x-end.x),abs(y-end.y))*math.sqrt(2)+abs(abs(x-end.x)-abs(y-end.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1
                        else:
                            changeG=minfP.G+math.sqrt(2)
                        if(self.map[x][y].G>changeG):
                            openlist.remove(self.map[x][y])
                            self.map[x][y].G=changeG
                            self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                            self.map[x][y].parent=minfP
                            openlist.append(self.map[x][y])
            if(end in openlist):
                x=end.x
                y=end.y
                self.map[x][y].parent=minfP
                if x==minfP.x or y==minfP.y:
                    self.map[x][y].G=minfP.G+1
                else:
                    self.map[x][y].G=minfP.G+math.sqrt(2)
                self.map[x][y].F=self.map[x][y].G
                self.path.insert(0,self.map[x][y])
                while(self.path[0].parent!=None):
                    self.path.insert(0,self.path[0].parent)
                break
    def show(self):
        wallx=[]
        wally=[]
        size=400
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j].wall==True:
                    wallx.append(self.map[i][j].x+0.5)
                    wally.append(self.map[i][j].y+0.5)
        plt.scatter(wallx,wally,s=size,marker='s',c='black')
        pathx=[]
        pathy=[]
        for i in range(len(self.path)):
            pathx.append(self.path[i].x+0.5)
            pathy.append(self.path[i].y+0.5)
        plt.scatter(pathx,pathy,s=size,marker='o',c='red')
        plt.xlim((0, len(self.map)))
        plt.ylim((0, len(self.map[0])))
        plt.xticks(np.arange(0,len(self.map)+1,1))
        plt.yticks(np.arange(0,len(self.map[0])+1,1))
        plt.grid()
        plt.show()
        

            
   
wall=[[6,7],[6,8],[7,6],[7,5],[7,4],[8,4],[8,3],[8,2]]                   
map=Map(17,14,wall)
map.asingle(map.map[4][5],map.map[13][4])
map.show()






