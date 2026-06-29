import numpy as np
import random

def moves(matrix):
    lst_move = []
    row, col = find_vacuum_position(matrix)
    
    directions = [
        ['LEFT', 0, -1],
        ['RIGHT', 0, 1],
        ['UP', -1, 0],
        ['DOWN', 1, 0]
    ]
    
    for dir_name, dr, dc in directions:
        row_new = row + dr
        col_new = col + dc
        
        if 0 <= row_new < 4 and 0 <= col_new < 4:
            lst_move.append([dir_name, dr, dc])
            
    return lst_move

def find_vacuum_position(matrix):
    pos = np.argwhere(matrix == 'x')
    if len(pos) == 0:
        return 0, 0
    return pos[0][0], pos[0][1]

def result_action(matrix, row, col, action):
    temp_mat = np.copy(matrix)
    _, dr, dc = action
    
    row_new, col_new = row + dr, col + dc
    
    temp_mat[row, col] = '0'
    temp_mat[row_new, col_new] = 'x'
     
    return temp_mat

def matrix_to_to_tuple(matrix):
    return tuple(map(tuple, matrix))

def or_search(state, path):
    if '1' not in state:
        return []
    
    state_tuple = matrix_to_to_tuple(state)
    if state_tuple in path:
        return False
    
    actions = moves(state)
    row, col = find_vacuum_position(state)
    
    for act in actions:
        result_state = result_action(state, row, col, act)
        possible_states = [result_state]
        
        lucky = random.random()
        if lucky > 0.7:
            possible_states.append(np.copy(state))
        
        new_path = path + [state_tuple]
        plan = and_search(possible_states, new_path)
        
        if plan != False:
            return [act[0], plan]
            
    return False

def and_search(states, path):
    plans = {}
    for s in states:
        s_tuple = matrix_to_to_tuple(s)
        plan_x = or_search(s, path)
    
        if plan_x == False:
            return False
    
        plans[s_tuple] = plan_x
    
    return plans

def and_or_search(initial_matrix):
    return or_search(initial_matrix, [])

def print_clean_plan(plan):
    spacing = "  "
    if plan == []:
        print(f"{spacing}➔ [MỤC TIÊU ĐẠT ĐƯỢC - SẠCH RÁC!] 🎉")
        return
    if plan == False:
        print(f"{spacing}➔ [THẤT BẠI]")
        return
        
    action, next_contingencies = plan
    print(f"{spacing}➔ Hành động: {action}")
    
    if isinstance(next_contingencies, dict):
        for i, (state, sub_plan) in enumerate(next_contingencies.items(), 1):
            clean_state = [[str(cell) for cell in row] for row in state]
            print(f"{spacing}  └─ Nếu trạng thái môi trường trở thành:")
            for row in clean_state:
                print(f"{spacing}     {row}")
            print_clean_plan(sub_plan)


if __name__ == "__main__":
    matrix = np.array([
        ['1', '1', '1', '0'],
        ['0', '0', 'x', '1'],
        ['1', '1', '0', '0'],
        ['1', '1', '0', '1']
    ])
    
    print("Trạng thái bắt đầu:")
    print(matrix)
    
    plan = and_or_search(matrix)
    print("\nKế hoạch tìm được (Plan):")
    print_clean_plan(plan)