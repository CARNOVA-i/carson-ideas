#!/usr/bin/env python3
"""Simulation Gate 3: distributed singularity-coordinate network."""
from __future__ import annotations
import csv, hashlib, json, time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

SEED=20261015; NS=(1,2,4,8,16); SNRS=(40.,30.,20.,10.); TRIALS=100
EXTENT=2.5; GRID=31; SIGMA=1.8; NAMES=("dx","dy","alpha","beta")
CONFIGS={"nominal":np.array([0,0,0,0.]),"translation":np.array([.08,-.06,0,0.]),"alpha":np.array([0,0,.08,0]),"beta":np.array([0,0,0,.08]),"mixed":np.array([-.06,.05,.06,-.05]),"edge":np.array([.09,.07,-.08,.07])}
ROOT=Path(__file__).resolve().parents[1]; FIG=ROOT/"figures"; CSV=Path(__file__).with_name("simulation_gate_3_results.csv"); SUMMARY=Path(__file__).with_name("simulation_gate_3_summary.json")

def grid():
 a=np.linspace(-EXTENT,EXTENT,GRID); return np.meshgrid(a,a,indexing="xy"),a[1]-a[0]

def candidate_points():
 return np.array([(x,y) for y in np.linspace(-1.35,1.35,7) for x in np.linspace(-1.35,1.35,7) if .45<np.hypot(x,y)<1.85])

def response(p):
 x,y=p; return np.array([[1,0,x,y],[0,1,-y,x]])

def placement(strategy,n):
 c=candidate_points()
 if strategy=="naive":
  angles=np.linspace(0,2*np.pi,n,endpoint=False); return np.c_[1.05*np.cos(angles),1.05*np.sin(angles)]
 if strategy=="diverse":
  order=np.argsort(np.sin(3*np.arctan2(c[:,1],c[:,0]))+.2*np.hypot(c[:,0],c[:,1])); idx=np.linspace(0,len(order)-1,n,dtype=int); return c[order[idx]]
 chosen=[int(np.argmax(np.sum(c*c,axis=1)))]
 while len(chosen)<n:
  best=None; score=-np.inf
  for j in range(len(c)):
   if j in chosen or np.min(np.linalg.norm(c[j]-c[chosen],axis=1))<.42: continue
   h=np.vstack([response(p) for p in c[chosen+[j]]]); f=h.T@h+1e-9*np.eye(4); s=np.linalg.slogdet(f)[1]
   if s>score: score=s; best=j
  chosen.append(best)
 return c[chosen]

def positions(base,theta):
 return np.array([p+response(p)@theta for p in base])

def field(xx,yy,pos):
 z=np.ones_like(xx,dtype=complex)
 for x,y in pos: z*=((xx-x)+1j*(yy-y))
 z*=np.exp(-(xx*xx+yy*yy)/(2*SIGMA**2)); z/=np.sqrt(np.mean(np.abs(z)**2)); return z

def variance(clean,snr): return float(np.mean(np.abs(clean)**2)/10**(snr/10))
def rv(z): return np.r_[z.real.ravel(),z.imag.ravel()]
def sym(a): return .5*(a+a.T)
def pinv(a):
 w,v=np.linalg.eigh(sym(a)); cut=max(np.max(w)*1e-9,1e-14); q=np.zeros_like(w); np.divide(1,w,out=q,where=w>cut); return (v*q)@v.T

def full_fisher(xx,yy,base,theta,gain,var):
 h=1e-5; cols=[]
 for j in range(4):
  d=np.zeros(4); d[j]=h; cols.append(gain*(field(xx,yy,positions(base,theta+d))-field(xx,yy,positions(base,theta-d)))/(2*h))
 t=field(xx,yy,positions(base,theta)); cols += [t,1j*t]; J=np.column_stack([c.ravel() for c in cols]); f=2/var*np.real(J.conj().T@J)
 return sym(f[:4,:4]-f[:4,4:]@np.linalg.pinv(f[4:,4:])@f[4:,:4])

def extract(xx,yy,obs,centers,spacing):
 out=[]; failures={"missed":0,"false":0,"assignment":0,"topology":0,"exit":0}
 for cx,cy in centers:
  if abs(cx)>1.9 or abs(cy)>1.9: failures["exit"]+=1; return None,failures
  mask=(abs(xx-cx)<=.34)&(abs(yy-cy)<=.34); k=np.unravel_index(np.argmin(np.where(mask,abs(obs),np.inf)),obs.shape); r,c=k
  if r<1 or c<1 or r>=GRID-1 or c>=GRID-1: failures["missed"]+=1; return None,failures
  sr,sc=slice(r-1,r+2),slice(c-1,c+2); x=xx[sr,sc].ravel(); y=yy[sr,sc].ravel(); z=obs[sr,sc].ravel(); A=np.c_[np.ones(9),x,y]
  cr=np.linalg.lstsq(A,z.real,rcond=None)[0]; ci=np.linalg.lstsq(A,z.imag,rcond=None)[0]; J=np.array([[cr[1],cr[2]],[ci[1],ci[2]]])
  if np.linalg.cond(J)>1e7: failures["missed"]+=1; return None,failures
  q=np.linalg.solve(J,-np.array([cr[0],ci[0]]))
  if np.linalg.norm(q-[cx,cy])>.42: failures["assignment"]+=1; return None,failures
  out.extend(q)
 return np.array(out),failures

def retention(info,full):
 w,v=np.linalg.eigh(full); W=(v*(1/np.sqrt(np.maximum(w,1e-14))))@v.T; e=np.clip(np.linalg.eigvalsh(sym(W@info@W)),0,1)
 per=np.clip(np.diag(info)/np.maximum(np.diag(full),1e-14),0,1); return e,float(np.mean(e)),float(np.prod(np.maximum(e,1e-15))**.25),per

def run_condition(rng,xx,yy,spacing,strategy,n,label,theta,snr):
 base=placement(strategy,n); true=positions(base,theta); gain=1.2*np.exp(.7j); clean=gain*field(xx,yy,true); var=variance(clean,snr); tf=time.perf_counter(); full=full_fisher(xx,yy,base,theta,gain,var); full_ms=1000*(time.perf_counter()-tf); H=np.vstack([response(p) for p in base])
 ideal_samples=[]; practical=[]; fail={k:0 for k in ("missed","false","assignment","topology","exit")}; tex=tm=0.
 for _ in range(TRIALS):
  noise=np.sqrt(var/2)*(rng.standard_normal(clean.shape)+1j*rng.standard_normal(clean.shape)); obs=clean+noise
  t=time.perf_counter(); a,fa=extract(xx,yy,obs,true,spacing); tex+=time.perf_counter()-t
  b,fb=extract(xx,yy,obs,base,spacing); tm+=time.perf_counter()-t-(tex/TRIALS if False else 0)
  if a is not None: ideal_samples.append(a)
  if b is not None: practical.append(b)
  for k in fail: fail[k]+=fb[k]
 def calc(samples):
  if len(samples)<max(12,2*n+2): return np.zeros((4,4)),None,None
  E=np.asarray(samples)-true.ravel(); C=sym(E.T@E/len(E)); I=sym(H.T@pinv(C)@H); G=pinv(I)@H.T@pinv(C); err=E@G.T; return I,np.sqrt(np.mean(err*err,axis=0)),err.mean(0)
 Ii,_,_=calc(ideal_samples); Ip,rmse,bias=calc(practical); ei,ri,di,pi=retention(Ii,full); ep,rp,dp,pp=retention(Ip,full); ep=np.minimum(ep,ei); rp=min(rp,ri); dp=min(dp,di); loss=max(0.,ri-rp)
 return {"snr_db":snr,"target_configuration":label,"placement":strategy,"N":n,"state_dimension":2*n,"compression_ratio":1922/(2*n),"ideal_joint_retention":ri,"practical_joint_retention":rp,"determinant_retention":dp,"ideal_generalized_eigenvalues":json.dumps(ei.tolist()),"practical_generalized_eigenvalues":json.dumps(ep.tolist()),**{f"retention_{k}":float(pp[i]) for i,k in enumerate(NAMES)},"rank":int(np.linalg.matrix_rank(Ip,tol=max(np.max(np.linalg.eigvalsh(Ip))*1e-9,1e-12))),"condition_number":float(np.linalg.cond(Ip)),"minimum_generalized_eigenvalue":float(ep.min()),"extraction_loss":loss,**{f"rmse_{k}":None if rmse is None else float(rmse[i]) for i,k in enumerate(NAMES)},**{f"bias_{k}":None if bias is None else float(bias[i]) for i,k in enumerate(NAMES)},"singularity_extraction_failures":fail["missed"],"assignment_failures":fail["assignment"],"topology_failures":fail["topology"],"detector_exit_failures":fail["exit"],"false_singularity_failures":fail["false"],"failure_rate":1-len(practical)/TRIALS,"extraction_runtime_ms":1000*tex/TRIALS,"matching_runtime_ms":1000*tm/TRIALS,"estimation_runtime_ms":0.,"total_runtime_ms":1000*(tex+tm)/TRIALS,"full_field_runtime_ms":full_ms}

def summarize(rows,checks):
 overall={}
 for s in ("naive","diverse","optimized"):
  overall[s]={}
  for n in NS:
   rr=[r for r in rows if r["placement"]==s and r["N"]==n]; overall[s][str(n)]={"state_dimension":2*n,"compression_ratio":1922/(2*n),"ideal_joint_retention":float(np.mean([r["ideal_joint_retention"] for r in rr])),"practical_joint_retention":float(np.mean([r["practical_joint_retention"] for r in rr])),"per_parameter":{k:float(np.mean([r[f"retention_{k}"] for r in rr])) for k in NAMES},"worst_parameter":float(min(np.mean([r[f"retention_{k}"] for r in rr]) for k in NAMES)),"failure_rate":float(np.mean([r["failure_rate"] for r in rr])),"extraction_loss":float(np.mean([r["extraction_loss"] for r in rr])),"total_runtime_ms":float(np.mean([r["total_runtime_ms"] for r in rr]))}
 candidates=[(s,n,v) for s,d in overall.items() for n,v in d.items() if int(n)<=16 and v["practical_joint_retention"]>=.9 and v["worst_parameter"]>=.7 and v["failure_rate"]<=.05]
 best=max(((s,n,v) for s,d in overall.items() for n,v in d.items()),key=lambda x:x[2]["practical_joint_retention"]); verdict="PASS" if candidates else ("CONDITIONAL PASS" if best[2]["practical_joint_retention"]>=.75 else "FAIL")
 return {"seed":SEED,"trials_per_condition":TRIALS,"conditions":len(NS)*3*len(CONFIGS)*len(SNRS),"total_paired_trials":len(NS)*3*len(CONFIGS)*len(SNRS)*TRIALS,"field":"normalized Gaussian-envelope product of controlled simple vortices","parameters":list(NAMES),"counts":list(NS),"placements":["naive","diverse","optimized"],"decision":{"joint":.9,"worst":.7,"max_N":16},"overall":overall,"best":{"placement":best[0],"N":int(best[1]),**best[2]},"smallest_passing":None if not candidates else min(candidates,key=lambda x:int(x[1]))[0:2],"verdict":verdict,"self_checks":checks}

def checks(xx,yy):
 b=placement("optimized",8); t=CONFIGS["mixed"]; p=positions(b,t); f=field(xx,yy,p); g=1.7*np.exp(1.2j); a,_=extract(xx,yy,f,p,0); q,_=extract(xx,yy,g*f,p,0); F=full_fisher(xx,yy,b,t,1+0j,variance(f,30)); return {"full_fisher_symmetry":bool(np.allclose(F,F.T)),"full_fisher_psd":bool(np.linalg.eigvalsh(F).min()>-1e-8),"full_rank":bool(np.linalg.matrix_rank(F)==4),"gain_invariance":bool(a is not None and q is not None and np.linalg.norm(a-q)<1e-9),"count_stable":bool(a is not None and len(a)==16),"assignment_correct":bool(a is not None and np.max(np.linalg.norm(a.reshape(-1,2)-p,axis=1))<.15)}

def figures(summary):
 FIG.mkdir(exist_ok=True); colors={"naive":"C0","diverse":"C1","optimized":"C2"}
 fig,ax=plt.subplots(figsize=(7.5,4.8),constrained_layout=True)
 for s in colors: ax.plot(NS,[summary["overall"][s][str(n)]["practical_joint_retention"] for n in NS],"o-",label=s,color=colors[s])
 ax.axhline(.9,color="k",ls="--"); ax.set(xlabel="singularity count N",ylabel="practical joint retention",title="Information versus network size",ylim=(0,1.05)); ax.legend(); ax.grid(alpha=.3); fig.savefig(FIG/"simulation_gate_3_information_vs_count.png",dpi=180); plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4.8),constrained_layout=True); x=np.arange(3); w=.15
 for j,n in enumerate((4,8,16)): ax.bar(x+(j-1)*w,[summary["overall"][s][str(n)]["practical_joint_retention"] for s in colors],w,label=f"N={n}")
 ax.set_xticks(x,list(colors)); ax.set(ylabel="practical joint retention",title="Placement comparison"); ax.legend(); fig.savefig(FIG/"simulation_gate_3_placement_comparison.png",dpi=180); plt.close(fig)
 best=summary["best"]; vals=[best["per_parameter"][k] for k in NAMES]; fig,ax=plt.subplots(figsize=(7,4.5),constrained_layout=True); ax.bar(NAMES,vals); ax.axhline(.7,color="k",ls="--"); ax.set(title=f"Best network mode retention: {best['placement']} N={best['N']}",ylabel="retention",ylim=(0,1.05)); fig.savefig(FIG/"simulation_gate_3_mode_retention.png",dpi=180); plt.close(fig)
 fig,axs=plt.subplots(1,3,figsize=(11,3.8),constrained_layout=True)
 for ax,s in zip(axs,colors):
  p=placement(s,8); ax.scatter(p[:,0],p[:,1]);
  for i,(x,y) in enumerate(p): ax.text(x,y,str(i+1)); ax.arrow(x,y,.12*x,-.12*y,width=.006,color="C1"); ax.arrow(x,y,.12*y,.12*x,width=.006,color="C2")
  ax.set(title=s,xlim=(-1.8,1.8),ylim=(-1.8,1.8),aspect="equal"); ax.grid(alpha=.2)
 fig.savefig(FIG/"simulation_gate_3_network_geometry.png",dpi=180); plt.close(fig)

def main():
 (xx,yy),sp=grid(); ck=checks(xx,yy); assert all(ck.values()),ck; rng=np.random.default_rng(SEED); rows=[]
 for s in ("naive","diverse","optimized"):
  for n in NS:
   for label,t in CONFIGS.items():
    for snr in SNRS: rows.append(run_condition(rng,xx,yy,sp,s,n,label,t,snr))
 summary=summarize(rows,ck); keys=list(rows[0]);
 with CSV.open("w",newline="",encoding="utf-8") as h: w=csv.DictWriter(h,fieldnames=keys); w.writeheader(); w.writerows(rows)
 figures(summary); stable=json.loads(json.dumps(summary));
 for d in stable["overall"].values():
  for v in d.values(): v.pop("total_runtime_ms",None)
 stable["best"].pop("total_runtime_ms",None)
 summary["deterministic_digest_excluding_timing"]=hashlib.sha256(json.dumps(stable,sort_keys=True).encode()).hexdigest(); SUMMARY.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8"); print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
