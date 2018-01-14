# codesnippets

Miscellaneous code snippets

## MVC usage example
+ Implement Model.get() factory method
+ Implement View.Draw() method
  + it will typically use Model.get(element_name) to build histogram, graph, etc.
+ launch
```bash
out=`date +%Y-%m-%d-%H%M`
python tools/performace_comparison.py -b -v -j conf.json  -o outputfile --dir=$out -e pdf
```
