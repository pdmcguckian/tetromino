# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: main
# Authors: Patrick McGuckian
# Last updated: 12th January 2020
# ####################################################


def Tetris(T):
    '''Main function that if called returns a solution to the task using the Gridfill class below. A high level overview of how
    it works is detailed in this function. For a more detailed description look through the gridfill class'''
    
    # Gridfill class is called and required global variables are found
    grid = Gridfill(T)
    
    # Method gives each position in a matrix the value of the count of the number of neighbouring positions needing filled surrounding it in the target grid T - to be used in the Greedy algorithm.
    grid.find_neighbours(0, 0, grid.width, grid.height)
    
    # Method starts filling pieces in the matrix at any point with only one neighbour - as this must be the start of the piece so the peice is likley to be correct.
    grid.fill_grid(fill_type='smart')

    # Method starts filling pieces in the matrix at any point that needs filled - acounting for any points missed by the previous method. Useful for high grid densities.
    grid.fill_grid(fill_type='dumb')

    # Final Method forces in pieces at any point it is possible and benfitil to do so (where at least 3 of the positions need to be filled).
    grid.fill_grid(fill_type='dumb', allow_force=True)

    return grid.filling_grid # Returns filling grid - the solution found by the code





class Gridfill():
    '''Grid fill class contains all the required objects and methods to complete the task. Its self.filling_grid object is the solution'''
    
    def __init__(self, T):
        '''Method defines all the required global variables and once at the start'''

        self.T = T
        self.height = len(T)    # Dimensions of grid
        self.width = len(T[0])
        self.neighbours_grid = [[0 for i in range(self.width)] for j in range(self.height)]   #Empty grid to be used as part of the greedy algorithm (see find_neighbours())
        self.filling_grid = [[(0,0) for i in range(self.width)] for j in range(self.height)]    #Empty grid to be to be filled with pieces and returned as result
        self.count = 1  #Variable to keep track of piece number as the filling grid is filled

        # piece_walk_graph dictionary contains the unweighted graph of the tree used to find spaces to place a pieces in the grid.
        # The traversal begins at 'start' and can go in any direction from there.
        # Each pieces is broken down into steps: up (u), down (d), left (l), or right(r) from the previous point.
        # Pieces that have no continuous walk from start to finish end in a 1 or 2 and the coordinates of the "jump" to the final point are given so they can still be considered.
        # A program was built to optimse the pieces priorities by testing the accuracy of every possible order and returning the best dictionary.
        self.piece_walk_graph = {
                        'start': [['l'], ['d'], ['u'], ['r']], 
                        'r': [['rr'], ['rd'], ['ru']],
                        'd': [['dl'], ['dr'], ['dd']],
                        'l': [['lu'], ['ll'], ['ld']],
                        'u': [['ur'], ['ul'], ['uu']],
                        
                        'ru': [['ru1', [0, 2]], ['rur'], ['ruu'], ['ru2', [1, 1]]],
                        'rr': [['rrd'], ['rru']],
                        'rd': [['rdr'], ['rd1', [0, -2]],['rd2', [1, -1]], ['rdd']],
                        
                        'dr': [['drr'], ['drd'], ['dr1', [-2, 0]]],
                        'dl': [['dld'], ['dll'], ['dl1', [2, 0]]], 
                        'dd': [['ddr'], ['ddl'], ['dd1', [-1, -1]], ['dd2', [1, -1]]],
                        
                        'lu': [['lu2', [-1, 1]], ['lu1', [0, 2]], ['lul'], ['luu']],
                        'll': [['lld'], ['llu']],
                        'ld': [['ld1', [-1, -1]], ['ldd'], ['ldl'], ['ld2', [0, -2]]],
                        
                        'ur': [['urr'], ['uru'], ['ur1', [-2, 0]]],
                        'ul': [['ulu'], ['ul1', [2, 0]], ['ull']],
                        'uu': [['uu1', [-1, 1]], ['uur'], ['uul'], ['uu2', [1, 1]]]
                        }

        # piece_id dirctionary contains the pieceID for all the complete pieces used when placing them in the returned grid.
        self.piece_id = {'rur': 16, 'ruu': 8, 'ru1': 14, 'ru2': 13, 'rru': 5, 'rrd': 9, 'rd2': 15, 'rdd': 6, 'rdr': 18, 'rd1': 14, 'dr1': 13, 'drd': 17, 'drr': 11, 'dll': 5, 'dld': 19, 'dl1': 13, 'dd2': 12, 'ddr': 4, 'ddl': 8, 'dd1': 14, 'lu1': 12, 'lu2': 13, 'luu': 4, 'lul': 18, 'lld': 7, 'llu': 11, 'ld2': 12, 'ldd': 10, 'ld1': 15, 'ldl': 16, 'urr': 7, 'ur1': 15, 'uru': 19, 'ull': 9, 'ulu': 17, 'ul1': 15, 'uul': 6, 'uur': 10, 'uu2': 12, 'uu1': 14}



    def find_neighbours(self, startx, starty, endx, endy):
        ''' Method gives each position needing filling a score equal to the number of neighbouring 1s.
        - Method is first passed for the entire grid. 
        - Then when a piece is placed its passed again, for a square around the point that has changed. 
        - Therefore only the positions with changed values are recalculated saving time. 
        - Updating the neighbours grid each time ensures greedy decisions are accurate.'''

        #Runs through every position being checked
        for y in range(starty, endy):
            for x in range(startx, endx):
                neighbours = 0 #Variable to record neighbours for the given position

                try: 
                    if self.T[y][x] == 1: # If position needs filled 

                        # Checks all nieghbouring pieces and adds one to neighbours if it needs filled 
                        if y+1 < self.height: #If current row is not bottom row
                            if self.T[y+1][x]== 1:
                                neighbours += 1

                        if x-1 >= 0: #If current collum is not first collum
                            if self.T[y][x-1] == 1:
                                neighbours += 1

                        if x+1 < self.width: # If current collum is not the last collum
                            if self.T[y][x+1] == 1:
                                neighbours += 1

                        if y-1 >= 0: # If current row is not top row
                            if self.T[y-1][x] == 1:
                                neighbours += 1
                        #Sets value position of nieghbours grid to the value of surrounding neigbours 
                        self.neighbours_grid[y][x] = neighbours

                except:
                    pass



    def fill_grid(self, fill_type, allow_force=False):
        '''  Method is used to search through the neighbours grid to find positions to begin filling pieces in. 
        - If fill_type is set to smart it will begin at positions with only one neighbour as these have to be the origin of a piece.
        - If fill_type is set to dumb it starts filling from the first empty position, filling any spaces missed by smart - useful for high densities. 
        - If allow_force is set to True and fill_type is dumb then it will force piecess in whenever it is benefital to do so. 
        - The method will continue to call itself recursivley until it stops being able to place a pieces (induction). '''

        should_repeat = False # Variable used to see if function should be recalled

        # Runs through entire grid
        for y_point in range(self.height):
            for x_point in range(self.width):
                
                #Smart Fill
                if self.neighbours_grid[y_point][x_point] == 1 and fill_type == 'smart': # If position has only one neighbour
    
                    shape = self.find_space(['start', [[y_point, x_point]]]) # Runs find_space() to try fill the space. If it fails to it sets shape variable to 0

                    if shape != 0: # If find_space() placed a piece
                        should_repeat = True # Sets variabe to True so method is called again

                #Dumb fill & dumb fill with force
                elif self.neighbours_grid[y_point][x_point] != 0 and fill_type == 'dumb': # If position is needs filled

                    shape = self.find_space(['start', [[y_point, x_point]]], allow_force) 

                    if shape != 0:
                        should_repeat = True 

        if should_repeat:
            return self.fill_grid(fill_type, allow_force) # Recursivley calls method
        else:
            return 0 # Ends



    def find_space(self, start, allow_force = False):
        ''' Method is used to find a piece that fits in the space. 
        - It uses the piece_walk_graph to transverse through the space needing filling, from the starting point (found by fill_grid), until it either finds
        a space to place a piece or runs out of possible pieces to fill it. 
        - It uses greedy iterative depth first search, choosing the next step from the piece_walk_graph that has the lowest number of neighbours first. If 
        that path leads to a dead end it backtracks - checking every possible piece before ending.
        - It also uses prune and search to speed up the process by not following paths that lead to a deada dead end. If the allow_force is set to True it will 
        also save any spaces only 1 step off a complete piece and attempt to force a piece into them if no complete path can be found.''' 


        to_visit = [start] # Creates the stack of nodes to visit
        could_force = [] # Creates an array for potential spaces to force pieces into

        # Repeats process until every potential node has been visited
        while len(to_visit) != 0:
            steps = to_visit[-1][1] # Takes the top position in the stack
            y_point = steps[-1][0]
            x_point = steps[-1][1]

            possible_steps = self.piece_walk_graph[to_visit[-1][0]] # Uses piece_walk_graph to find any potential possible steps

            # Cycles through the potential steps
            step_neighbours = {}
            step_coordinates = {}
            for i in possible_steps:
                
                # If it is possible to make the step and the space needs filled it's neighbours and coordinates are recorded
                # If the step can't be made that section of the graph is no longer followed (prune and search)
                if i[0][-1] == 'r' and self.possible_step(i, x_point, y_point) == 1:
                    step_coordinates[i[0]] = [y_point, x_point+1]
                    step_neighbours[i[0]] = self.neighbours_grid[y_point][x_point+1]

                elif i[0][-1] == 'd' and self.possible_step(i, x_point, y_point) == 1:
                    step_coordinates[i[0]] = [y_point + 1, x_point]
                    step_neighbours[i[0]] = self.neighbours_grid[y_point+1][x_point]

                elif i[0][-1] == 'l' and self.possible_step(i, x_point, y_point) == 1:
                    step_coordinates[i[0]] = [y_point, x_point - 1]
                    step_neighbours[i[0]] = self.neighbours_grid[y_point][x_point-1]

                elif i[0][-1] == 'u' and self.possible_step(i, x_point, y_point) == 1:
                    step_coordinates[i[0]] = [y_point - 1, x_point]
                    step_neighbours[i[0]] = self.neighbours_grid[y_point-1][x_point]
                
                elif (i[0][-1] == '1' or i[0][-1] == '2') and self.possible_step(i, x_point, y_point) == 1:
                    step_coordinates[i[0]] = [y_point + i[1][1], x_point + i[1][0]]
                    step_neighbours[i[0]] = self.neighbours_grid[y_point+i[1][1]][x_point+i[1][0]]

            del to_visit[-1] # The current step is removed from the list so it isn't visited again

            # The possible steps are sorted by the neighbour values as required by the greedy algorithm
            step_neighbours = sorted(step_neighbours.items(), key=lambda x: x[1], reverse=True)
            
            # The possible steps are added to the stack with the lowest neighbours count first (greedy algorithm)
            for i in step_neighbours:
                to_visit.append([i[0], steps + [step_coordinates[i[0]]]])

                # If allow_force is True and the length of the found path is 3 then forcing could be useful so its added to the could_force list
                if len(i[0]) == 2 and allow_force:
                    could_force.append([i[0], steps + [step_coordinates[i[0]]]])


            if len(to_visit) == 0: #If every point has been visited
                if len(could_force) != 0:   # If there are any points that could be forced it calls the forcing method
                    return self.find_force(could_force)
                return 0
            
            elif len(to_visit[-1][0]) == 3: # If the space for a full piece has been found break and call the piece fill method
                return self.fill_space(to_visit[-1][1], to_visit[-1][0])

            #If niether of the previous cases are true it repeats the process with the next item in the stack



    def find_force(self, could_force):  
        ''' Method is used to force in pieces. Pieces are only forced if there are 3 connected points needing filling and an empty space.
        This reduces missing pieces by 3 and increases excess pieces by 1 improving the score overall. It uses a similar method as find_space() 
        except it only does it for one set of possible directtions and the space doesnt need to be filled.'''

        #Cycles through all the posistions it could force
        for i in could_force:
            steps = i[1] # Steps that make up the current position
            y_point = steps[-1][0] # Coordinates of the current position 
            x_point = steps[-1][1]

            possible_pieces = self.piece_walk_graph[i[0]] #Finds potential pieces to force

            #Cycles through all potential pieces
            for piece in possible_pieces:

                #If it is possible to make the step and it doesn't overlap with another piece it's coordinates are added to the steps list
                if piece[0][-1] == 'r' and self.possible_step(piece, x_point, y_point) != float('inf'):
                    steps.append([y_point, x_point+1])

                elif piece[0][-1] == 'd' and self.possible_step(piece, x_point, y_point) != float('inf'):
                    steps.append([y_point+1, x_point])

                elif piece[0][-1] == 'l' and self.possible_step(piece, x_point, y_point) != float('inf'):
                    steps.append([y_point, x_point-1])

                elif piece[0][-1] == 'u' and self.possible_step(piece, x_point, y_point) != float('inf'):
                    steps.append([y_point-1, x_point])

                elif (piece[0][-1] == '1' or piece[0][-1] == '2') and self.possible_step(piece, x_point, y_point) != float('inf'):
                        steps.append([y_point+piece[1][1], x_point+piece[1][0]])     

                #If any forceable piece has been found the fill_space method is called and the process ends
                if len(steps) == 4:
                    return self.fill_space(steps, piece[0])

        #If no pieces can be forced the process stops
        return 0



    def possible_step(self, piece, x_point, y_point):
        ''' Method is used by find_space() and find_force() to see if a proposed step is within the borders of the grid. If it is it returns the
        value of the step position in the target grid to be tested to see if its empty/forcable by the find_space() and find_force() method '''

        if piece[0][-1] == 'r':
            if x_point+1 < self.width:
                return self.T[y_point][x_point+1]

        elif piece[0][-1] == 'd':
            if y_point+1 < self.height:
                return self.T[y_point+1][x_point]

        elif piece[0][-1] == 'l':
            if x_point-1 >= 0:
                return self.T[y_point][x_point-1]

        elif piece[0][-1] == 'u':
             if y_point-1 >= 0:
                 return self.T[y_point-1][x_point]

        elif (piece[0][-1] == '1' or piece[0][-1] == '2'):
            if y_point+piece[1][1] >= 0 and x_point+piece[1][0] >= 0:
                if x_point+piece[1][0] < self.width and y_point+piece[1][1] < self.height:
                    return self.T[y_point+piece[1][1]][x_point+piece[1][0]]

        # If step is not possible it returns infinity as this value will be rejected by the by find_space() and find_force()
        return float('inf')



    def fill_space(self, points, piece):
        ''' Method used to fill the space found using either find_space() or force_space() '''

        # Cycles through all the coordinates of the space needing filled
        for i in points:
            self.filling_grid[i[0]][i[1]] = (self.piece_id[piece], self.count) #Sets point in output grid to the required values
            self.T[i[0]][i[1]] = float('inf') #Sets the point in the target grid to infinity to desiginate it as a point that cant be changed
            self.neighbours_grid[i[0]][i[1]] = 0
        
        self.count += 1 # Adds one to piece count to keep it update
        self.find_neighbours(points[0][1]-4, points[0][0]-4, points[0][1]+4, points[0][0]+4) #Updates the neighbours grid to make sure greedy test is accurate
        
        return piece