import tkinter as tk
from tkinter import  ttk
from tkinter import *
from tkinter.font import BOLD
from matplotlib.pyplot import margins
import pandas as pd
# read data from a csv file
data = pd.read_csv("graph_data.csv")
data=pd.DataFrame(data)
# cities of Romania graph
cities = list(data['Cities'])
costMat=[]

# convert the data into list and id to each city 
for j in range(len(cities)):
    city_data = []
    for  i in cities:
        city_data.append(data[i][j])
    costMat.append(city_data)

# SLD for Romania graph 
# Heuristic Information
sld = {0:366, 1:0, 2:160, 3:242, 4:161, 5:176, 6:77, 7:151, 8:226, 9:244, 10:241, 11:234, 12 : 380, 13:100, 14:193, 15:253, 16:329, 17:80, 18:199, 19:374}

# Node class representing a city in romania 
# The depth at which it is present, cost from the start node, it's id and it's parent if any
class Node:
    def __init__(self,node, depth, parent,cost):
        self.state = node
        self.depth= depth
        self.parent=parent
        self.cost=cost
    
    def getState(self):
        return self.state
    def getParent(self):
        return self.parent
    def getCost(self):
        return self.cost
    def getDepth(self):
        return self.depth

# Result Board
class resultBoard:
    def __init__(self, algo, depth, pathCost, nodes_generated):
        self.algo = algo
        self.depth= depth
        self.pathCost=pathCost
        self.nodes_generated=nodes_generated
        
    def getAlgo(self):
        print(self.algo)
        return self.algo
    def getPathCost(self):
        return self.pathCost
    def getNodesCount(self):
        return self.nodes_generated
    def getDepth(self):
        return self.depth

start = 'Arad'  #start node
end = 'Bucharest' #goal node

# graph search of BFS
def bfs_graph():
    frontier=[]
    explored = []
    rootnode = cities.index(start)
     # add the start node to the frontier and start the search
    frontier.append(Node(rootnode,0,-1,0))
    nodes=1
    res=0
    while(True):
        # the end node is not reachable from the start node
        if(len(frontier)==0):
            print('Failed! No path exists between {} to {}'.format(start,end))
            break
        # remove the front node from the frontier
        curr = frontier.pop(0)
        explored.append(curr.getState())

        # make a copy of frontier to store only states and use those states to check the frntier state while exploring the node childs
        frontier_copy=[]
        for node in frontier:
            frontier_copy.append(node.getState())
        # expand the current node and add the node to th frontier  if nor already explored or expanded
        for i in range(len(costMat[0])):
             # if path exist and the expanded node is not already explored and expanded then add the node to the frontier
            if(costMat[curr.getState()][i]!=0 and (i not in frontier_copy) and (i not in explored)):
                frontier.append(Node(i,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][i]))
                nodes+=1
                 # if the curr node is the goal node then break the loop (stop the search)
                if(cities[i]==end):
                    res=1
                    endNode = Node(i,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][i])
                    break
        if(res==1):
            break
    print('-----------------------------')
    print('Graph Version of Breadth First Search')        
    print('-----------------------------') 
    print("The path followed")
    ind = endNode
    # print path from start to end node
    path=[]
    while(True):
        path.append(cities[ind.getState()])
        if(ind.getState()==cities.index(start)):
            break
        ind = ind.getParent()
    # print the result board to the console
    print('Path : ',*path[::-1],sep=" -> ")
    result = resultBoard("Graph Version of Breadth First Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path, result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.getCost())
    print('Depth at which {} node is present : {}'.format(end, endNode.getDepth()))
    print("No. of nodes generated : ",nodes)
    print()


# Graph version  for depth limited search
def DLS_graph(limit=3, idls=False):   
    gFrontier=[] #node stack
    # add the start node to the frontier stack and start the search
    rootnode = cities.index(start)
    rootnode = Node(rootnode,0,-1,0)
    gFrontier.append(rootnode)
    gExplored=[]
    nodes=1
    endNode=-1
    # continue the search till there is no node in the frontier or till the goal node is expanded
    while(len(gFrontier)>0):
        curr = gFrontier.pop(0)
        gExplored.append(curr.getState())
        # if the curr node is the goal node then break the loop (stop the search)
        if(curr.getState()==cities.index(end)):
            print("Success")
            endNode = curr
            gExplored.append(curr.getState())
            break
        # if the current depth is less than the limit then expand the node
        if(curr.getDepth()<limit):
            for act in range(len(cities)-1,-1,-1):
                # if path exist and the expanded node is not already explored add the node to the frontier
                if(costMat[act][curr.getState()]>0 and act not in gExplored):
                    gen_node = Node(act,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][act])
                    gFrontier.insert(0,gen_node)
                    nodes+=1
                    
    print('-----------------------------')
    print('Graph Version of Depth Limited Search Search!')        
    print('-----------------------------') 
     # the end node is not reachable from the start node
    if(len(gFrontier)==0 and curr.getState()!=cities.index(end)):
        print("Solution does not exist")
        return -1
    else:
        print("The path followed")
        ind = endNode
        path=[]
        # traverse the path and add the costs
        while(True):
            path.append(cities[ind.getState()])
            if(ind.getState()==cities.index(start)):
                break
            ind = ind.getParent()
    # print the result board to the console and display in the window
    print('Path : ',*path[::-1],sep=" -> ")
    if(idls):
        result = resultBoard("Graph Version of Iterative Deepening Search",endNode.getDepth(),endNode.getCost(),nodes)
    else:
        result = resultBoard("Graph Version of Depth Limited Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path, result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.cost)
    print('Depth at which {} node is present : {}'.format(end,endNode.depth ))
    print("No. of nodes generated : ",nodes)
    print()
    return 1


# Iterative deepening depth limited search
def IDLS_graph(): 
    # depth limited to 3
    depth=20
    print('-----------------------------')
    print('Graph Version of Iterative Deepening Depth Limited Search!')        
    print('-----------------------------')      
    # find the depth at which the goal node is present
    for currLimit in range(depth):
        res =DLS_graph(currLimit, idls=True)
        if(res!=-1):
            # print("The limit at which solution exists is ",currLimit)
            break

# graph search for A* graph
def astar_graph():
    frontier=[]
    explored=[]
    # add the start node to the frontier and start the search
    rootnode = Node(cities.index(start),0,-1,0)
    frontier.append(rootnode)
    nodes=1
    while(True):
         # the end node is not reachable from the start node
        if(len(frontier)==0):
            print('Failed! No path exists between {} to {}'.format(start,end))
            return 0
        # remove the front node from the frontier based on evaluation function [minimum f(x)]
        mi=10000000000
        for i in range(len(frontier)):
            fi = frontier[i].getCost()
            hi = sld[frontier[i].getState()]
            g = fi+hi
            if(g<mi):
                mi=g
                curr=frontier[i]
         # if the curr node is the goal node then break the loop (stop the search)
        if(cities[curr.getState()]==end):
            explored.append(i)
            endNode=curr
            break
        # remove node with minimum f(x) = h(x)+g(x)
        frontier.remove(curr)
        explored.append(curr.getState())

        # make a copy of frontier to store only states
        frontier_copy=[]
        for node in frontier:
            frontier_copy.append(node.getState())

        # search child nodes of selected node
        for i in range(len(costMat[0])):
            if(costMat[curr.getState()][i]!=0  and (i not in explored)):
                # Add the cost 
                frontier.append(Node(i,curr.getDepth()+1, curr,curr.getCost()+costMat[curr.getState()][i])) 
                nodes+=1
    print('-----------------------------')
    print('Graph Version of A* Search!')        
    print('-----------------------------')   
    print("The path followed")
    ind = endNode
    print(endNode.getState())
    path=[]
    while(True):
        path.append(cities[ind.getState()])
        if(ind.getState()==cities.index(start)):
            break
        ind = ind.getParent()
    # print the result board to the console and display in the window
    print('Path : ',*path[::-1],sep=" -> ")
    result = resultBoard("Graph Version of A* Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path, result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.getCost())
    print('Depth at which {} node is present : {}'.format(end,endNode.getDepth() ))
    print("No. of nodes generated : ",nodes)

# DFS for Graph search
def DFS_graph():   
    gFrontier=[] #node stack
    path=[]
    # add the start node to the frontier and start the search
    rootnode = cities.index(start)
    rootnode = Node(rootnode, 0,-1,0)
    gFrontier.append(rootnode)
    gExplored=[]
    nodes=0
    # continue till the node is present in the frontier and the goal node is not reached
    while(len(gFrontier)>0):
        curr = gFrontier.pop(0)
        gExplored.append(curr.getState())
         # if the curr node is the goal node then break the loop (stop the search)
        if(curr.getState()==cities.index(end)):
            print("Success")
            endNode = curr
            break
        # expand the node
        for act in range(len(cities)-1,-1,-1):
            # path exist between curr node and the act node 
            if(costMat[act][curr.getState()]>0 and act not in gExplored):
                node = Node(act,curr.getDepth()+1 , curr, curr.getCost()+costMat[curr.getState()][act])
                gFrontier.insert(0,node)
                nodes+=1
    print('-----------------------------')
    print('Graph Version of Depth First Search!')        
    print('-----------------------------')      
    print("The path followed")
    ind = endNode
    path=[]
    # traverse the path and add the costs
    while(True):
        path.append(cities[ind.getState()])
        if(ind.getState()==cities.index(start)):
            break
        ind = ind.getParent()



    print('Path : ',*path[::-1],sep=" -> ")
    result = resultBoard("Graph Version of Depth First Search",endNode.getDepth(),endNode.getCost(),nodes)

    input_frame = create_graph_view_frame(root, path, result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ',endNode.getCost())
    print('Depth at which {} node is present : {}'.format(end, endNode.getDepth()))
    print("No. of nodes generated : ",len(gFrontier)+len(gExplored))
    print()


# Tree search for bfs
def bfs_tree():
    tree_frontier=[]
    rootnode = cities.index(start)
    tree_frontier.append(Node(rootnode,0,-1,0))
    res=0
    nodes=1

    while(True):
         # the end node is not reachable from the start node
        if(len(tree_frontier)==0):
            print('Failed! No path exists between {} to {}'.format(start,end))
            break
        # remove the front node from the frontier
        curr = tree_frontier.pop(0)
        # make a copy of frontier to store only states and use those states to check the frntier state while exploring the node childs
        frontier_copy=[]
        for node in tree_frontier:
            frontier_copy.append(node.getState())

        for i in range(len(costMat[0])):
             # if path exist and the expanded node is not already explored add the node to the frontier
            if(costMat[curr.getState()][i]!=0 and (i not in frontier_copy)):   
                # append the successive nodes to frontier
                tree_frontier.append(Node(i, curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][i]))
                nodes+=1
                # print(cities[curr], cities[i])
                if(cities[i]==end):
                    res=1
                    endNode = Node(i,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][i])
                    break
        if(res==1):
            break
    print('-----------------------------')
    print('Tree Version of Breadth First Search!')        
    print('-----------------------------')   
    print("The path followed")
    ind = endNode
    path=[]
    while(True):
        path.append(cities[ind.getState()])
        if(ind.getState()==cities.index(start)):
            break
        ind = ind.getParent()

    print('Path : ',*path[::-1],sep=" -> ")
    result = resultBoard("Tree Version of Breadth First Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path, result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.getCost())
    print('Depth at which {} node is present : {}'.format(end, endNode.getDepth()))
    print("No. of nodes generated : ",nodes)
    print()


def DFS_tree():   
    gFrontier=[] #node stack
    rootnode = cities.index(start)
    rootnode = Node(rootnode,0,-1,0)
    gFrontier.append(rootnode)
    nodes=0
     # exit when the end node is not reachable from the start node
    while(len(gFrontier)>0):
        curr = gFrontier.pop(0)
        # if the curr node is the goal node then break the loop (stop the search)
        if(curr.getState()==cities.index(end)):
            print("Success")
            endNode=curr
            break
        # expand the node
        for act in range(len(cities)-1,-1,-1):
            if(costMat[act][curr.getState()]>0):
                node = Node(act, curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][act])
                gFrontier.insert(0,node)
                nodes+=1
        if(nodes>100):
            result=-1
            break
    print('-----------------------------')
    print('Tree Version of  Depth First Search!')        
    print('-----------------------------')   
    if(result==-1):
        print("Infinite nodes are generated! Solution doesn't exist.")
        input_frame = create_graph_view_frame(root, [],"Infinite nodes are generated! Solution doesn't exist." )
        input_frame.grid(column=0, row=0)    
    else:
        print("The path followed")
        ind =endNode
        path=[]
        cost=0
        # trverse the path and add the costs
        while(True):
            path.append(cities[ind.getState()])
            if(ind.getState()==cities.index(start)):
                break
            ind = ind.getParent()
        #  Display the result board
        print('Path : ',*path[::-1],sep=" -> ")
        result = resultBoard("Tree Version of Depth First Search",endNode.getDepth(),endNode.getCost(),nodes)
        input_frame = create_graph_view_frame(root, path, result)
        input_frame.grid(column=0, row=0)
        print('Pathcost : ', endNode.getCost())
        print('Depth at which {} node is present : {}'.format(end,endNode.getDepth()))
        print("No. of nodes generated : ",nodes)
        print()

# Tree search of A* algorithm
def astar_tree():
    tree_frontier=[]
    rootnode = cities.index(start)
    rootnode = Node(rootnode,0,-1,0)
    tree_frontier.append(rootnode)
    nodes=1
    while(True):
        # the end node is not reachable from the start node
        if(len(tree_frontier)==0):
            print('Failed! No path exists between {} to {}'.format(start,end))
            return 0

        # remove the node from the frontier based on evaluation function [minimum f(x)]
        mi=10000000000
        for i in range(len(tree_frontier)):
            fi = tree_frontier[i].getCost()
            hi = sld[tree_frontier[i].getState()]
            g = fi+hi
            if(g<mi):
                mi=g
                curr=(tree_frontier[i])

        # remove node with minimum f(x) = h(x)+g(x)
        tree_frontier.remove(curr)
        # if the curr node is the goal node then break the loop (stop the search)
        if(cities[curr.getState()]==end):
            endNode=curr
            break

        # make a copy of frontier to store only states
        frontier_copy=[]
        for node in tree_frontier:
            frontier_copy.append(node.getState())

        # search child nodes of selected node
        for i in range(len(costMat[0])):
            if(costMat[curr.getState()][i]!=0):
                # Add the cost 
                # append the successive nodes to frontier
                tree_frontier.append(Node(i,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][i]))
                nodes+=1
            
        if(len(tree_frontier)>20):
            break
    print('-----------------------------')
    print('Tree Version of A* Search!')        
    print('-----------------------------')  
    print("The path followed")
    ind = endNode
    path=[]
    while(True):
        path.append(cities[ind.getState()])
        if(ind.getState()==cities.index(start)):
            break
        ind = ind.getParent()
    # Display the result board
    print('Path : ',*path[::-1], sep=" -> ")
    result = resultBoard("Tree Version of A* Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path,result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.getCost())
    print('Depth at which {} node is present : {}'.format(end,endNode.getDepth() ))
    print("No. of nodes generated : ",nodes)
      
#  Tree version of Depth limited search
def DLS_tree(limit=3, idls=False): 
    tFrontier=[] #node stack
    rootnode = cities.index(start)
    rootnode = Node(rootnode,0,-1,0)
    tFrontier.append(rootnode)
    nodes=1
    endNode=-1
     #exit when the end node is not reachable from the start node
    while(len(tFrontier)>0):
        curr = tFrontier.pop(0)
        # if the curr node is the goal node then break the loop (stop the search)
        if(curr.getState()==cities.index(end)):
            print("Success")
            endNode = curr
            break
        # expand the node if its depth is less than the limit
        if(curr.getDepth()<limit):
            for act in range(len(cities)-1,-1,-1):
                if(costMat[act][curr.getState()]>0):
                    gen_node = Node(act,curr.getDepth()+1,curr,curr.getCost()+costMat[curr.getState()][act])
                    tFrontier.insert(0,gen_node)
                    nodes+=1
                    
    print('-----------------------------')
    print('Tree Version of Depth Limited Search!')        
    print('-----------------------------')         
    if(len(tFrontier)==0 and curr.getState()!=cities.index(end)):
        print("Solution does not exist")
        return -1
    else:
        print("The path followed")
        ind = endNode
        path=[]
        # traverse the path and add the costs
        while(True):
            path.append(cities[ind.getState()])
            if(ind.getState()==cities.index(start)):
                break
            ind = ind.getParent()
    #display the result board
    print('Path : ',*path[::-1],sep=" -> ")
    if(idls):
        result = resultBoard("Tree Version of Iterative Deepening Search",endNode.getDepth(),endNode.getCost(),nodes)
    else:
        result = resultBoard("Tree Version of Depth Limited Search",endNode.getDepth(),endNode.getCost(),nodes)
    input_frame = create_graph_view_frame(root, path,result)
    input_frame.grid(column=0, row=0)
    print('Pathcost : ', endNode.cost)
    print('Depth at which {} node is present : {}'.format(end,endNode.depth ))
    print("No. of nodes generated : ",nodes)
    print()
    return 1

#Tree version of iterative deepening depth first search
def IDLS_tree(): 
    depth=20  
    print('-----------------------------')
    print('Tree Version of Iterative Deepening Depth Limited Search!')        
    print('-----------------------------')   
    for currLimit in range(depth):
        res = DLS_tree(limit=currLimit, idls=True)
        if(res!=-1):
            # print("The limit at which solution exists is ",currLimit)
            break
    

#  Plot cities of Romania 
def create_graph_view_frame(container, path, results="empty"):
    frame = ttk.Frame(container)
    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)
    C = tk.Canvas(frame, bg="pink", height=500, width=600)

    Label(C, text = "ROMANIA GRAPH",  bg='#000', fg='#fff',pady=10, padx=10, font=10).place(x = 170,y = 20) 

    # create all the points representing cities of Romania
    C.create_rectangle(100,50,105,55, width = 4, fill = 'black')
    Oradea = Label(C, text = "Oradea").place(x = 40,y = 20) 
    Label(C, text = "71", bg="pink").place(x =60, y=50)            
    C.create_rectangle(80,90,85,95, width = 4, fill = 'black')
    Label(C, text = "Zerind").place(x = 30,y = 80)   
    C.create_rectangle(60,150,65,155, width = 4, fill = 'black')
    Label(C, text = "Arad").place(x = 20,y = 130) 
    Label(C, text = "75", bg="pink").place(x =80, y=110)
    Label(C, text = "140", bg="pink").place(x =110, y=170)
    C.create_rectangle(60,250,65,255, width = 4, fill = 'black')
    Label(C, text = "Timisoara").place(x = 20,y = 270) 
    Label(C, text = "118", bg="pink").place(x =30, y=200)
    C.create_rectangle(120,310,125,315, width = 4, fill = 'black')
    Label(C, text = "Lugoj").place(x = 130,y = 300)
    Label(C, text = "111", bg="pink").place(x =90, y=256)
    C.create_rectangle(125,350,130,355, width = 4, fill = 'black')
    Label(C, text = "Mehdia").place(x = 60,y = 340)
    Label(C, text = "70", bg="pink").place(x =135, y=324)
    C.create_rectangle(123,400,128,405, width = 4, fill = 'black')
    Label(C, text = "Drobeta").place(x = 60,y = 400)
    Label(C, text = "75", bg="pink").place(x =135, y=364)
    C.create_rectangle(210,410,215,415, width = 4, fill = 'black')
    Label(C, text = "Craiova").place(x = 190,y = 430)
    Label(C, text = "120", bg="pink").place(x =150, y=410)
    C.create_rectangle(330,450,335,455, width = 4, fill = 'black')
    Label(C, text = "Giurgiu").place(x = 340,y = 445)
    Label(C, text = "90", bg="pink").place(x =330, y=400)
    C.create_rectangle(530,430,535,435, width = 4, fill = 'black')
    Label(C, text = "Eforie").place(x = 520,y = 440)
    C.create_rectangle(490,340,495,345, width = 4, fill = 'black')
    Label(C, text = "Hirsova").place(x = 500,y = 330)
    Label(C, text = "86", bg="pink").place(x =520, y=370)
    C.create_rectangle(430,340,435,345, width = 4, fill = 'black')
    Label(C, text = "Urziceni").place(x = 420,y = 350)
    C.create_rectangle(370,390,375,395, width = 4, fill = 'black')
    Label(C, text = "Bucharest").place(x = 380,y = 390)
    Label(C, text = "101", bg="pink").place(x =320, y=364)
    Label(C, text = "85", bg="pink").place(x =385, y=340)
    C.create_rectangle(480,200,485,205, width = 4, fill = 'black')
    Label(C, text = "Vaslui").place(x = 490,y = 200)
    Label(C, text = "142", bg="pink").place(x =465, y=250)
    C.create_rectangle(390,70,395,75, width = 4, fill = 'black')
    Label(C, text = "Neamt").place(x = 380,y = 40)
    Label(C, text = "87", bg="pink").place(x =420, y=70)
    C.create_rectangle(450,120,455,125, width = 4, fill = 'black')
    Label(C, text = "Iasi").place(x = 460,y = 110)
    Label(C, text = "92", bg="pink").place(x =470, y=140)
    C.create_rectangle(200,180,205,185, width = 4, fill = 'black')
    Label(C, text = "Sibiu").place(x = 210,y = 150)
    Label(C, text = "80", bg="pink").place(x =225, y=210)
    Label(C, text = "99", bg="pink").place(x =250, y=170)
    C.create_rectangle(290,200,295,205, width = 4, fill = 'black')
    Label(C, text = "Fagaras").place(x = 280,y = 170)
    Label(C, text = "151", bg="pink").place(x =160, y=95)
    Label(C, text = "211", bg="pink").place(x =350, y=290)
    C.create_rectangle(230,250,235,255, width = 4, fill = 'black')
    Label(C, text = "Rimnicu Vilcea").place(x = 130,y = 240)
    C.create_rectangle(300,320,305,325, width = 4, fill = 'black')
    Label(C, text = "Pitesti").place(x = 280,y = 350)
    Label(C, text = "138", bg="pink").place(x =253, y=370)
    Label(C, text = "146", bg="pink").place(x =225, y=320)
    Label(C, text = "97", bg="pink").place(x =283, y=275)

    # Label all the edges 
    #  coordinates representing cities in the graph
    cities_coordinates = {"Oradea":(100,50), "Zerind":(80,90),"Pitesti":(300,320), "Rimnicu Vilcea":(230,250), 
                        "Fagaras":(290,200),"Sibiu":(200,180),"Iasi":(450,120),"Vaslui":(480,200),"Urziceni":(430,340),
                        "Hirsova":(490,340),"Eforie":(530, 430),"Giurgiu":(330,450),"Craiova":(210,410),"Drobeta":(123,400),
                        "Mehadia":(125,350),"Lugoj":(120,310),"Timisoara":(60,250),"Arad":(60,150),"Bucharest":(370,390),"Neamt":(390,70)}

    # connect the cities if path exists between the two
    for i in range(0,len(cities)):
        for j in range(0, len(cities)):
            if(costMat[i][j]>0):
                if(cities[i] in path and cities[j] in path):
                    C.create_line(cities_coordinates[cities[i]][0],cities_coordinates[cities[i]][1],cities_coordinates[cities[j]][0],cities_coordinates[cities[j]][1], fill = 'red')
                else:
                    C.create_line(cities_coordinates[cities[i]][0],cities_coordinates[cities[i]][1],cities_coordinates[cities[j]][0],cities_coordinates[cities[j]][1])
    
    # result board 
    result_board = tk.Canvas(frame, bg="white", height=500, width=400)
    Label(result_board, text = "Search Results",bg="#fff",fg='#000',pady=10, padx=10, font=10).place(x= 100, y=30)

    if(results=="empty"):
        # Default display for result board
        Label(result_board, text="Choose and Compare algorithms!").place(x= 100, y=200)
    elif(results!="empty" and type(results) is str):
        # for the exception cases where reslut for any algorithm is not possible
        Label(result_board, text="Tree Version of Depth First Search!", fg = "pink", font=20).place(x= 70, y=80)
        Label(result_board, text=results).place(x= 70, y=140)
    else:
        # If any of the algorithms are chose show the result board
        Label(result_board, text=results.getAlgo(), fg = "pink", font=20).place(x= 70, y=80)
        text = "Path Cost : "+str(results.getPathCost())
        Label(result_board, text=text).place(x=100,y=120)
        text= "Total Number of Nodes generated : "+str(results.getNodesCount())
        Label(result_board, text= text).place(x=100,y=160)
        text="Depth at which "+end+" is present  : "+str(results.getDepth())
        Label(result_board, text= text).place(x=100,y=200)

    result_board.pack(side="right")
    C.pack(side="left")
    return frame

# create buttons for the algorithms
def create_button_frame(container):

    frame = ttk.Frame(container)

    frame.columnconfigure(0, weight=1)
    style = ttk.Style()
    style.configure("BW.TLabel", background="#b78")

    # Display options for  Graph version of algorithms
    ttk.Button(frame, text='Breadth First Search',command=bfs_graph).grid(column=1, row=1)
    ttk.Button(frame, text='Depth First Search',command=DFS_graph).grid(column=2, row=1)
    ttk.Button(frame, text='Iterative Deepening DFS',command=IDLS_graph).grid(column=3, row=1)
    ttk.Button(frame, text='A* Search',command=astar_graph).grid(column=4, row=1)
    ttk.Button(frame, text='Depth Limited Search',command=DLS_graph).grid(column=5, row=1)
    # Display options for Tree versions of algorithms
    ttk.Button(frame, text='Breadth First Search',command=bfs_tree).grid(column=1, row=2)
    ttk.Button(frame, text='Depth First Search',command=DFS_tree).grid(column=2, row=2)
    ttk.Button(frame, text='Iterative Deepening DFS',command=IDLS_tree).grid(column=3, row=2)
    ttk.Button(frame, text='A* Search',command=astar_tree).grid(column=4, row=2)
    ttk.Button(frame, text='Depth Limited Search',command=DLS_tree).grid(column=5, row=2)

    l1 = ttk.Label(text="Graph version", style="BW.TLabel")
    l1.place(x=130,y=520)
    l2 = ttk.Label(text="Tree version", style="BW.TLabel")
    l2.place(x=130,y=560)

    for widget in frame.winfo_children():
        widget.grid(padx=20, pady=10)

    return frame

if __name__ == "__main__":
    # root window
    root = tk.Tk()
    root.title('Search Algorithms')
    root.geometry('1200x650')
    root.resizable(0, 0)
    root.attributes('-toolwindow', True)

    # layout on the root window
    root.columnconfigure(0, weight=4)
    root.columnconfigure(1, weight=1)

    # graph view
    input_frame = create_graph_view_frame(root,[])
    input_frame.grid(column=0, row=0)

    # Button Window
    button_frame = create_button_frame(root)
    button_frame.grid(column=0, row=1)

    root.mainloop()