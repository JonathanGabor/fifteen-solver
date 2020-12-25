def generate_wd_tables():
    wd_table = []
    wd_neighbors = []
    wd_tuple_lookup = []
    for i in range(4):
        next_tuple_lookup, next_neighborhood, next_table = walking_distance_table(i)
        wd_tuple_lookup.append(next_tuple_lookup)
        wd_neighbors.append(next_neighborhood)
        wd_table.append(next_table)
    return wd_table, wd_neighbors, wd_tuple_lookup

def walking_distance_table(goal):
    state = [[4, 0, 0, 0], [0, 4, 0, 0], [0, 0, 4, 0], [0, 0, 0, 4]]
    state[goal][goal] = 3
    frontier = [(state, goal, -1, 0, -1)]
    tuple_ids = {}
    neighborhoods = []
    walking_distance = []
    id = 0
    while len(frontier) != 0:
        (state, blank, home_row, depth, origin) = frontier[0]
        a = tuple(state[0]+state[1]+state[2]+state[3])
        if a in tuple_ids:
            loc = tuple_ids[a]
            neighborhoods[loc][home_row] = origin
            neighborhoods[origin][7-home_row] = loc
        else:
            tuple_ids[a] = id
            neighborhoods.append([-1]*8)
            walking_distance.append(depth)
            if blank != 0:
                for home_row in range(4):
                    if state[blank-1][home_row] != 0:
                        new_state = [row[:] for row in state]
                        new_state[blank]  [home_row] += 1
                        new_state[blank-1][home_row] -= 1
                        frontier.append((new_state, blank-1, home_row, depth+1, id))
            if blank != 3:
                for home_row in range(4):
                    if state[blank+1][home_row] != 0:
                        new_state = [row[:] for row in state]
                        new_state[blank]  [home_row] += 1
                        new_state[blank+1][home_row] -= 1
                        frontier.append((new_state, blank+1, 7-home_row, depth+1, id))
            id += 1
        del frontier[0]
    return tuple_ids, neighborhoods, walking_distance
