## To be completed

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
