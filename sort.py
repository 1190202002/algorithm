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
    # QuickSort(arraylist[i],0,int((1e4)-1))
    # sorted(arraylist[i])
    QuickSort3(arraylist[i],0,int((1e6)-1))
    end=time.time()
    plt.scatter(i*10,float(end-start)*1000)
    plt.ylabel("time/ms")
    plt.xlabel("repeat persent:%")
    print(i)
plt.show()


