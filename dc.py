import numpy as np
import matplotlib.pyplot as plt
import time
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
        # self.show(self.pointset,np.array(result))
    def recursion(self,start,end,pointset,result):
        maxs=0
        index=-1
        for i in range(min(start,end)+1,max(start,end)):
            area=np.cross([pointset[end][0]-pointset[start][0],pointset[end][1]-pointset[start][1]],[pointset[i][0]-pointset[start][0],pointset[i][1]-pointset[start][1]])
            if(area>maxs):
                index=i
                maxs=area
        if(index!=-1):
            result.append(pointset[index])
            self.recursion(start,index,pointset,result)
            self.recursion(index,end,pointset,result)
list1=[]
list2=[]
list3=[]
x=[]
for i in range(10,500,50):
     x.append(i)
     convex=Convex(i)
     start=time.time()
     convex.dc()
     end=time.time()
     list1.append(end-start)
plt.plot(x,list1)
plt.show()