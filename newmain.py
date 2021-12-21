import csv

global graph_init
global graph_init_colors
global graph_colors
global num
global permutation
global back_permutation

def read(path):
    global graph_init, graph_init_colors, num, permutation, back_permutation
    permutation = {}
    back_permutation = {}
    count = 0
    with open(path, 'r') as file:
        f = csv.reader(file)
        for i, line in enumerate(f):
            if i == 0:
                continue
            if not line[0] in permutation:
                permutation[line[0]] = count
                count += 1
            if not line[1] in permutation:
                permutation[line[1]] = count
                count += 1
    for k, v in permutation.items():
        back_permutation[v] = k
    transf = {'red' : 1, 'green' : 2, 'blue' : 3}
    num = len(permutation)
    colors = []
    edges = []
    with open(path, 'r') as file:
        f = csv.reader(file)
        for i, line in enumerate(f):
            if i == 0:
                continue
            edges.append([permutation[line[0]], permutation[line[1]]])
            colors.append((permutation[line[0]], int(transf[line[2]])))
            colors.append((permutation[line[1]], int(transf[line[3]])))
    graph_init = [[] for i in range(num)]
    graph_init_colors = [[] for i in range(num)]
    for i in edges:
        graph_init[i[0]].append(i[1])
        graph_init[i[1]].append(i[0])
    for i in colors:
        if not len(graph_init_colors[i[0]]):
            for j in range(1, 4):
                if j != i[1]:
                    graph_init_colors[i[0]].append(j)

global graph
global grey
global sequence
global stack
global black

def dfs1():
    global grey, sequence, stack, graph
    if len(stack) == 0:
        return
    ver = stack[-1]
    if black[ver]:
        sequence.append(ver)
        stack.pop()
        return
    grey[ver] = 1
    if grey[ver]:
        black[ver] = 1
    for next in graph[ver]:
        if not grey[next]:
            grey[next] = 1
            stack.append(next)

global Tgraph
global comp
global color

def dfs2():
    global grey, stack, Tgraph, color
    if len(stack) == 0:
        return
    ver = stack[-1]
    comp[ver] = color
    grey[ver] = 1
    stack.pop()
    for next in Tgraph[ver]:
        if not grey[next]:
            grey[next] = 1
            stack.append(next)
    
global res_col

def dfs3():
    if len(stack) == 0:
        return
    ver = stack[-1]
    if black[ver]:
        stack.pop()
        ver1 = ver
        if ver >= num:
            ver -= num
        if not res_col[ver]:
            res_col[ver] = graph_colors[ver1]
        return
    grey[ver] = 1
    if grey[ver]:
        black[ver] = 1
    for next in graph[ver]:
        if not grey[next]:
            grey[next] = 1
            stack.append(next)

def main(path):
    read(path)
    global graph_init, graph_init_colors, num, graph, graph_colors
    graph = [[] for i in range(num * 2)]
    graph_colors = [0 for i in range(num * 2)]
    for i, _ in enumerate(graph_init):
        graph_colors[i] = graph_init_colors[i][0]
        graph_colors[i + num] = graph_init_colors[i][1]
    for i, edges in enumerate(graph_init):
        for j in edges:
            if graph_init_colors[i][0] == graph_init_colors[j][0]:
                graph[i].append(num + j)
            if graph_init_colors[i][0] == graph_init_colors[j][1]:
                graph[i].append(j)
            if graph_init_colors[i][1] == graph_init_colors[j][0]:
                graph[i + num].append(j + num)
            if graph_init_colors[i][1] == graph_init_colors[j][1]:
                graph[i + num].append(j)
    global stack, grey, sequence, black
    stack = []
    grey = [0 for i in range(2 * num)]
    black = [0 for i in range(2 * num)]
    sequence = []
    for i in range(2 * num):
        if not grey[i]:
            stack.append(i)
            while len(stack):
                dfs1()
    global Tgraph, comp, color
    comp = [0 for i in range(2 * num)]
    grey = [0 for i in range(2 * num)]
    Tgraph = [[] for i in range(2 * num)]
    color = 0
    for i, edges in enumerate(graph):
        for j in edges:
            Tgraph[j].append(i)
    while len(sequence):
        ver = sequence[-1]
        sequence.pop()
        if not grey[ver]:
            stack.append(ver)
            while len(stack):
                dfs2()
            color += 1
    for i in range(num):
        if comp[i] == comp[num + i]:
            print("it is impossible")
            return 
    global res_col
    res_col = [0 for i in range(num)]
    grey = [0 for i in range(2 * num)]
    black = [0 for i in range(2 * num)]
    for i in range(2 * num):
        if not grey[i]:
            stack.append(i)
            while len(stack):
                dfs3()
    transf = {1 : 'red', 2 : 'green', 3 : 'blue'}
    dct_res = {}
    for i, v in enumerate(res_col):
        dct_res[back_permutation[i]] = transf[v]
    return dct_res
    
print(main('graph.csv'))
