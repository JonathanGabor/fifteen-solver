import solver
import walking_distance as wd
import random

def print_path(path):
    for i, state in enumerate(path):
        print("step " + str(i))
        print_puzzle(state)
        print("")

def print_puzzle(state):
    for row in range(4):
        for col in range(4):
            val = state[4*row + col]
            if val < 10:
                print(" ", end="")
            if val==16:
                print(" ", end="\t")
            else:
                print(str(state[4*row+col]), end="\t")
        print("")

def is_solvable(state):
    invs = 0
    z = state.index(16)
    for i in range(15):
        if i != z:
            for j in range(i+1, 16):
                if state[i] > state[j]:
                    invs += 1
    return (z//4 + invs) % 2 == 1

if __name__ == "__main__":
    wd_table, wd_neighbors, wd_tuple_lookup = wd.generate_wd_tables()

    run_times = []
    solved5 = 0
    solved30 = 0
    solved100 = 0
    max_time = 100
    num_tests = 20

    for test in range(num_tests):
        state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        random.shuffle(state)
        while not is_solvable(state):
           random.shuffle(state)

        print("\nRunning test " + str(test+1) + " out of " + str(num_tests))
        print_puzzle(state)
        print(state)

        run_time, path = solver.a_star(state, max_time, wd_tuple_lookup, wd_table, wd_neighbors)

        if run_time == -1:
            print("no solution found")
            run_times.append(max_time + 1)
        else:
            print("solved in " + str(len(path)-1) + " moves")
            print("solved in " + str(run_time) + " seconds")
            run_times.append(run_time)
            if run_time <= 101:
                solved100 += 1
                if run_time <= 30:
                    solved30 += 1
                    if run_time <= 5:
                        solved5 += 1

    print("\nSolved in 5 seconds: " + str(solved5) + "/" + str(num_tests))
    print("Solved in 30 seconds: " + str(solved30) + "/" + str(num_tests))
    print("Solved in 100 seconds: " + str(solved100) + "/" + str(num_tests))
    run_times.sort()
    print("\nBest: " + str(run_times[0]))
    print("Median: " + str(run_times[(len(run_times)-1)//2]))
    print("Worst: " + str(run_times[-1]))
