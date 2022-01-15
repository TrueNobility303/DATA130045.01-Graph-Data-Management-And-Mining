from gspan import config as gspan_config
from gspan import main as gspan_main

#args_str = '-s 2 w True graphdata/graph.data.1'

args_str = '-s 400 dataset\yeast\data_graph\yeast.graph'

#naive & filter & k-prunning
#25.09 & 18.45 & 13.95 

flags, _ = gspan_config.parser.parse_known_args(args=args_str.split())
gspan_main.main(flags)

## support  = 8000

""" 
t # 2
v 0 2
v 1 2
v 2 2
e 0 1 5
e 1 2 5

where: [2, 3, 4, 9, 10, 11, 12, 14, 15, 21, 23, 24, 27, 29, 30, 36, 39, 40, 41, 43, 47, 48, 49, 50, 53, 54, 55, 57, 59, 60, 61, 64, 65, 66, 67, 68, 69...]
"""

