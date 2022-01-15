
#输入gspan格式的图，将其转化为subgraph_match格式的图
from gspan.graph import Graph,AUTO_EDGE_ID

def transform(input_str, output_str):

    input_file = open(input_str, 'r') 
    output_file = open(output_str,'w')

    tgraph = Graph(0,is_undirected=True, eid_auto_increment=True)

    #文件读入部分
    lines = [line.strip() for line in input_file.readlines()]
    for i, line in enumerate(lines):
        cols = line.split(' ')
        if cols[0] == 't':
           continue
        elif cols[0] == 'v':
            tgraph.add_vertex(int(cols[1]), int(cols[2]))
        elif cols[0] == 'e':
            #print(cols)

            #为了保持统一性，统计忽略边权，将其设置为0
            tgraph.add_edge(AUTO_EDGE_ID, int(cols[1]), int(cols[2]), 0)
    
    #文件输出部分

    num_of_edges = tgraph.get_num_edges()
    num_of_vertex = tgraph.get_num_vertices()
    header = "t" + " " + str(num_of_vertex) + " " + str(num_of_edges) + '\n'
    #print(header)
    output_file.write(header)
    for vid,vertex in tgraph.vertices.items():
        line = 'v' + ' ' + str(vertex.vid) + ' ' + str(vertex.vlb) + ' ' + str(vertex.get_degree()) + '\n'
        #print(line)
        output_file.write(line)
    
    for v in tgraph.vertices.values():
        #print(v.vid)
        for to, e in v.edges.items():
            vid1, vid2 = v.vid, tgraph.vertices[to].vid
            if vid1 < vid2:
                line = 'e' + ' ' + str(vid1) + ' ' + str(vid2) + ' '  + '\n'
                output_file.write(line)

if __name__ == "__main__":
    input_str = 'dataset\mining\gspan_res'
    output_str = 'dataset\mining\G'
    transform(input_str,output_str) 

    
