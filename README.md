# algorithm
<a name="Ig1MF"></a>
# 实验一：分治算法
<a name="KARRk"></a>
## 实现基于枚举方法的凸包求解算法
<br />算法思想：考虑 Q 中的任意四个点 A、B、C、D，如果 A 处于BCD构成的三角形内部，那么 A 一定不属于凸包 P 的顶点集合。遍历所有点，按以上想法将所有不属于凸包的顶点去除，剩余点即为凸包上的点。剩余点中选取最左侧点为原点，将所有点按斜率排序，原点放在首位，按序连接所有点即为凸包。

算法实现：
```python
import numpy as np
import matplotlib.pyplot as plt
class Convex(object):
    def __init__(self, insize):
        self.insize=insize
        xy=np.random.random((self.insize,2))*100
        angle=np.zeros((self.insize,1))
        self.pointset=np.concatenate((xy,angle),1)
    #搜索x值最小的点
    def searchminx(self,plist):
        minx=100
        index=0
        for i in range(len(plist)):
            if(plist[i][0]<minx):
                minx=plist[i][0]
                index=i
        return index
    #判断点是否在三角形内
    def isTrinside(self,a,b,c,d):
        ab=b-a
        bc=c-b
        ca=a-c
        ad=d-a
        bd=d-b
        cd=d-c
        if((np.cross(ab,ad)>0 and np.cross(bc,bd)>0 and np.cross(ca,cd)>0) or (np.cross(ab,ad)<0 and np.cross(bc,bd)<0 and np.cross(ca,cd)<0)):
            return True
        else:
            return False
    #show
    def show(self,pointset,result):
        plt.scatter(pointset[:,0],pointset[:,1],s=2,c='blue')
        plt.scatter(result[:,0],result[:,1],s=2,c='red')
        x=result[:,0]
        x=np.append(x,result[0][0])
        y=result[:,1]
        y=np.append(y,result[0][1])
        plt.plot(x,y)
        plt.show()
    #基于枚举方法的凸包求解算法
    def enum_point(self):
        for a in range(0,self.insize-2):
            for b in range(a+1,self.insize-1):
                for c in range(a+2,self.insize):
                    for d in range(self.insize):
                        if(self.isTrinside(self.pointset[a][:2],self.pointset[b][:2],self.pointset[c][:2],self.pointset[d][:2]) and self.pointset[d][2]==0):
                            self.pointset[d][2]=-1
        result=[]
        for i in range(self.insize):
            if self.pointset[i][2]!=-1:
                result.append(self.pointset[i])
        index=self.searchminx(result)
        min=result[index]
        del result[index]
        for i in range(len(result)):
            result[i][2]=(result[i][1]-min[1])/(result[i][0]-min[0])
        result.sort(key=lambda y:y[1])
        result.sort(key=lambda x:x[2])
        result.insert(0,min)
        result=np.array(result)
        self.show(self.pointset,result)

```
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726429731-f8cd3c60-30a7-47a1-8240-31f7272ca38f.png#averageHue=%23fcfcfc&clientId=ue9655ccc-0aee-4&from=paste&height=237&id=u45225df8&originHeight=355&originWidth=474&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=20532&status=done&style=none&taskId=u00af34bc-83b9-44a0-851b-dee257cb216&title=&width=316)<br />图 1 枚举结果
<a name="xaYbf"></a>
## 实现基于 Graham-Scan 的凸包求解算法
<br />算法思想：找到点集Q中最左侧点，以此点为原点，将所有点按斜率从小到大排序，原点放在首位。将排序后数组中的前2个值入栈，开始凸包计算。判断数组中下一个点是否在栈顶2个点向量（方向指向栈顶点）的左侧或连线上。若不在，栈顶点不符合要求，需要移除，并继续判断栈顶点。若在，则入栈。当遍历完数组所有值时，程序结束。栈中存储着凸包图形结点。

算法实现：<br />在1中Convex类中添加
```python
 #基于 Graham-Scan 的凸包求解算法
    def grahamscan(self):
        pointset=self.pointset.tolist()
        index=self.searchminx(pointset)
        min=pointset[index]
        del pointset[index]
        for i in range(len(pointset)):
            pointset[i][2]=(pointset[i][1]-min[1])/((pointset[i][0]-min[0]))
        pointset.sort(key=lambda y:y[1])
        pointset.sort(key=lambda x:x[2])
        result=[]
        result.append(min)
        result.append(pointset[0])
        for i in range(1,len(pointset)):
            while(np.cross([result[-1][0]-result[-2][0],result[-1][1]-result[-2][1]],[pointset[i][0]-result[-2][0],pointset[i][1]-result[-2][1]])<0):
                result.pop()
            result.append(pointset[i])
        self.show(self.pointset,np.array(result))

```
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726503263-11acb5de-bfbb-4bca-9db9-7084053547e3.png#averageHue=%23fcfcfc&clientId=ue9655ccc-0aee-4&from=paste&height=241&id=u6f8a05b4&originHeight=362&originWidth=483&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=20452&status=done&style=none&taskId=u6af6041b-8315-4575-8c0c-73d88f53ab3&title=&width=322)<br />图 2 Graham-Scan结果

<a name="oFTHm"></a>
## 实现基于分治思想的凸包求解算法
算法思想：将点集按x坐标从小到大排序，第一个first和最后一个点last一定为凸包上的点。将两点连线，线段将求解凸包问题分解为求解上凸包和下凸包两个问题。对于上凸包，从上侧找一个点max，使与线段形成的三角形面积最大。此点max必为上凸包的点，连接first与max，max与last，重复上述步骤，递归求解，下凸包同理。

算法实现：<br />在1中Convex类中添加

```
#基于分治方法的凸包求解
    def dc(self):
        pointset=self.pointset.tolist()
        pointset.sort(key=lambda y:y[1])
        pointset.sort(key=lambda x:x[0])
        start=0
        end=len(pointset)-1
        result=[pointset[start],pointset[end]]
        self.recursion(start,end,pointset,result)
        self.recursion(end,start,pointset,result)
        min=result[0]
        del result[0]
        for i in range(len(result)):
            result[i][2]=(result[i][1]-min[1])/(result[i][0]-min[0])
        result.sort(key=lambda x:x[2])
        result.insert(0,min)
        self.show(self.pointset,np.array(result))
    def recursion(self,start,end,pointset,result):
        maxs=0
        index=-1
        for i in range(min(start,end)+1,max(start,end)):
             # area=np.cross([pointset[end][0]-pointset[start][0],pointset[end][1]-pointset[start][1]],[pointset[i][0]-pointset[start][0],pointset[i][1]-pointset[start][1]]) 效率低
            area=pointset[end][0]*pointset[i][1]+pointset[end][1]*pointset[start][0]+pointset[i][0]*pointset[start][1]-pointset[end][1]*pointset[i][0]-pointset[end][0]*pointset[start][1]-pointset[i][1]*pointset[start][0]
            if(area>maxs):
                index=i
                maxs=area
        if(index!=-1):
            result.append(pointset[index])
            self.recursion(start,index,pointset,result)
            self.recursion(index,end,pointset,result)

```
![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726544973-8b79e389-7c7c-44b0-8f57-6ef4084178d7.png#averageHue=%23fcfcfc&clientId=ue9655ccc-0aee-4&from=paste&height=300&id=uff37d67c&originHeight=450&originWidth=600&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=28860&status=done&style=none&taskId=u023cde21-5002-4e52-9906-b851fa9e436&title=&width=400)<br />图 3 分治结果
<a name="YQi5q"></a>
## 对比三种凸包求解算法
基于枚举的凸包求解算法时间曲线如图4所示，数据量180，用时超过175000ms。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726574079-bfc91866-ab4d-44e3-a4c5-94fe668e0f3e.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=285&id=ufa78e117&originHeight=427&originWidth=570&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=24472&status=done&style=none&taskId=u660d5beb-4e34-4d3c-a92d-7b205c60dd1&title=&width=380)<br />图 4

基于 Graham-Scan 的凸包求解算法时间曲线如图5所示，数据量10000，用时不足1000ms。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726580155-14f76aa4-3c2a-4acd-a369-76a875a09c23.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=278&id=u1e5344d4&originHeight=417&originWidth=556&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=19820&status=done&style=none&taskId=u5e82bc2e-9ed5-42cd-8146-646c085791a&title=&width=370.6666666666667)<br />图 5

基于分治思想的凸包求解算法时间曲线如图所示, 数据量10000，用时约200ms。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726586842-27ea872b-c9e2-45be-96f8-0b934bda51e4.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=338&id=u6cd27a3a&originHeight=507&originWidth=676&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=34524&status=done&style=none&taskId=u1fa3b82a-2ade-4c21-ab82-63b19c78c78&title=&width=450.6666666666667)<br />图 6

<a name="DY3AP"></a>
# 实验二：搜索算法
<a name="WVPo0"></a>
## <br />实现单向与双向的 A*搜索算法
<br />算法思路：将开始节点加入活结点表，选择活结点表中总距离（已经走过的距离+估算距离终点的距离）最短的点minP，将minP移入死结点表，并将minP符合条件（不是不能走的点，不是死结点表中的点）的相邻节点计算总距离并添加minP为父节点后加入活结点表。若活结点表中有此点，比较两者的总距离，若后加入的总距离小，则用后加入的点替代原点，否则直接加入。重复上述步骤，直到终点加入活结点表，结束。从终点一路找父节点找到起点，即为最短路径。双向A即同时对起点和终点使用A算法，直到活结点表中有相同点。从相同点出发可以到起点和终点，此即为最短路径。

算法实现：
```
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
    #初始化地图
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
                            self.map[x][y].G=minfP.G+1
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)
                        #无视障碍物，估算还要走的距离
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
                            self.map[x][y].G=minfP.G+1
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)
                        self.map[x][y].H=min(abs(x-end.x),abs(y-end.y))*math.sqrt(2)+abs(abs(x-end.x)-abs(y-end.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist1.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1
                        else:
                            changeG=minfP.G+math.sqrt(2)
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
                            self.map[x][y].G=minfP.G+1
                        else:
                            self.map[x][y].G=minfP.G+math.sqrt(2)
                        self.map[x][y].H=min(abs(x-start.x),abs(y-start.y))*math.sqrt(2)+abs(abs(x-start.x)-abs(y-start.y))
                        self.map[x][y].F=self.map[x][y].G+self.map[x][y].H
                        self.map[x][y].parent=minfP
                        openlist2.append(self.map[x][y])
                    else:
                        if minfP.x==x or minfP.y==y:
                            changeG=minfP.G+1
                        else:
                            changeG=minfP.G+math.sqrt(2)
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
map.doubleasingle(map.map[4][5],map.map[13][4])

```

如下图所示，为A_和双向A_算法结果，方式不同，但总路程相同，均为4+5√2<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726791972-24f51064-4120-44e3-a25e-69b5c7f697cb.png#averageHue=%23f3eeee&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u6d8128e8&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=60344&status=done&style=none&taskId=ucb4019b0-4c88-4480-b596-93f41dff1b4&title=&width=577.3333333333334)<br />Figure 1  A*结果<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726801227-8e76c6a7-d3f3-414b-9790-b78804970a0f.png#averageHue=%23f3eeee&clientId=ue9655ccc-0aee-4&from=paste&height=413&id=u56fafa7d&originHeight=620&originWidth=827&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=55593&status=done&style=none&taskId=u15c8097b-93a4-41c5-b220-00e8a37b28f&title=&width=551.3333333333334)<br />Figure 2 双向A*结果
<a name="CONhb"></a>
## <br />测试 A*算法的应用

![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726832402-9be13a66-cae6-4abe-bf79-4986c15e6888.png#averageHue=%23f3f1f1&clientId=ue9655ccc-0aee-4&from=paste&height=325&id=u2a0d8440&originHeight=487&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=63911&status=done&style=none&taskId=ud961478b-09bf-47b3-9d52-81266d45fc1&title=&width=577.3333333333334)<br />Figure 3 A*算法结果<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700726858139-1ca7951e-e935-4af2-a7a6-003b8897e87f.png#averageHue=%23f3f0f0&clientId=ue9655ccc-0aee-4&from=paste&height=325&id=u1f41c2e1&originHeight=487&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=65157&status=done&style=none&taskId=u3322f7f2-7e0c-41e9-b690-9326a061d90&title=&width=577.3333333333334)<br />Figure 4 双向A*算法结果<br />二者路径不同，所走的路程几乎相同，相差不足0.3

<a name="WJyFm"></a>
# 实验三：近似算法
<a name="hbQX8"></a>
## <br />实现基于贪心策略的近似算法
<br />算法思路：选择能覆盖最多未被覆盖元素的子集
> <br />算法Greedy_cover(X, F)<br />输入 : 有限集X, X的子集合族F， X=∪S∈F S，|X|=|F|<br />输出 : C⊆F，满足X=∪S∈F S且C是满足X=∪S∈F S的最小集族，即|C|最小<br />1:  U←X<br />2:  C←θ<br />3:   While   U≠θ   Do<br />4:      贪心选择能覆盖最多U元素的子集S<br />5:      U←U-S<br />6:      C←C∪{S}<br />7:   Return C

<br />算法实现：
```
import numpy as np 
import copy
import pulp 
import time
import matplotlib.pyplot as plt
class Approx(object):
    #初始化输入数据
    def __init__(self,insize):
        self.X=np.random.choice(10000,insize,replace=False).tolist()
        resX=self.X.copy()
        self.F=[]
        choice=np.random.choice(insize,20,replace=False)
        s0=[]
        for i in choice:
            s0.append(resX[i])
        self.F.append(set(s0))
        resX=list(set(resX).difference(set(s0)))
        Us=s0
        while(len(resX)>=20):
            si_n=np.random.randint(1,21)
            si_x=np.random.randint(1,si_n+1)
            si=[]
            choicerex=np.random.choice(len(resX),si_x,replace=False)
            for i in choicerex:
                si.append(resX[i])
            choices=np.random.choice(len(Us),si_n-si_x,replace=False)
            for i in choices:
                si.append(Us[i])
            self.F.append(set(si))
            resX=list(set(resX).difference(set(si)))
            Us=list(set(Us).union(set(si)))
        self.F.append(set(resX))
        count=len(self.F)
        for i in range(insize-count):
            s_n=np.random.randint(1,21)
            choice=np.random.choice(insize,s_n,replace=False)
            s=[]
            for i in choice:
                s.append(self.X[i])
            self.F.append(set(s))
    #贪心
    def greedy(self):
        U=self.X.copy()
        C=[]
        while len(U)>0:
            maxlength=0
            for i in range(len(self.F)):
                if len(self.F[i].intersection(set(U)))>maxlength:
                    maxlength=len(self.F[i].intersection(set(U)))
                    index=i
            U=set(U).difference(self.F[index])
            C.append(self.F[index])
        return C 

```

下图为不同输入数据量大小时，两种算法所得覆盖集中集合个数与所用时间<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727025538-b3d1829c-70ae-48d9-b4bd-f1b5cc601b6e.png#averageHue=%23faf9f9&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u6a965fad&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=57028&status=done&style=none&taskId=u86d5e125-c8cd-4944-8528-0b9c3070155&title=&width=577.3333333333334)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727034004-b619ce7b-2952-4bff-a6ae-c651a4ccd5f3.png#averageHue=%23faf9f9&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u5f22033e&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=53250&status=done&style=none&taskId=uf99e2a34-734b-478b-8c7c-a64900882d4&title=&width=577.3333333333334)
<a name="QZJmb"></a>
## 实现一个基于线性规划近似算法

算法思路：
> 线性规划舍入算法<br />算法Appox_Cover_VC(X, F)<br />输入 : 有限集X, X的子集合族F， X=∪S∈F S，|X|=|F|<br />输出 : C⊆F，满足X=∪S∈F S且C是满足X=∪S∈F S的最小集族，即|C|最小<br />1:  根据X和F的关系，构建线性规划表达式<br />2:  调用pulp库求解LP松弛问题的最优解x<br />3:   For   S∈F   Do<br />4:      If xs≥1/f   then   C←C∪{S}<br />5:   Return C

<br />算法实现：
```
 #线性规划
    def lineprograme(self):
        C=[]
        problem=pulp.LpProblem(name="lineprograme",sense=pulp.LpMinimize)
        index=[i for i in range(len(self.F))]
        xs=pulp.LpVariable.dicts("xs",index,0,1)
        problem+=pulp.lpSum(xs)
        f=0
        for e in self.X:
            xe=[xs[i] for i in range(len(self.F)) if e in self.F[i]]
            problem+=(pulp.lpSum(xe)>=1)
            if(len(xe)>f):
                f=len(xe)
        problem.solve()
        xs=[]
        for v in problem.variables():
            xs.append(v.varValue)
        for i in range(len(xs)):
            if xs[i]>=1.0/f:
                C.append(self.F[i])
        return C

```

下图为不同输入数据量大小时，两种算法所得覆盖集中集合个数与所用时间<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727058828-5e72bc24-7902-4d6e-a917-45cb46246788.png#averageHue=%23f9f9f9&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=ud64d01aa&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=60933&status=done&style=none&taskId=u1a80fcc9-996d-4e09-8618-c0440c27a8d&title=&width=577.3333333333334)<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727067709-a1d7e669-4e40-4145-853f-5d2bda7af9b2.png#averageHue=%23fafafa&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u15dc9781&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=55813&status=done&style=none&taskId=ufcecf087-4a81-4989-8f87-694d11bbefe&title=&width=577.3333333333334)
<a name="maUTm"></a>
# 实验四：快速排序
<a name="H8kvH"></a>
## <br />按照算法导论中给出的伪代码实现快速排序
<br />算法思路：<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727104066-c4e9b6e4-91dc-4a0d-b053-62aced76e4b4.png#averageHue=%23f3f3f3&clientId=ue9655ccc-0aee-4&from=paste&height=476&id=u01d29a01&originHeight=714&originWidth=578&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=99117&status=done&style=none&taskId=u7328b1e6-4376-454d-83ab-f9ef91a2419&title=&width=385.3333333333333)<br />算法实现：
```
import numpy as np
def QuickSort(A,p,r):
    if p<r:
        q=Rand_Partition(A,p,r)
        QuickSort(A,p,q-1)
        QuickSort(A,q+1,r)
def Rand_Partition(A,p,r):
    i=np.random.randint(p,r+1)
    A[r],A[i]=A[i],A[r]
    x=A[r]
    i=p-1
    for j in range(p,r):
        if A[j]<=x:
            i=i+1
            A[i],A[j]=A[j],A[i]
    A[i+1],A[r]=A[r],A[i+1]
    return i+1

array=np.random.randint(0,100,30)
print(array)
QuickSort(array,0,29)
print(array)

```

小样例测试结果正确：<br />输入：[57 34  0 92 77 80 31 30  4 60  3 16 48 39 59 57 37  4 14 12 57 10 27 91<br />43 39 91 17 53 18]<br />输出：[ 0  3  4  4 10 12 14 16 17 18 27 30 31 34 37 39 39 43 48 53 57 57 57 59<br />60 77 80 91 91 92]
<a name="ZpMsG"></a>
## <br />测试算法在不同输入下的表现
<br />算法在数据过大时耗时过长，采用1e4的数据大小计算，结果如下，接下来对算法进行改进。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727167221-33a9bc19-6403-4cd0-a3dc-bf64d6f40879.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u43f8166d&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=38774&status=done&style=none&taskId=uaa74e389-8507-4cc7-8b91-f1e0b4a966b&title=&width=577.3333333333334)<br />调用编程语言库函数中的快速排序算法在各个数据实验数据集上运行算法，用时如图所示，发现相同的数越多，用时越短。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727175478-7e39acf2-325d-435b-bcf0-676b5745e8f9.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=u1241b1a8&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=35318&status=done&style=none&taskId=uc073bced-ee2b-4123-a4b9-91be611fc3a&title=&width=577.3333333333334)<br />对原排序算法进行改进，保证了与锚点相同的在中间，小于的在左边，大于的在右边，中间相等的值不用再进行排序，大大节省计算量。

```
def QuickSort2(A,l,r):
    if l<r:
        p = l
        q = r
        i = np.random.randint(p,r+1)
        x = A[i]
        i = l
        while(i <= q):
            if(A[i] == x):
                i=i+1
                continue
            elif(A[i] < x):
                
                A[i], A[p]=A[p], A[i] 
                i=i+1
                p=p+1 
            else: 
                A[i], A[q]=A[q], A[i]
                q=q-1
        QuickSort2(A, l, p - 1)
        QuickSort2(A, q + 1, r)

```

所得时间结果，相同的数越多，用时越短。<br />![image.png](https://cdn.nlark.com/yuque/0/2023/png/40483545/1700727208691-643bc123-6db2-4bb6-adef-adb57abbc2bb.png#averageHue=%23fbfbfb&clientId=ue9655ccc-0aee-4&from=paste&height=433&id=uec1b795b&originHeight=649&originWidth=866&originalType=binary&ratio=1.5&rotation=0&showTitle=false&size=35228&status=done&style=none&taskId=ufdd7f5bd-3d6d-4639-9285-e556d900edd&title=&width=577.3333333333334)

<a name="vaf3y"></a>
# 附代码
```
import numpy as np 
import copy
import pulp 
import time
import matplotlib.pyplot as plt
class Approx(object):
    #初始化输入数据
    def __init__(self,insize):
        self.X=np.random.choice(10000,insize,replace=False).tolist()
        resX=self.X.copy()
        self.F=[]
        choice=np.random.choice(insize,20,replace=False)
        s0=[]
        for i in choice:
            s0.append(resX[i])
        self.F.append(set(s0))
        resX=list(set(resX).difference(set(s0)))
        Us=s0
        while(len(resX)>=20):
            si_n=np.random.randint(1,21)
            si_x=np.random.randint(1,si_n+1)
            si=[]
            choicerex=np.random.choice(len(resX),si_x,replace=False)
            for i in choicerex:
                si.append(resX[i])
            choices=np.random.choice(len(Us),si_n-si_x,replace=False)
            for i in choices:
                si.append(Us[i])
            self.F.append(set(si))
            resX=list(set(resX).difference(set(si)))
            Us=list(set(Us).union(set(si)))
        self.F.append(set(resX))
        count=len(self.F)
        for i in range(insize-count):
            s_n=np.random.randint(1,21)
            choice=np.random.choice(insize,s_n,replace=False)
            s=[]
            for i in choice:
                s.append(self.X[i])
            self.F.append(set(s))
    #贪心
    def greedy(self):
        U=self.X.copy()
        C=[]
        while len(U)>0:
            maxlength=0
            for i in range(len(self.F)):
                if len(self.F[i].intersection(set(U)))>maxlength:
                    maxlength=len(self.F[i].intersection(set(U)))
                    index=i
            U=set(U).difference(self.F[index])
            C.append(self.F[index])
        return C 
    #线性规划
    def lineprograme(self):
        C=[]
        problem=pulp.LpProblem(name="lineprograme",sense=pulp.LpMinimize)
        index=[i for i in range(len(self.F))]
        xs=pulp.LpVariable.dicts("xs",index,0,1)
        problem+=pulp.lpSum(xs)
        f=0
        # for i in range(len(xs)):
        #     problem+=(xs[i]==0 or xs[i]==1)
            # problem+=(xs[i]>=0)
        for e in self.X:
            xe=[xs[i] for i in range(len(self.F)) if e in self.F[i]]
            problem+=(pulp.lpSum(xe)>=1)
            if(len(xe)>f):
                f=len(xe)
        problem.solve()
        xs=[]
        for v in problem.variables():
            xs.append(v.varValue)
        for i in range(len(xs)):
            if xs[i]>=1.0/f:
                C.append(self.F[i])
        return C
greedy=[]
line=[]
for i in range(100,5000,500):
    a=Approx(i)
    start=time.time()
    C0=a.greedy()
    end=time.time()
    greedy.append([i,end-start,len(C0)])

    # start=time.time()
    # C1=a.lineprograme()
    # end=time.time()
    # line.append([i,end-start,len(C1)])

plt.plot(np.array(greedy)[:,0:1],np.array(greedy)[:,1:2],color='red',label="greedy")
# plt.plot(np.array(line)[:,0:1],np.array(line)[:,1:2],color='blue',label="lineprograme")
plt.xlabel("num_size")
plt.ylabel("time/s")
plt.legend()
plt.title("two algorithms spend time with different input number size")
plt.show()
plt.plot(np.array(greedy)[:,0:1],np.array(greedy)[:,2:3],color='red',label="greedy")
# plt.plot(np.array(line)[:,0:1],np.array(line)[:,2:3],color='blue',label="lineprograme")
plt.xlabel("num_size")
plt.ylabel("number of C")
plt.legend()
plt.title("two algorithms number of result set with different input number size")
plt.show()



```

```
import numpy as np
import time
import matplotlib.pyplot as plt
import sys  # 导入sys模块
sys.setrecursionlimit(30000000)  
def QuickSort(A,p,r):
    if p<r:
        q=Rand_Partition(A,p,r)
        QuickSort(A,p,q-1)
        QuickSort(A,q+1,r)
    else:
        return
def QuickSort2(A,l,r):
    if l<r:
        p = l
        q = r
        i = np.random.randint(p,r+1)
        x = A[i]
        i = l
        while(i <= q):
            if(A[i] == x):
                i=i+1
                continue
            elif(A[i] < x):
                
                A[i], A[p]=A[p], A[i] 
                i=i+1
                p=p+1 
            else: 
                A[i], A[q]=A[q], A[i]
                q=q-1
        QuickSort2(A, l, p - 1)
        QuickSort2(A, q + 1, r)

def Rand_Partition(A,p,r):
    i=np.random.randint(p,r+1)
    A[r],A[i]=A[i],A[r]
    x=A[r]
    i=p-1
    for j in range(p,r):
        if A[j]<=x:
            i=i+1
            A[i],A[j]=A[j],A[i]
    A[i+1],A[r]=A[r],A[i+1]
    return i+1
arraylist=[]
for i in range(11):
    array=np.random.choice(int(1e6),int(1e6-i*1e5),replace=False)
    d=np.random.randint(0,int(1e6))
    if i!=0:
        array=np.concatenate((array,np.full(int(i*1e5),d,int)))
    arraylist.append(array)


for i in range(11):
    start=time.time()
    #太慢
    # QuickSort(arraylist[i],0,int((1e4)-1)) 
    # sorted(arraylist[i])
    QuickSort2(arraylist[i],0,int((1e6)-1))
    end=time.time()
    plt.scatter(i*10,float(end-start)*1000)
    plt.ylabel("time/ms")
    plt.xlabel("repeat persent:%")
    print(i)
plt.show()



```
