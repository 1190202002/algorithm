import math
class Point(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.F=0
        self.G=0
        self.H=0
        self.wall=False
        self.parent=None
#计算openlist中F最小点
def search_minF(inlist):
    minF=1000
    index=0
    for i in range(len(inlist)):
        if(inlist[i].F<minF):
            minF=inlist[i].F
            index=i
    return inlist[index]

dir=[[-1,-1],[0,-1],[1,-1],[-1,0],[-1,1],[1,0],[1,1],[0,1]]
ysize=5
xsize=7
map=[]
for i in range(xsize):
    linemap=[]
    for j in range(ysize):
       linemap.append(Point(i,j))
    map.append(linemap)
start=map[1][2]
end=map[5][2]
map[3][1].wall=True
map[3][2].wall=True
map[3][3].wall=True
openlist=[]
closelist=[]
openlist.append(start)
path=start
while(1):
    minfP=search_minF(openlist)
    openlist.remove(minfP)
    closelist.append(minfP)
    
    for i in range(8):
        x=minfP.x+dir[i][0]
        y=minfP.y+dir[i][1]
        if(0<=x<7 and 0<=y<5 and map[x][y].wall!=True and map[x][y] not in closelist):
            if(map[x][y] not in openlist):
                if(i%2==1):
                    map[x][y].G=minfP.G+1
                else:
                    map[x][y].G=minfP.G+math.sqrt(2)
                map[x][y].H=min(abs(x-end.x),abs(y-end.y))*math.sqrt(2)+abs(abs(x-end.x)-abs(y-end.y))
                map[x][y].F=map[x][y].G+map[x][y].H
                map[x][y].parent=minfP
                openlist.append(map[x][y])
            else:
                if(i%2==1):
                    changeG=minfP.G+1
                else:
                    changeG=minfP.G+math.sqrt(2)
                if(map[x][y].G>changeG):
                    openlist.remove(map[x][y])
                    map[x][y].G=changeG
                    map[x][y].F=map[x][y].G+map[x][y].H
                    map[x][y].parent=minfP
                    openlist.append(map[x][y])
    if(end in openlist): 
        path=minfP
        break
while(path.parent!=None):
    print(path.x,path.y)
    path=path.parent





