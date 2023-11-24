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


