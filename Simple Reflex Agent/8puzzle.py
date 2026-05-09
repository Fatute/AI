import numpy as np
import random

def find_blank_position(matrix):
    vi_tri = np.argwhere(matrix == 0)[0]
    return vi_tri[0], vi_tri[1]

def get_valid_moves(matrix):

    row, col = find_blank_position(matrix)
    danh_sach_buoc_di = []
    
    huong_di = [
        ["UP", -1, 0], 
        ["DOWN", 1, 0], 
        ["LEFT", 0, -1], 
        ["RIGHT", 0, 1]
    ]
    
    for ten, dg, ct in huong_di:
        dong_moi, cot_moi = row + dg, col + ct
        if 0 <= dong_moi < 3 and 0 <= cot_moi < 3:
            danh_sach_buoc_di.append((ten, dong_moi, cot_moi))
            
    return danh_sach_buoc_di

def run_reflex_agent(ini_matrix):
    trang_thai_hien_tai = np.array(ini_matrix)
    history = [] 
    buoc_dem = 0
    
    print("=== TRẠNG THÁI KHỞI ĐẦU ===")
    print(trang_thai_hien_tai)
    
    while True:
        current_list = trang_thai_hien_tai.tolist()
        
        if current_list in history:
            print(f"\n[DỪNG CHƯƠNG TRÌNH] Trùng trạng thái cũ.")
            print(f"Tổng số bước đã đi: {buoc_dem}")
            break
            
        history.append(current_list)
        
        moves = get_valid_moves(trang_thai_hien_tai)
        direction, row, col = random.choice(moves)
        
        r_empty, c_empty = find_blank_position(trang_thai_hien_tai)
        so_bi_thay_the = trang_thai_hien_tai[row, col]
        
        trang_thai_hien_tai[r_empty, c_empty] = so_bi_thay_the
        trang_thai_hien_tai[row, col] = 0
        
        buoc_dem += 1
        print(f"\nBước {buoc_dem}: Di chuyển {direction} (đổi chỗ với số {so_bi_thay_the})")
        print(trang_thai_hien_tai)


def generate_random_board():
    numbers = list(range(9))
    
    np.random.shuffle(numbers)
    
    board = np.array(numbers).reshape(3, 3)
    
    return board

matrix_3x3 = generate_random_board()
run_reflex_agent(matrix_3x3)
