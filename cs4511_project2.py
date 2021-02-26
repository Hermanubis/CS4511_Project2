import numpy as np

def backtracking(numcolor, colors, index, numvertice, graph, heuristicNew):
    if index == numvertice:
    # if we have searched through all vertices in the graph
        return True
   
    # using heuristics, we prioritize most constrained variables (vertices with the most neighbors)
    indexValue = heuristicNew[index]
    
    check = 0
    for i in range(1, numcolor + 1):
        check = 1
        for j in range(numvertice): # check all neighbors of this vertex
            if graph[indexValue][j] == 1 and colors[j] == i: 
                # constraint check. if a neighbor is already assigned color i, backtrack and try another color
                check = 0 
                break
        
        if check == 1: # check=1 if none of the neighbors have color i
            colors[indexValue] = i # set the color to i if there's no conflict
            #recursively call backtracking search with the next element
            if backtracking(numcolor, colors, index + 1, numvertice, graph, heuristicNew) == True: 
                return True
            colors[indexValue] = 0 # else unassign the color and backtrack
 
def csp(numcolor, numvertice, graph, heuristic):
    colors = np.zeros([numvertice], dtype = int)
    heuristicNew = np.argsort(heuristic)[::-1] #sort heuristic by index in descending order
    startIndex = 0
    # if backtracking algorithm found a solution
    if backtracking(numcolor, colors, startIndex, numvertice, graph, heuristicNew) == True:
        colorList = []
        for i in range(len(colors)):
            colorList.append(colors[i])
        return colorList
 
# Main
if __name__ == "__main__":
    
    myfile = open("gc_78317103208800.txt")
    txtLines = myfile.readlines()
    # remove commented lines
    txtLines[:] = [x for x in txtLines if not x.startswith('#')]
    
    edges = []
    numColor = 0
    numvertice = 0
    heuristic = []
    for lines in txtLines:
        
        # format lines from txt
        lines = lines.rstrip()
        lines = lines.strip("\n")
        lines = lines.split(",")
        
        if len(lines) == 1 and "colors" in lines[0]: # get number of colors from the correct line
            lines1 = lines[0].split(" ")
            numColor = int(lines1[2])
             
        elif len(lines) == 2:
            # in the format of From, To
            for i in range(len(lines)):
                lines[i] = int(lines[i])
            edges.append(lines)
            
    numvertice = len({x for y in edges for x in y})
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
  
    colorAssignment = csp(numColor, numvertice, mygraph, heuristic)
    if colorAssignment != None:
        print("Vertices Color Assignment: ")
        print(colorAssignment)
    else:
        print("No solution found")
 