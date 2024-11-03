Clone the repository with the sub-modules for `ply` dependencies

```bash
git clone --recurse-submodules https://github.com/bwaklog/plywood.git
```


`ply` module path 

```python
from ply.src.ply import lex
from ply.src.ply import yacc
```

---

(WIP) Constructs
1. Variable declarations
2. Arithmetic Expression: `$((expr))`

Example
```bash
x=100
while [ $x -gt 0 ]
do
    command
    x=$(($x-1))
done
```

3. if-else conditions