# codesnippets

Miscellaneous code snippets

## MVC usage example
+ Implement Model.get() factory method
+ Implement View.Draw() method
  + it will typically use Model.get(element_name) to build histogram, graph, etc.
+ launch
```bash
out=`date +%F-%H%M`
python tools/performace_comparison.py -b -v -j conf.json  -o outputfile --dir=$out -e pdf
#OR using python config file
python tools/performace_comparison.py -b -v -j conf_cff.py  -o outputfile --dir=$out -e pdf
```
+ tests
```bash
python -m unittest discover . -v
```

## LaTeX
```bash 
cp -a latex resources build; cd build/;pdflatex latex/slides.tex;cd -
cp -a latex resources build; cd build/;pdflatex latex/report.tex;cd -
```

## Binning usage example
```python
import ROOT as rt
import numpy as np
from autobinning import OprimizedBinning

filename = "file.root"    
cuts = "(((HLT_IsoMu24==1||HLT_IsoTkMu24==1) && met > 50 && HT > 500 && fabs(LeptonEta)<2.1 ))"
c = rt.TChain("Craneen__Mu")
c.Add(filename)
nev = c.Draw("leptonIso","nJets>=10&&nMtags>=4","goff")
pybuf = c.GetVal(0)
pybufw = c.GetW()
buf = np.array([pybuf[i] for i in range(0,nev)])
ob = OprimizedBinning( buf, pybufw )
ob._lowstat_thresh=30
ob._lowstat_algo='scott'
h = ob.get_histogram()
c.Draw("leptonIso>>sample_hist","nJets>=10&&nMtags>=4","goff")
h.SetDrawOption('hist text pE0')
```

## Scons dependency tree
**requires graphviz**

```bash
scons -Q -n -f SConstruct kbc| ./scons_dependency_tree.py | dot -Tpdf > dot_rendering.pdf
```
alternatively
```bash
scons --tree=all -Q -n -f SConstruct kbc| ./scons_dependency_tree.py | dot -Tpdf > dot_rendering.pdf
```
