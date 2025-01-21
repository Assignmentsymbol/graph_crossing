## Crossing minimization challenge

### References
1. [Intersection detect Algorithm](https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/) - By Ansh Riyal.
2.[WebTool for manual testing](https://jacoblmiller.github.io/tum-gd-contest/tool.html)

### Environment set up instruction for the old program(confirmed)
Without IDE:
1. Download python (recommmend 3.9)
2. Download pip (3.9) by: 'python -m ensurepip --upgrade' or 'python -m pip install --upgrade pip'
3. Align global pip and python version:
	3.1. Windows: make sure they are in system-path and the path of python is above pip
4. Download dependencies/libraries: 'pip install -r requirements-win.txt' (or requirements-linux/osx respectively)
5. After work, run pip freeze > "requirements-***.txt" to save the updated dependency list.

### How to run the script:
1. Set up the same environment as above.
2. Replace the two special fields i.e. &lt;input directory absolute path&gt; and &lt;output directory absolute path&gt; in the
"config.txt" file to the corresponding ones.
3. Place the input files such as 'graph1.json' in the input directory, make sure no other readable file exist in this directory such as 'report'.
4. Run the script with python, the output files and a overall report file will be generated under the earlier given 
output directory path.
⚠️: Once a planar embedding is generated the script will through out an error.

With pycharm:
To be finished...

# Best Results
| Embedding        | Intersection Count | Runtime (s) |
|----------------------------|--------------------|-------------|
| ![Graph 1](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g1.png) | 1                 | <1s       |
| ![Graph 2](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g2.png) | 2                 | <1s       |
| ![Graph 3](https://github.com/Assignmentsymbol/graph_crossing/blob/669b91df9aaacf3af26dbdefcba1eae2401d952b/python/pics/g3.png) | 1                 | <1s       |
| ![Graph 4](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g4.png) | 1                 | <1s       |
| ![Graph 5](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g5.png) | 1                 | <1s      |
| ![Graph 6](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g6.png) | 2                 | <10s       |
| ![Graph 7](https://github.com/Assignmentsymbol/graph_crossing/blob/669b91df9aaacf3af26dbdefcba1eae2401d952b/python/pics/g7.png)| 2                 | <1s      |
| ![Graph 8](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g8.png) | 0 (legal embedding without adjustment)               | <5s       |
| ![Graph 9](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g9.png) | 940                | <100s|
| ![Graph 10](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g10.png) | ∞ (illegal embedding)                 | <5s       |
| ![Graph 11](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g11.png) | ∞                 | <5s       |
| ![Graph 12](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g12.png) | 299               | <1s       |
| ![Graph 13](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g13.png) | 1485              | <100s       |
| ![Graph 14](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g14.png) | 649                 | very very very long... > 5mins       |
| ![Graph 15](https://github.com/Assignmentsymbol/graph_crossing/blob/c5d711af630a4a600dc8f9deff5c8f14520fe6fd/python/pics/g15.png) | ∞                | <60s       |

