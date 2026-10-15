#!/usr/bin/env python3
"""Simulation Gate 2: bounded multi-mode compact-state information test."""

from __future__ import annotations

import argparse, csv, hashlib, json, time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

SEED = 20261015
GRID_SIZE, EXTENT, SIGMA = 31, 2.5, 1.15
SNRS = (40.0, 30.0, 20.0, 10.0)
TRIALS = 120
STEP = np.array([2e-5, 2e-5, 2e-5, 2e-5])
NAMES = ("dx", "dy", "alpha", "beta")
CONFIGS = {
    "nominal": np.array([0.0, 0.0, 0.0, 0.0]),
    "translated": np.array([0.18, -0.14, 0.0, 0.0]),
    "deformation": np.array([0.0, 0.0, 0.18, 0.22]),
    "mixed": np.array([-0.16, 0.12, -0.16, 0.20]),
    "conditioned_edge": np.array([0.24, 0.21, 0.24, -0.26]),
}
ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
CSV_PATH = Path(__file__).with_name("simulation_gate_2_results.csv")
JSON_PATH = Path(__file__).with_name("simulation_gate_2_summary.json")


def grid():
    axis = np.linspace(-EXTENT, EXTENT, GRID_SIZE)
    return np.meshgrid(axis, axis, indexing="xy")


def field(xx, yy, theta):
    """Controlled zero with anisotropy alpha and radial phase curvature beta."""
    dx, dy, alpha, beta = theta
    u, v = xx - dx, yy - dy
    r2 = u*u + v*v
    envelope = np.exp(-((1 + alpha)*u*u + (1 - alpha)*v*v)/(2*SIGMA**2))
    phase = np.exp(1j * beta * r2 / SIGMA**2)
    return (u + 1j*v) * envelope * phase


def noise_variance(signal, snr):
    return float(np.mean(np.abs(signal)**2) / 10**(snr/10))


def realvec(z):
    return np.r_[z.real.ravel(), z.imag.ravel()]


def target_derivatives(xx, yy, theta):
    out = []
    for j, h in enumerate(STEP):
        d = np.zeros(4); d[j] = h
        out.append((field(xx, yy, theta+d)-field(xx, yy, theta-d))/(2*h))
    return out


def efficient_full_fisher(xx, yy, theta, gain, variance):
    template = field(xx, yy, theta)
    cols = [gain*d for d in target_derivatives(xx, yy, theta)] + [template, 1j*template]
    jac = np.column_stack([c.ravel() for c in cols])
    f = (2/variance)*np.real(jac.conj().T @ jac)
    return sym(f[:4,:4] - f[:4,4:] @ np.linalg.pinv(f[4:,4:]) @ f[4:,:4])


def affine_fit(xx, yy, observed, radius=2):
    admitted = (np.abs(xx) <= .65) & (np.abs(yy) <= .65)
    row, col = np.unravel_index(np.argmin(np.where(admitted, np.abs(observed), np.inf)), observed.shape)
    if min(row, col) < radius or row >= GRID_SIZE-radius or col >= GRID_SIZE-radius:
        raise ValueError("window")
    sr, sc = slice(row-radius,row+radius+1), slice(col-radius,col+radius+1)
    x, y, z = xx[sr,sc].ravel(), yy[sr,sc].ravel(), observed[sr,sc].ravel()
    a = np.column_stack((np.ones(x.size), x, y))
    cr = np.linalg.lstsq(a, z.real, rcond=None)[0]
    ci = np.linalg.lstsq(a, z.imag, rcond=None)[0]
    jac = np.array([[cr[1],cr[2]],[ci[1],ci[2]]])
    if not np.isfinite(np.linalg.cond(jac)) or np.linalg.cond(jac)>1e6: raise ValueError("jacobian")
    loc = np.linalg.solve(jac, -np.array([cr[0],ci[0]]))
    if not np.all(np.isfinite(loc)) or np.any(np.abs(loc)>EXTENT): raise ValueError("location")
    return loc, jac, (row, col)


def invariant_patch(observed, rc, radius=2):
    row,col=rc; p=observed[row-radius:row+radius+1,col-radius:col+radius+1].ravel()
    norm=np.linalg.norm(p)
    if norm < 1e-14: raise ValueError("patch norm")
    q=p/norm
    anchor=np.vdot(np.arange(1,p.size+1), q)
    if abs(anchor)>1e-14: q=q*np.exp(-1j*np.angle(anchor))
    return np.r_[q.real,q.imag]


def states(xx, yy, observed):
    loc,jac,rc=affine_fit(xx,yy,observed)
    gram=jac.T@jac; gram/=max(np.trace(gram),1e-15)
    s6=np.r_[loc,gram[0,0],gram[0,1],gram[1,1],np.linalg.det(gram)]
    row,col=rc; r=3
    sr,sc=slice(row-r,row+r+1),slice(col-r,col+r+1)
    x=(xx[sr,sc]-loc[0]).ravel(); y=(yy[sr,sc]-loc[1]).ravel(); z=observed[sr,sc].ravel()
    scale=xx[0,1]-xx[0,0]
    design=np.column_stack((np.ones(x.size),x,y,x*x,x*y,y*y,x**3,x*x*y,x*y*y,y**3))
    c=np.linalg.lstsq(design,z,rcond=None)[0]
    ref=c[1] if abs(c[1])>1e-12 else c[2]
    ratios=np.array([c[2]/ref,c[3]*scale/ref,c[4]*scale/ref,c[5]*scale/ref,c[6]*scale**2/ref,c[9]*scale**2/ref])
    rich=np.r_[loc,ratios.real,ratios.imag]
    patch=invariant_patch(observed,rc)
    return {"S2_position":loc,"S6_jacobian":s6,"S14_descriptor":rich,"P50_patch":patch}


def sym(a): return .5*(a+a.T)


def pinv_psd(a, rcond=1e-9):
    w,v=np.linalg.eigh(sym(a)); cutoff=max(np.max(w)*rcond,1e-14)
    inverse=np.zeros_like(w); np.divide(1.0,w,out=inverse,where=w>cutoff)
    return (v*inverse)@v.T


def feature_jacobian(xx,yy,theta,gain,name):
    cols=[]
    for j,h in enumerate(STEP):
        d=np.zeros(4); d[j]=h
        cols.append((states(xx,yy,gain*field(xx,yy,theta+d))[name]-states(xx,yy,gain*field(xx,yy,theta-d))[name])/(2*h))
    return np.column_stack(cols)


def generalized_retention(info, full):
    wf,vf=np.linalg.eigh(sym(full)); wf=np.maximum(wf,1e-14)
    invsqrt=(vf*(1/np.sqrt(wf)))@vf.T
    vals=np.linalg.eigvalsh(sym(invsqrt@info@invsqrt))
    vals=np.clip(vals,0,1)
    return vals, float(np.mean(vals)), float(np.prod(np.maximum(vals,1e-15))**.25)


def run_condition(rng,xx,yy,label,theta,snr):
    gain=1.25*np.exp(.73j); clean=gain*field(xx,yy,theta); variance=noise_variance(clean,snr)
    full=efficient_full_fisher(xx,yy,theta,gain,variance)
    clean_states=states(xx,yy,clean)
    samples={k:[] for k in clean_states}; failures={k:0 for k in clean_states}; extract={k:0.0 for k in clean_states}
    noises=[]
    for _ in range(TRIALS):
        n=np.sqrt(variance/2)*(rng.standard_normal(clean.shape)+1j*rng.standard_normal(clean.shape)); noises.append(n)
        try:
            t=time.perf_counter(); st=states(xx,yy,clean+n); elapsed=time.perf_counter()-t
            for k in samples: samples[k].append(st[k]); extract[k]+=elapsed
        except ValueError:
            for k in samples: failures[k]+=1
    rows=[]
    full_cov=pinv_psd(full); full_std=np.sqrt(np.diag(full_cov))
    for name,vals in samples.items():
        dim=clean_states[name].size
        if len(vals)<max(20,dim+5): raise RuntimeError(f"too few {name} samples")
        arr=np.asarray(vals); centered=arr-clean_states[name]
        cov=sym(centered.T@centered/len(centered))
        jac=feature_jacobian(xx,yy,theta,gain,name)
        ci=pinv_psd(cov); info=sym(jac.T@ci@jac)
        eig,trace_ret,det_ret=generalized_retention(info,full)
        est_start=time.perf_counter(); gainmat=pinv_psd(info)@jac.T@ci; errors=centered@gainmat.T; est_ms=1000*(time.perf_counter()-est_start)/len(arr)
        bias=errors.mean(0); rmse=np.sqrt(np.mean(errors**2,axis=0)); crb=np.sqrt(np.diag(pinv_psd(info)))
        per=np.clip(np.diag(info)/np.maximum(np.diag(full),1e-15),0,1)
        rows.append({"snr_db":snr,"target_configuration":label,"gain_amplitude":1.25,"gain_phase_rad":.73,"representation":name,"state_dimension":dim,"compression_ratio":1922/dim,
          **{f"retention_{N}":float(per[i]) for i,N in enumerate(NAMES)},"joint_trace_retention":trace_ret,"joint_determinant_retention":det_ret,
          "fisher_eigenvalues":json.dumps([float(x) for x in np.linalg.eigvalsh(info)]),"generalized_retention_eigenvalues":json.dumps([float(x) for x in eig]),
          "rank":int(np.linalg.matrix_rank(info,tol=max(np.max(np.linalg.eigvalsh(info))*1e-9,1e-12))),"condition_number":float(np.linalg.cond(info)),
          **{f"rmse_{N}":(None if per[i] < 1e-6 else float(rmse[i])) for i,N in enumerate(NAMES)},**{f"bias_{N}":(None if per[i] < 1e-6 else float(bias[i])) for i,N in enumerate(NAMES)},
          "failure_rate":failures[name]/TRIALS,"extraction_runtime_ms":1000*extract[name]/TRIALS,"estimator_runtime_ms":est_ms,"total_runtime_ms":1000*extract[name]/TRIALS+est_ms})
    # Full-field local GLS benchmark with global complex gain estimated as nuisance.
    template=field(xx,yy,theta)
    complex_cols=[gain*d for d in target_derivatives(xx,yy,theta)]+[template,1j*template]
    h=np.column_stack([realvec(c) for c in complex_cols]); full_map=np.linalg.pinv(h)[:4]
    t0=time.perf_counter(); full_errors=np.asarray([full_map@realvec(n) for n in noises]); full_ms=1000*(time.perf_counter()-t0)/TRIALS
    full_bias=full_errors.mean(0); full_rmse=np.sqrt(np.mean(full_errors**2,axis=0))
    rows.append({"snr_db":snr,"target_configuration":label,"gain_amplitude":1.25,"gain_phase_rad":.73,"representation":"full_field","state_dimension":1922,"compression_ratio":1.0,
      **{f"retention_{N}":1.0 for N in NAMES},"joint_trace_retention":1.0,"joint_determinant_retention":1.0,"fisher_eigenvalues":json.dumps([float(x) for x in np.linalg.eigvalsh(full)]),"generalized_retention_eigenvalues":json.dumps([1.0]*4),"rank":int(np.linalg.matrix_rank(full)),"condition_number":float(np.linalg.cond(full)),
      **{f"rmse_{N}":float(full_rmse[i]) for i,N in enumerate(NAMES)},**{f"bias_{N}":float(full_bias[i]) for i,N in enumerate(NAMES)},"failure_rate":0.0,"extraction_runtime_ms":0.0,"estimator_runtime_ms":full_ms,"total_runtime_ms":full_ms})
    return rows


def aggregate(rows, checks):
    reps=("S2_position","S6_jacobian","S14_descriptor","P50_patch","full_field")
    overall={}
    for rep in reps:
        rr=[r for r in rows if r["representation"]==rep]
        overall[rep]={"state_dimension":rr[0]["state_dimension"],"compression_ratio":rr[0]["compression_ratio"],
          "joint_trace_retention":float(np.mean([r["joint_trace_retention"] for r in rr])),"joint_determinant_retention":float(np.mean([r["joint_determinant_retention"] for r in rr])),
          "per_parameter_retention":{n:float(np.mean([r[f"retention_{n}"] for r in rr])) for n in NAMES},
          "worst_parameter_retention":float(min(np.mean([r[f"retention_{n}"] for r in rr]) for n in NAMES)),
          "rmse":{n:(float(np.mean([r[f"rmse_{n}"] for r in rr if r[f"rmse_{n}"] is not None])) if any(r[f"rmse_{n}"] is not None for r in rr) else None) for n in NAMES},"failure_rate":float(np.mean([r["failure_rate"] for r in rr])),
          "runtime_ms":{"extraction":float(np.mean([r["extraction_runtime_ms"] for r in rr])),"estimation":float(np.mean([r["estimator_runtime_ms"] for r in rr])),"total":float(np.mean([r["total_runtime_ms"] for r in rr]))}}
    candidates=[(k,v) for k,v in overall.items() if k!="full_field" and v["state_dimension"]<=20 and v["joint_trace_retention"]>=.9 and v["worst_parameter_retention"]>=.7]
    smallest=min(candidates,key=lambda kv:kv[1]["state_dimension"])[0] if candidates else None
    verdict="PASS" if smallest else ("CONDITIONAL PASS" if max(overall[k]["joint_trace_retention"] for k in ("S6_jacobian","S14_descriptor"))>=.75 else "FAIL")
    return {"seed":SEED,"trials_per_condition":TRIALS,"conditions":len(CONFIGS)*len(SNRS),"total_paired_trials":TRIALS*len(CONFIGS)*len(SNRS),
      "model":"translated Gaussian-envelope vortex with zero-preserving anisotropy alpha and radial phase curvature beta","parameters":list(NAMES),
      "decision_criteria":{"pass_joint":.9,"pass_worst_parameter":.7,"max_state_dimension":20,"bands":{"excellent":">=0.95","strong":"0.90-0.95","partial":"0.75-0.90","weak":"0.50-0.75","insufficient":"<0.50"}},
      "overall":overall,"smallest_passing_state":smallest,"verdict":verdict,"locality_classification":"A" if overall["P50_patch"]["joint_trace_retention"]>=.9 else ("B" if overall["P50_patch"]["joint_trace_retention"]>=.75 else "C"),
      "negative_controls":{"A":"S2 position is rank deficient for alpha and beta by construction.","B":"all compact features were tested under non-unit complex gain; claimed descriptors normalize gain."},"self_checks":checks}


def checks(xx,yy):
    theta=CONFIGS["mixed"]; a=states(xx,yy,field(xx,yy,theta)); b=states(xx,yy,1.8*np.exp(1.1j)*field(xx,yy,theta))
    inv={k:bool(np.linalg.norm(a[k]-b[k])<2e-7) for k in a}
    f=efficient_full_fisher(xx,yy,theta,1+0j,noise_variance(field(xx,yy,theta),30))
    deriv=target_derivatives(xx,yy,theta)
    out={"fisher_symmetry":bool(np.allclose(f,f.T,atol=1e-9)),"fisher_psd":bool(np.min(np.linalg.eigvalsh(f))>=-1e-8),"full_parameter_rank":bool(np.linalg.matrix_rank(f)==4),"finite_full_fisher":bool(np.all(np.isfinite(f))),"zero_controlled":bool(abs(field(np.array([[theta[0]]]),np.array([[theta[1]]]),theta)[0,0])<1e-14),"gain_invariance":inv,"deformation_derivatives_nonzero":bool(np.linalg.norm(deriv[2])>0 and np.linalg.norm(deriv[3])>0)}
    if not all(v if isinstance(v,bool) else all(v.values()) for v in out.values()): raise AssertionError(out)
    return out


def write(rows,summary):
    keys=list(rows[0]);
    with CSV_PATH.open("w",newline="",encoding="utf-8") as h:
        w=csv.DictWriter(h,fieldnames=keys); w.writeheader(); w.writerows(rows)
    JSON_PATH.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")


def figures(summary,rows):
    FIGURES.mkdir(exist_ok=True); reps=["S2_position","S6_jacobian","S14_descriptor","P50_patch","full_field"]; labels=["S2","S6","S14","P50","Full"]
    dims=[summary["overall"][r]["state_dimension"] for r in reps]; vals=[summary["overall"][r]["joint_trace_retention"] for r in reps]
    fig,ax=plt.subplots(figsize=(7.5,4.8),constrained_layout=True); ax.semilogx(dims,vals,"o-"); ax.axhline(.9,color="k",ls="--",label="PASS target");
    for x,y,l in zip(dims,vals,labels): ax.annotate(l,(x,y),xytext=(4,5),textcoords="offset points")
    ax.set(xlabel="real-valued state dimension",ylabel="mean generalized Fisher retention",title="Task information versus state dimension",ylim=(0,1.05)); ax.grid(alpha=.3); ax.legend(); fig.savefig(FIGURES/"simulation_gate_2_information_vs_dimension.png",dpi=180); plt.close(fig)
    mat=np.array([[summary["overall"][r]["per_parameter_retention"][n] for n in NAMES] for r in reps[:-1]])
    fig,ax=plt.subplots(figsize=(8,4.8),constrained_layout=True); im=ax.imshow(mat,vmin=0,vmax=1,cmap="viridis"); ax.set_xticks(range(4),NAMES); ax.set_yticks(range(4),labels[:-1]); ax.set(title="Mode-by-mode information retention"); fig.colorbar(im,ax=ax); fig.savefig(FIGURES/"simulation_gate_2_mode_retention.png",dpi=180); plt.close(fig)
    fig,axs=plt.subplots(2,2,figsize=(9,7),constrained_layout=True)
    for ax,n in zip(axs.ravel(),NAMES):
        for r,l in zip(reps[:-1],labels[:-1]):
            ys=[]
            for s in SNRS:
                values=[x[f"rmse_{n}"] for x in rows if x["representation"]==r and x["snr_db"]==s and x[f"rmse_{n}"] is not None]
                ys.append(float(np.mean(values)) if values else np.nan)
            ax.semilogy(SNRS,ys,"o-",label=l)
        ax.set(title=n,xlabel="SNR (dB)",ylabel="RMSE"); ax.grid(alpha=.3)
    axs[0,0].legend(); fig.savefig(FIGURES/"simulation_gate_2_rmse.png",dpi=180); plt.close(fig)
    loc=[summary["overall"][r]["joint_trace_retention"] for r in ("S14_descriptor","P50_patch","full_field")]
    fig,ax=plt.subplots(figsize=(7,4.5),constrained_layout=True); ax.bar(["S14 descriptor","5x5 patch","full field"],loc); ax.axhline(.9,color="k",ls="--"); ax.set(title="Locality of multi-mode information",ylabel="mean generalized Fisher retention",ylim=(0,1.05)); fig.savefig(FIGURES/"simulation_gate_2_locality.png",dpi=180); plt.close(fig)


def digest(summary):
    stable=json.loads(json.dumps(summary));
    for v in stable["overall"].values(): v.pop("runtime_ms",None)
    return hashlib.sha256(json.dumps(stable,sort_keys=True).encode()).hexdigest()


def main():
    p=argparse.ArgumentParser(); p.add_argument("--self-check-only",action="store_true"); a=p.parse_args(); xx,yy=grid(); ck=checks(xx,yy)
    if a.self_check_only: print(json.dumps(ck,indent=2)); return
    rng=np.random.default_rng(SEED); rows=[]
    for label,theta in CONFIGS.items():
        for snr in SNRS: rows.extend(run_condition(rng,xx,yy,label,theta,snr))
    summary=aggregate(rows,ck); write(rows,summary); figures(summary,rows); summary["deterministic_digest_excluding_timing"]=digest(summary); JSON_PATH.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8"); print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
