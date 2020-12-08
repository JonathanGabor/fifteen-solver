import heapq
import time

def neighbors(state, i, h_wd, v_wd, map, previous, start_blank, wd_neighbors):
    neighborhood = []

    #move blank left?
    if i%4 != 0:
        if previous != 1:
            new_state = state[:]
            new_state[i-1] = 16
            new_state[i] = state[i-1]
            n_wd = wd_neighbors[start_blank%4][v_wd][7 - map[new_state[i]-1]%4]
            neighborhood.append((new_state, i-1, h_wd, n_wd, -1))
    #move blank right?
    if i%4 != 3:
        if previous != -1:
            new_state = state[:]
            new_state[i+1] = 16
            new_state[i] = state[i+1]
            n_wd = wd_neighbors[start_blank%4][v_wd][map[new_state[i]-1]%4]
            neighborhood.append((new_state, i+1, h_wd, n_wd, 1))
    #move blank up?
    if i>3:
        if previous != 4:
            new_state = state[:]
            new_state[i-4] = 16
            new_state[i] = state[i-4]
            n_wd = wd_neighbors[start_blank//4][h_wd][7 -map[new_state[i]-1]//4]
            neighborhood.append((new_state, i-4, n_wd, v_wd, -4))
    #move blank down?
    if i<12:
        if previous != -4:
            new_state = state[:]
            new_state[i+4] = 16
            new_state[i] = state[i+4]
            n_wd = wd_neighbors[start_blank//4][h_wd][map[new_state[i]-1]//4]
            neighborhood.append((new_state, i+4, n_wd, v_wd, 4))
    return neighborhood
    
def move(state, dir, blank):
    new_state = state[:]
    new_state[blank+dir] = 16
    new_state[blank] = state[blank+dir]
    return new_state, blank+dir
    
def heuristic_manhattan(state, map):
    total = 0
    for row in range(4):
        for col in range(4):
            index = 4*row+col
            incorrect = state[index]
            if incorrect == 16: continue
            incorrect_row = int((map[incorrect-1])//4)
            incorrect_col = (map[incorrect-1])%4
            distance = abs(incorrect_row-row) + abs(incorrect_col-col)
            total+=distance
    return total

def heuristic_wd(blank, h_wd, v_wd, wd_table):
    return wd_table[blank%4][v_wd] + wd_table[blank//4][h_wd]
    
def combine_paths(initial_state, start, lookup):
    state = initial_state
    path = []
    blank = state.index(16)
    for direction in start:
        path.append(state)
        state, blank = move(state, direction, blank)
    for direction in lookup[tuple(state)]:
        path.append(state)
        state, blank = move(state, 0-direction, blank)
    path.append(state)
    return path        
       
def a_star(s, max_time, wd_tuple_lookup, wd_table, wd_neighbors):  
    end_time = time.time() + max_time

    forward_visited = [set() for i in range(16)]
    reverse_visited = [set() for i in range(16)]
    path_lookup_fw = dict()
    path_lookup_rv = dict()

    start_blank = s.index(16)

    map = [0] * 16
    h_puzzle_fw = [0] * 16
    h_puzzle_rv = [0] * 16
    v_puzzle_fw = [0] * 16
    v_puzzle_rv = [0] * 16
    for i, num in enumerate(s):
        map[num-1] = i
        if num != 16:            
            h_puzzle_fw[4*(i//4) + (num-1)//4] += 1
            h_puzzle_rv[4*((num-1)//4) + i//4] += 1
            v_puzzle_fw[4*(i%4) + (num-1)%4] += 1
            v_puzzle_rv[4*((num-1)%4) + i%4] += 1    
    h_wd_fw = wd_tuple_lookup[3]         [tuple(h_puzzle_fw)]
    h_wd_rv = wd_tuple_lookup[map[15]//4][tuple(h_puzzle_rv)]
    v_wd_fw = wd_tuple_lookup[3]         [tuple(v_puzzle_fw)]
    v_wd_rv = wd_tuple_lookup[map[15]%4] [tuple(v_puzzle_rv)]
        
    frontier = []
    heapq.heappush(frontier, (0, [], s,                                        False, start_blank, h_wd_fw, v_wd_fw, 2))
    heapq.heappush(frontier, (0, [], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], True,  15,          h_wd_rv, v_wd_rv, 2))

    while len(frontier) > 0:
        if time.time() > end_time:
            return -1, None

        (_, path, node, reversed, blank, h_wd, v_wd, previous) = heapq.heappop(frontier)

        if reversed:
            visited = tuple(node) in reverse_visited[blank]
            if not visited:
                reverse_visited[blank].add(tuple(node))
                path_lookup_rv[tuple(node)] = tuple(path[::-1])                    
            solved = tuple(node) in forward_visited[blank]
        else:
            visited = tuple(node) in forward_visited[blank]
            if not visited: 
                forward_visited[blank].add(tuple(node))
                path_lookup_fw[tuple(node)] = tuple(path[::-1])
            solved = tuple(node) in reverse_visited[blank]

        if solved:
            if reversed:
                path = combine_paths([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], path, path_lookup_fw)
                path.reverse()
            else:
                path = combine_paths(s, path, path_lookup_rv)
            return time.time() + max_time - end_time, path

        if not visited:
            if reversed:
                neighborhood = neighbors(node, blank, h_wd, v_wd, map, previous, start_blank, wd_neighbors)
            else:
                neighborhood = neighbors(node, blank, h_wd, v_wd, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], previous, 15, wd_neighbors)
            for neighbor in neighborhood:
                (nstate, nblank, nh_wd, nv_wd, nprevious) = neighbor
                new_path = path + [nprevious]
                if reversed:
                    futureCost = heuristic_wd(start_blank, nh_wd, nv_wd, wd_table)
                else:
                    futureCost = heuristic_wd(15, nh_wd, nv_wd, wd_table)
                total_cost = len(path) + futureCost
                heapq.heappush(frontier, (total_cost, new_path, nstate, reversed, nblank, nh_wd, nv_wd, nprevious))
    return -1, None
