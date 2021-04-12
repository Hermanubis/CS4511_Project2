import numpy as np
import copy

#remove inconsistent values
def revise(colorDomain, x, y):
    removed = 0
    for i in colorDomain[x]:
        able = False
        for j in colorDomain[y]:
            if (i != j): #a different color is still in the domain
                able = True
                break
        if (able == False): # if no value in y's domain can satisfy the constraint
            colorDomain[x].remove(i) #remove from domain
            removed += 1
    if(removed > 0):
        return True
    return False
        

def ac3(colorDomain):
    queue = arc #add arcs to a queue
    while queue: #while queue is not empty
        (x, y) = queue.pop()         
        updated = revise(colorDomain, x, y)
        if(updated == True): #if the domain is changed
            if(len(colorDomain[x]) == 0 or len(colorDomain[y]) == 0):
                return False
            for node in neighbor[x]:
                queue.append([node, x]) #add neighboring arcs back to the queue
    return True
        
def backtracking(colors, index, graph, heuristicNew, colorDomain):
    if index == numvertice:
    # if we have searched through all vertices in the graph
        return True
   
    # using heuristics, we prioritize most constrained variables (vertices with the most neighbors)
    indexValue = heuristicNew[index]
    
    check = 0
    for i in range(1, numcolor + 1):
        backup = copy.deepcopy(colorDomain)
        if ac3(colorDomain) == True:
            check = 1          
            for j in neighbor[indexValue]: # check all neighbors of this vertex
                if graph[indexValue][j] == 1 and colors[j] == i: 
                    # constraint check. if a neighbor is already assigned color i, backtrack and try another color
                    check = 0 
                    break       
            if check == 1: # check=1 if none of the neighbors have color i
                colors[indexValue] = i # set the color to i if there's no conflict
                #recursively call backtracking search with the next element
                if backtracking(colors, index + 1, graph, heuristicNew, colorDomain) == True: 
                    return True
                colors[indexValue] = 0 # else unassign the color and backtrack           
        colorDomain = backup
    return None
    
 
def csp(numcolor, graph):
    colors = np.zeros([numvertice], dtype = int)
    colorDomain = [[color for color in range(numcolor)] for vertex in range(numvertice)]
    heuristicNew = np.argsort(heuristic)[::-1] #sort heuristic by index in descending order
    startIndex = 0
    # if backtracking algorithm found a solution
    if backtracking(colors, startIndex, graph, heuristicNew, colorDomain) == True:
        colorList = []
        for i in range(len(colors)):
            colorList.append(colors[i])
        return colorList
    else:
        return None
 
# Main
if __name__ == "__main__":
    
    myfile = open("gc_78317100510400.txt")
    txtLines = myfile.readlines()
    # remove commented lines
    txtLines[:] = [x for x in txtLines if not x.startswith('#')]
    
    edges = []
    numcolor = 0
    numvertice = 0
    heuristic = []
    vertices = set()
    
    arc = set()
    for lines in txtLines:
        
        # format lines from txt
        lines = lines.rstrip()
        lines = lines.strip("\n")
        lines = lines.split(",")
        
        if len(lines) == 1 and "colors" in lines[0]: # get number of colors from the correct line
            lines1 = lines[0].split(" ")
            numcolor = int(lines1[2])
             
        elif len(lines) == 2:
            # in the format of From, To
            for i in range(len(lines)):
                lines[i] = int(lines[i])
                vertices.add(lines[i])
            edges.append(lines)
            
    numvertice = len({x for y in edges for x in y})
    vertices = sorted(vertices)
    neighbor = [[0]] * numvertice
    for path in edges:
        neighbor[vertices.index(path[0])].append(vertices.index(path[1]))
        neighbor[vertices.index(path[1])].append(vertices.index(path[0]))
        arc.add(tuple([path[1], path[0]]))
        arc.add(tuple([path[0], path[1]]))
    # remove duplicate using set and count number of vertices

    mygraph = np.zeros([numvertice, numvertice], dtype = int)
    # construct the adjacency matrix
    temp = min(edges)
    if temp[0] == 0 or temp[1] == 0: # if the vertices start from 0
        for i in range(len(edges)):
            mygraph[edges[i][0]][edges[i][1]] = 1
            mygraph[edges[i][1]][edges[i][0]] = 1
    else:
        for i in range(len(edges)): # if the vertices start from 1
            mygraph[edges[i][0]-1][edges[i][1]-1] = 1
            mygraph[edges[i][1]-1][edges[i][0]-1] = 1
    # print(mygraph)
    
    for i in range(len(mygraph)): # heuristic = number of neighbors
        heuristic.append(int(np.count_nonzero(mygraph[i])))
  
    colorAssignment = csp(numcolor, mygraph)
    if colorAssignment != None:
        print("Vertices Color Assignment: ")
        print(colorAssignment)
    else:
        print("No solution found")
 
