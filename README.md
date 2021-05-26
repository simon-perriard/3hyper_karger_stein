Little project to solve the min-cut problem in 3-uniform [hypergraphs](https://en.wikipedia.org/wiki/Hypergraph) in the context of the [Advanced Algorithms](https://edu.epfl.ch/coursebook/en/advanced-algorithms-CS-450) course taught at EPFL.

It is implemented by extending the famous [Karger Stein algorithm](https://en.wikipedia.org/wiki/Karger%27s_algorithm "Wiki to Karger Stein algorithm").

SHOW_CUTS global variable must be set to True if you want the program to display all the minimum cuts. If set to False, it will only show the number of min cuts in the graph.

For faster results, run with [PyPy](https://www.pypy.org/) instead of usual CPython.
