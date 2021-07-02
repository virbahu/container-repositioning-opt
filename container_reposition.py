import numpy as np
from scipy.optimize import linprog
def optimize_repositioning(ports, surplus, deficit, costs):
    n=len(ports); c=[]; A_eq=[]; b_eq=[]
    for i in range(n):
        for j in range(n):
            if i!=j: c.append(costs[i][j])
    n_vars=n*(n-1)
    for i in range(n):
        row=[0]*n_vars; idx=0
        for a in range(n):
            for b in range(n):
                if a!=b:
                    if a==i: row[idx]=1
                    if b==i: row[idx]-=1
                    idx+=1
        A_eq.append(row); b_eq.append(surplus[i]-deficit[i])
    bounds=[(0,None)]*n_vars
    res=linprog(c,A_eq=A_eq,b_eq=b_eq,bounds=bounds,method='highs')
    if res.success:
        moves=[]; idx=0
        for i in range(n):
            for j in range(n):
                if i!=j:
                    if res.x[idx]>0.5: moves.append({"from":ports[i],"to":ports[j],"units":round(res.x[idx])})
                    idx+=1
        return {"moves":moves,"total_cost":round(res.fun,0)}
    return {"error":"infeasible"}
if __name__=="__main__":
    ports=["Shanghai","LA","Rotterdam"]; surplus=[100,0,50]; deficit=[0,80,0]
    costs=[[0,3000,2500],[3000,0,4000],[2500,4000,0]]
    print(optimize_repositioning(ports,surplus,deficit,costs))
