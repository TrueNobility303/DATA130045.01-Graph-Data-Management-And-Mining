# -- coding:utf-8 --

import sys
import os
import glob
from subprocess import Popen, PIPE
from typing import Set

from numpy import inf
import copy
from gspan.graph import Graph, Vertex
from queue import Queue 

def generate_args(binary, *params):
    arguments = [binary]
    arguments.extend(list(params))
    return arguments

def execute_binary(args):
    process = Popen(' '.join(args), shell=True, stdout=PIPE, stderr=PIPE)
    (std_output, std_error) = process.communicate()
    process.wait()
    rc = process.returncode

    return rc, std_output, std_error

def get_subgraph_macth(data_graph_path, query_graph_path,binary_path = None):
    if binary_path == None:
        binary_path = 'DPiso.exe'
    execution_args = generate_args(binary_path, '-d', data_graph_path, '-q', query_graph_path, '-filter', 'DPiso',
                                       '-order', 'DPiso', '-engine', 'DPiso')
    
    (rc, std_output, std_error) = execute_binary(execution_args)

    query_graph_name = os.path.splitext(os.path.basename(query_graph_path))[0]

    if rc == 0:
        embedding_num = 0
        std_output = std_output.decode(encoding='utf-8',errors='strict')
        std_output_list = std_output.split('\n')
        
        for line in std_output_list:
            if '#Embeddings' in line: 
                embedding_num = int(line.split(':')[1].strip())
                break

        #得到embedding的数量
        #print(embedding_num)

        std_output = std_error.decode(encoding='utf-8',errors='strict')
        std_output_list = std_output.split('\n')
        
        PHI = []
        for line in std_output_list:

            #得到的结果形如 1 - 2 0 - 4 2 - 5 是一个Q-G的结果对
            
            phi = line.split(' ')[:-1:]
            if len(phi) == 0:
                continue
            PHI.append(phi)
        
        size_of_pattern = len(PHI[0])
        minn_support = embedding_num

        for i in range(size_of_pattern):
            vertex_set = set()
            for j in range(embedding_num):
                match = PHI[j][i].split('-')
                u,v = match[0], match[1]
                vertex_set.add(v) 
            size_of_set = len(vertex_set)           
            if size_of_set < minn_support:
                minn_support = size_of_set
        
        #计算MNI指数并返回
        return minn_support

    else:
        #print(std_error)
        #print('Error in matching!')
        #exit(-1)
        return inf
        
def graph2matchfile(tgraph,output_file_str):
    output_file = open(output_file_str,'w')
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

def generate_candidates(G:Graph,Q:Graph):
    Candidate = dict()

    #将度与标签满足约束的结点都加入候选集当中
    for u in Q.vertices.values():
        set_of_candidate = set()
        for v in G.vertices.values():
            if u.vlb == v.vlb and v.get_degree() > u.get_degree():
                set_of_candidate.add(v)
        Candidate[u] = set_of_candidate
    return Candidate

def filter_candidate(G:Graph,Q:Graph, Candidate,support):

    propagation_queue = Queue()
    for u in  Q.vertices.values():
        propagation_queue.put(u)
    
    #子程序，判断u的候选v是否满足条件
    def check_candidate(u:Vertex, v:Vertex):
        for nb in Q.get_neibors(u):

            exist_valid_candiate = False
            for cd in Candidate[nb]:
                if v.is_adjacent(cd):
                    exist_valid_candiate = True 
            
            if exist_valid_candiate is False:
                return False
        
        return True 

    while not propagation_queue.empty():
        u = propagation_queue.get()
        need_propagation = False
        
        rm_list = []

        #添加关于支持度的剪枝
        if len(Candidate[u]) < support:
            for v in Candidate[u]:
                rm_list.append(v)
                need_propagation = True
        else:
            for v in Candidate[u]:
                if check_candidate(u,v) == False:
                    rm_list.append(v)
                    need_propagation = True

        for v in rm_list:
            Candidate[u].remove(v) 

        #将邻居结点放入标签传播列表中
        if need_propagation is True:
            for nb in Q.get_neibors(u):
                propagation_queue.put(nb)
    return Candidate 

def enumerate_subgraph(G:Graph,Q:Graph,Candidate):

    #没有使用DPiso的order，根据Q的顺序的版本
    PHI = []
    order = list(Q.vertices.values())
    
    phi = dict()
    def dfs(u,depth):
        #尝试匹配候选
        for v in Candidate[u]:
            is_ok = True
            for x in phi:
                #如果该结点已经被使用过
                if phi[x] == v:
                    is_ok = False
                    break
                elif u.is_adjacent(x) and not v.is_adjacent(phi[x]):
                    is_ok = False
                    break
            if is_ok == False:
                continue
            
            phi[u] = v
            if depth == len(order)-1:
                PHI.append(copy.copy(phi))
            else:
                dfs(order[depth+1],depth+1)

        if u in phi:
            del phi[u]
        return 
    
    dfs(order[0],0)
    
    embedding_num = len(PHI)
    minn_support = embedding_num
    for u in order:
        vertex_set = set()
        for j in range(embedding_num):
            v = PHI[j][u]
            vertex_set.add(v.vid) 
        
        size_of_set = len(vertex_set)           
        if size_of_set < minn_support:
            minn_support = size_of_set
    return minn_support
    
if __name__ == "__main__":
    #data_path = 'dataset\mining\G'
    #query_path = 'dataset\mining\Q'

    #data_path = '.\dataset\dblp\data_graph\dblp.graph'
    #query_path = '.\dataset\dblp\query_graph\query_dense_4_1.graph'

    data_path = '.\dataset\mining\G'
    query_path = '.\dataset\mining\Q'

    get_subgraph_macth(data_path,query_path)