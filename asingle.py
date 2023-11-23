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
        self.cost=0

class Map(object):
    #初始化地图
    def __init__(self,xsize,ysize,wall,river,sland):
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
        for i in range(len(river)):
            x=river[i][0]
            y=river[i][1]
            self.map[x][y].cost=2
        for i in range(len(sland)):
            x=sland[i][0]
            y=sland[i][1]
            self.map[x][y].cost=4
    #搜索节点表中总距离最小点
    def searchminF(self,inlist):
        minF=1000
        index=0
        for i in range(len(inlist)):
            if(inlist[i].F<minF):
                minF=inlist[i].F
                index=i
        return inlist[index]
    #A*算法
    def asingle(self,start,end):
        dir=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        openlist=[]
        closelist=[]
        openlist.append(start)
        while(1):
            minfP=self.searchminF(openlist)
            openlist.remove(minfP)
            closelist.append(minfP)
            for i in range(8):
                x=minfP.x+dir[i][0]
                y=minfP.y+dir[i][1]
                if(0<=x<len(self.map) and 0<=y<len(self.map[0]) and self.map[x][y].wall!=True and self.map[x][y] not in closelist):
                    if(self.map[x][y] not in openlist):
                        #已经走的距离=父节点已经走的距离+父节点到此节点距离
                        if minfP.x==x or minfP.y==y:
                            self.map[x][y].G=minfP.G+1+self.map[x][y].cost
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)+self.map[x][y].cost
                        #无视障碍物，估算还要走的距离
                        self.map[x][y].H=min(abs(x-end.x),abs(y-end.y))*math.sqrt(2)+abs(abs(x-end.x)-abs(y-end.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1+self.map[x][y].cost
                        else:
                            changeG=minfP.G+math.sqrt(2)+self.map[x][y].cost
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
                    self.map[x][y].G=minfP.G+1+self.map[x][y].cost
                else:
                    self.map[x][y].G=minfP.G+math.sqrt(2)+self.map[x][y].cost
                self.map[x][y].F=self.map[x][y].G
                self.path.insert(0,self.map[x][y])
                while(self.path[0].parent!=None):
                    self.path.insert(0,self.path[0].parent)
                break
        self.show()   
    #双向A*算法
    def doubleasingle(self,start,end):
        dir=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
        openlist1=[]
        closelist=[]
        openlist1.append(start)
        openlist2=[]
        openlist2.append(end)
        finish=False
        parent=start
        while(1):
            #起点A*
            minfP=self.searchminF(openlist1)
            openlist1.remove(minfP)
            closelist.append(minfP)
            for i in range(8):
                x=minfP.x+dir[i][0]
                y=minfP.y+dir[i][1]
                if(0<=x<len(self.map) and 0<=y<len(self.map[0]) and self.map[x][y].wall!=True and self.map[x][y] not in closelist):
                    if self.map[x][y] in openlist2:
                        finish=True
                        parent=self.map[x][y].parent
                        connect=self.map[x][y]
                    if(self.map[x][y] not in openlist1):
                        if minfP.x==x or minfP.y==y:
                            self.map[x][y].G=minfP.G+1+self.map[x][y].cost
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)+self.map[x][y].cost
                        self.map[x][y].H=min(abs(x-end.x),abs(y-end.y))*math.sqrt(2)+abs(abs(x-end.x)-abs(y-end.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist1.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1+self.map[x][y].cost
                        else:
                            changeG=minfP.G+math.sqrt(2)+self.map[x][y].cost
                        if(self.map[x][y].G>changeG):
                            openlist1.remove(self.map[x][y])
                            self.map[x][y].G=changeG
                            self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                            self.map[x][y].parent=minfP
                            openlist1.append(self.map[x][y])
            if(finish): break
            #终点A*
            minfP=self.searchminF(openlist2)
            openlist2.remove(minfP)
            closelist.append(minfP)
            for i in range(8):
                x=minfP.x+dir[i][0]
                y=minfP.y+dir[i][1]
                if(0<=x<len(self.map) and 0<=y<len(self.map[0]) and self.map[x][y].wall!=True and self.map[x][y] not in closelist):
                    if self.map[x][y] in openlist1:
                        finish=True
                        parent=self.map[x][y].parent
                        connect=self.map[x][y]
                    if(self.map[x][y] not in openlist2):
                        if minfP.x==x or minfP.y==y:
                            self.map[x][y].G=minfP.G+1+self.map[x][y].cost
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)+self.map[x][y].cost
                        self.map[x][y].H=min(abs(x-start.x),abs(y-start.y))*math.sqrt(2)+abs(abs(x-start.x)-abs(y-start.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist2.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1+self.map[x][y].cost
                        else:
                            changeG=minfP.G+math.sqrt(2)+self.map[x][y].cost
                        if(self.map[x][y].G>changeG):
                            openlist2.remove(self.map[x][y])
                            self.map[x][y].G=changeG
                            self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                            self.map[x][y].parent=minfP 
                            openlist2.append(self.map[x][y])
            if(finish): break
        self.path.insert(0,connect)
        while(self.path[0].parent!=None):
            self.path.insert(0,self.path[0].parent)
        self.path.append(parent)
        while(self.path[-1].parent!=None):
            self.path.append(self.path[-1].parent)
        self.show()            
    #显示结果          
    def show(self):
        wallx=[]
        wally=[]
        riverx=[]
        rivery=[]
        slandx=[]
        slandy=[]
        size=200
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j].wall==True:
                    wallx.append(self.map[i][j].x+0.5)
                    wally.append(self.map[i][j].y+0.5)
                if self.map[i][j].cost==2:
                    riverx.append(self.map[i][j].x+0.5)
                    rivery.append(self.map[i][j].y+0.5)
                if self.map[i][j].cost==4:
                    slandx.append(self.map[i][j].x+0.5)
                    slandy.append(self.map[i][j].y+0.5) 
        plt.scatter(wallx,wally,s=size,marker='s',c='black')
        plt.scatter(riverx,rivery,s=size,marker='s',c='blue')
        plt.scatter(slandx,slandy,s=size,marker='s',c='yellow')
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
        
wall=[[0,17],[1,17],[2,8],[2,9],[2,12],[2,13],[2,17],[3,0],[3,1],[3,3],[3,4],[3,5],[3,6],[3,7],[3,8],[3,13],[3,17],[3,19],[4,4],[4,8],[4,13],[4,17],[5,4],[5,8],[5,9],[5,10],[5,11],[5,12],[5,13],[5,17],[6,4],[6,13],[7,0],[7,1],[7,2],[7,4],[7,9],[7,10],[7,12],[7,13],[7,14],[7,17],[7,18],[7,19]
,[8,4],[8,5],[8,6],[8,7],[8,8],[8,9],[8,14],[8,16],[8,17],[9,6],[9,17],[10,17],[11,6],[12,0],[12,1],[12,2],[12,3],[12,4],[12,5],[12,6],[12,7],[12,12],[12,13],[12,14],[12,15],[12,16],[12,17],[12,18],[12,19],[19,7],[19,8],[19,9],[20,7],[20,8],[20,9],[21,7],[21,8],[21,9],[24,3],[24,4],[25,3],[25,4],[28,9],[31,6],[31,8],[36,10],[36,12]]                   
river=[[28,0],[29,0],[30,0],[29,1],[30,1],[31,1],[30,2],[31,2],[32,2],[31,3],[32,3],[33,3],[31,4],[32,4],[33,4],[32,5],[33,5],[34,5],[32,6],[33,6],[34,6],[33,7],[34,7],[32,8],[34,8],[35,8],[32,9],[33,9],[35,9],[36,9],[32,10],[33,10],[34,10],[32,11],[33,11],[34,11],[35,11]
,[33,12],[34,12],[35,12],[33,13],[34,13],[33,14],[34,14],[33,15],[32,16],[33,17],[34,18]]
sland=[[24,19],[25,19],[26,19],[27,19],[28,19],[29,19],[30,19],[31,19],[32,19],[33,19],[34,19],[35,19],[36,19],[37,19],[38,19],[39,19],[25,18],[26,18],[27,18],[28,18],[29,18],[30,18],[31,18],[32,18],[33,18],[35,18],[36,18],[37,18],[38,18],[39,18],[26,17],[27,17],[28,17],[29,17],[30,17],[31,17],[32,17],[34,17],[35,17],[36,17],[37,17],[38,17],[39,17]
,[26,16],[27,16],[28,16],[29,16],[30,16],[31,16],[33,16],[34,16],[35,16],[36,16],[26,15],[27,15],[28,15],[29,15],[30,15],[31,15],[32,15],[34,15],[35,15],[27,14],[28,14],[29,14],[30,14],[31,14],[32,14],[27,13],[28,13],[29,13],[30,13],[31,13],[32,13],[29,12],[30,12],[31,12],[32,12]]
map=Map(40,20,wall,river,sland)
# map.asingle(map.map[4][9],map.map[35][19])
map.doubleasingle(map.map[4][9],map.map[35][19])







