# === Cell 2 ===
from tkinter import *
from tkinter import ttk
import numpy as np
import math
import random
import time
import sys
sys.path.append("..")
from Node import Node
# === Cell 3 ===
# Biến toàn cục dùng chung cho GUI
cells = []
cells2 = [] # Cho ma trận thứ 2 trong Tìm kiếm mù
selected_algo = None
selected_blind_algo = None
selected_csp_algo = None
selected_adversarial_algo = None
current_group = "menu" # Màn hình hiện tại: menu, blind, others, csp, adversarial
window = None
text_area = None
solution_text = None
stop_execution = False

# Biến dùng cho Adversarial
adversarial_nodes = 0
adversarial_board = []

# Biến dùng cho CSP
csp_canvas = None
csp_tree = None
tree_items = {}
polygon_ids = {}
speed_scale = None

# Node positions cho đồ thị ràng buộc CSP (x, y) trên canvas
node_positions = {
    "Củ Chi":    (155, 55),
    "Hóc Môn":   (180, 145),
    "Quận 12":   (295, 140),
    "Gò Vấp":    (340, 200),
    "Bình Thạnh":(410, 205),
    "Thủ Đức":   (490, 165),
    "Tân Bình":  (315, 255),
    "Tân Phú":   (245, 255),
    "Bình Tân":  (190, 305),
    "Bình Chánh":(155, 435),
    "Phú Nhuận": (385, 255),
    "Quận 10":   (335, 305),
    "Quận 11":   (275, 305),
    "Quận 3":    (395, 305),
    "Quận 1":    (435, 340),
    "Quận 5":    (355, 360),
    "Quận 6":    (280, 360),
    "Quận 4":    (460, 385),
    "Quận 8":    (315, 415),
    "Quận 7":    (460, 440),
    "Nhà Bè":    (430, 510),
    "Cần Giờ":   (490, 590),
}
NODE_RADIUS = 24

# Keep label_positions for legacy compatibility
label_positions = {k: list(v) for k, v in node_positions.items()}

colors_hex = {"Đỏ": "#FF5733", "Xanh lá": "#2ECC71", "Xanh dương": "#3498DB", "Vàng": "#F1C40F"}

variables = [
    "Củ Chi", "Hóc Môn", "Quận 12", "Bình Tân", "Bình Chánh", "Gò Vấp", "Tân Bình", "Tân Phú", 
    "Bình Thạnh", "Thủ Đức", "Phú Nhuận", "Quận 10", "Quận 11", "Quận 3", "Quận 1", "Quận 5",  
    "Quận 6", "Quận 4", "Quận 8", "Quận 7", "Nhà Bè", "Cần Giờ"
]

constrain = {
    "Củ Chi": ["Quận 12"],
    "Hóc Môn": ["Quận 12", "Bình Tân", "Bình Chánh", "Củ Chi"],
    "Quận 12": ["Gò Vấp", "Hóc Môn", "Tân Bình", "Tân Phú", "Bình Tân", "Thủ Đức", "Bình Thạnh"],
    "Bình Tân": ["Hóc Môn", "Quận 12", "Tân Phú", "Quận 6", "Quận 8", "Bình Chánh"],
    "Bình Chánh": ["Hóc Môn", "Bình Tân", "Quận 7", "Quận 8", "Nhà Bè"],
    "Gò Vấp": ["Quận 12", "Phú Nhuận", "Tân Bình", "Bình Thạnh", "Thủ Đức"],
    "Tân Bình": ["Quận 12", "Phú Nhuận", "Quận 11", "Quận 10", "Bình Tân", "Quận 3", "Quận 6"],
    "Tân Phú": ["Quận 12", "Bình Tân", "Quận 11", "Quận 6"],
    "Bình Thạnh": ["Quận 12", "Gò Vấp", "Phú Nhuận", "Quận 1", "Quận 4", "Thủ Đức"],
    "Thủ Đức": ["Quận 12", "Gò Vấp", "Phú Nhuận", "Bình Thạnh", "Quận 1", "Quận 4", "Quận 7"],
    "Phú Nhuận": ["Gò Vấp", "Tân Bình", "Quận 3", "Quận 1", "Thủ Đức", "Bình Thạnh"],
    "Quận 10": ["Quận 11", "Quận 5", "Tân Bình", "Quận 3", "Quận 4"],
    "Quận 11": ["Quận 10", "Tân Bình", "Tân Phú", "Quận 6", "Quận 4"],
    "Quận 3": ["Tân Bình", "Phú Nhuận", "Quận 5", "Quận 1", "Quận 10"],
    "Quận 1": ["Thủ Đức", "Bình Thạnh", "Phú Nhuận", "Quận 3", "Quận 5", "Quận 4"],
    "Quận 5": ["Quận 1", "Quận 3", "Quận 6", "Quận 8", "Quận 10", "Quận 11"],
    "Quận 6": ["Bình Tân", "Tân Bình", "Tân Phú", "Quận 11", "Quận 5", "Quận 8"],
    "Quận 4": ["Bình Thạnh", "Thủ Đức", "Quận 1", "Quận 7", "Quận 10", "Quận 11"],
    "Quận 8": ["Bình Tân", "Bình Chánh", "Quận 5", "Quận 6", "Quận 7"],
    "Quận 7": ["Quận 8", "Quận 4", "Thủ Đức", "Bình Chánh", "Nhà Bè"],
    "Nhà Bè": ["Cần Giờ", "Quận 7", "Bình Chánh"],
    "Cần Giờ": ["Nhà Bè"]
}

# Đảm bảo đồ thị ràng buộc là ĐỐI XỨNG (hai chiều)
# Ví dụ: nếu Củ Chi → Quận 12 thì Quận 12 cũng phải → Củ Chi
for _area, _neighbors in list(constrain.items()):
    for _nb in _neighbors:
        if _area not in constrain[_nb]:
            constrain[_nb].append(_area)

colors = ["Đỏ", "Vàng", "Xanh lá", "Xanh dương"]
result = {}

def reset_view():
    for widget in window.winfo_children():
        widget.grid_forget()
        widget.pack_forget()

def trigger_stop():
    global stop_execution
    stop_execution = True

def exit_visualizer():
    global stop_execution
    stop_execution = True
    show_menu()

def reset_others_ui():
    if 'solution_text' in globals() and solution_text:
        try:
            solution_text.delete(1.0, END)
        except Exception:
            pass
    if 'text_area' in globals() and text_area:
        try:
            text_area.delete(1.0, END)
        except Exception:
            pass
    try:
        mat, r, c = create_mat()
        draw_state(mat)
    except Exception:
        pass

def reset_blind_ui():
    if 'solution_text' in globals() and solution_text:
        try:
            solution_text.delete(1.0, END)
        except Exception:
            pass
    if 'text_area' in globals() and text_area:
        try:
            text_area.delete(1.0, END)
        except Exception:
            pass
    try:
        algo = selected_blind_algo.get()
        if algo == "Mù Partial":
            real_state = np.array([
                ['1', '?', '1', '0'],
                ['0', '0', '?', '1'],
                ['x', '1', '0', '1'],
                ['?', '?', '?', '?']
            ])
            start_belief = [
                np.array([['1', '0', '1', '0'],
                          ['0', '0', '0', '1'],
                          ['x', '1', '0', '1'],
                          ['0', '0', '0', '1']]),
                np.array([['1', '0', '0', '0'],
                          ['1', '1', '1', 'x'],
                          ['1', '0', '0', '0'],
                          ['1', '1', '0', '0']])
            ]
            try:
                grid1_frame = window.nametowidget(".!frame.!labelframe")
                grid1_frame.config(text="Belief State A")
                grid2_frame = window.nametowidget(".!frame.!labelframe2")
                grid2_frame.config(text="Belief State B")
            except Exception:
                pass
            draw_blind_states(start_belief[0], start_belief[1])
        else:
            start_belief = [
                np.array([['1', '0', '1', '0'],
                          ['0', '0', '0', '1'],
                          ['x', '1', '0', '1'],
                          ['0', '0', '0', '1']]),
                np.array([['1', '0', '0', '0'],
                          ['1', '1', '1', 'x'],
                          ['1', '0', '0', '0'],
                          ['1', '1', '0', '0']])
            ]
            try:
                grid1_frame = window.nametowidget(".!frame.!labelframe")
                grid1_frame.config(text="Belief State A")
                grid2_frame = window.nametowidget(".!frame.!labelframe2")
                grid2_frame.config(text="Belief State B / Real")
            except Exception:
                pass
            draw_blind_states(start_belief[0], start_belief[1])
    except Exception:
        pass

def reset_csp_ui():
    global result
    if 'solution_text' in globals() and solution_text:
        try:
            solution_text.delete(1.0, END)
        except Exception:
            pass
    if 'text_area' in globals() and text_area:
        try:
            text_area.delete(1.0, END)
        except Exception:
            pass
    try:
        result.clear()
    except Exception:
        pass
    try:
        draw_blank_map()
    except Exception:
        pass

def reset_adversarial_ui():
    global adversarial_board
    adversarial_board = [
        ['', 'O', 'X'],
        ['', 'O', ''],
        ['X', '', '']
    ]
    if 'solution_text' in globals() and solution_text:
        try:
            solution_text.delete(1.0, END)
        except Exception:
            pass
    if 'text_area' in globals() and text_area:
        try:
            text_area.delete(1.0, END)
        except Exception:
            pass
    try:
        draw_adversarial_board()
    except Exception:
        pass

def cell_clicked(row, col):
    global stop_execution
    if current_group != "adversarial" or not stop_execution:
        return
    val = adversarial_board[row][col]
    if val == "":
        adversarial_board[row][col] = "X"
    elif val == "X":
        adversarial_board[row][col] = "O"
    else:
        adversarial_board[row][col] = ""
    draw_adversarial_board()

def draw_adversarial_board():
    for r in range(3):
        for c in range(3):
            val = adversarial_board[r][c]
            lbl = cells[r][c]
            lbl.config(text=val)
            if val == 'X':
                lbl.config(fg='#FF5733')
            elif val == 'O':
                lbl.config(fg='#3498DB')
            else:
                lbl.config(fg='black')

def on_adversarial_algo_change(*args):
    global stop_execution
    stop_execution = True
    if current_group == "adversarial":
        reset_adversarial_ui()

def on_algo_change(*args):
    global stop_execution
    stop_execution = True
    if current_group == "others":
        reset_others_ui()

def on_blind_algo_change(*args):
    global stop_execution
    stop_execution = True
    if current_group == "blind":
        reset_blind_ui()

def on_csp_algo_change(*args):
    global stop_execution
    stop_execution = True
    if current_group == "csp":
        reset_csp_ui()

# --- MÀN HÌNH CHỌN NHÓM THUẬT TOÁN (MENU) ---
def show_menu():
    global current_group
    current_group = "menu"
    reset_view()
    
    # Tiêu đề chính
    title_lbl = Label(window, text="HỆ THỐNG TRỰC QUAN HÓA THUẬT TOÁN TÌM KIẾM", font=("Times New Roman", 18, "bold"), bg="#eaeaea", fg="black")
    title_lbl.pack(pady=40)
    
    sub_lbl = Label(window, text="Chọn nhóm thuật toán để bắt đầu trực quan hóa:", font=("Times New Roman", 12, "bold"), bg="#eaeaea", fg="gray")
    sub_lbl.pack(pady=10)
    
    # Frame chứa 4 nút chọn nhóm lớn (lưới 2x2)
    btn_frame = Frame(window, bg="#eaeaea")
    btn_frame.pack(pady=20)
    
    btn_blind = Button(
        btn_frame, 
        text="1. Thuật toán tìm kiếm mù\n(Sensorless & Partial Observation)", 
        font=("Times New Roman", 12, "bold"), 
        bg="cyan", 
        fg="black", 
        width=35, 
        height=5, 
        relief=RAISED, 
        cursor="hand2", 
        command=show_blind_visualizer
    )
    btn_blind.grid(row=0, column=0, padx=20, pady=15)
    
    btn_others = Button(
        btn_frame, 
        text="2. Nhóm còn lại\n(BFS, DFS, UCS, A*, Local Search...)", 
        font=("Times New Roman", 12, "bold"), 
        bg="cyan", 
        fg="black", 
        width=35, 
        height=5, 
        relief=RAISED, 
        cursor="hand2", 
        command=show_others_visualizer
    )
    btn_others.grid(row=0, column=1, padx=20, pady=15)

    btn_csp = Button(
        btn_frame, 
        text="3. Tô màu bản đồ\n(CSP - Backtracking & Forward Checking)", 
        font=("Times New Roman", 12, "bold"), 
        bg="cyan", 
        fg="black", 
        width=35, 
        height=5, 
        relief=RAISED, 
        cursor="hand2", 
        command=show_csp_visualizer
    )
    btn_csp.grid(row=1, column=0, padx=20, pady=15)

    btn_adversarial = Button(
        btn_frame, 
        text="4. Thuật toán đối kháng\n(Tic Tac Toe - Minimax, Alpha-Beta, Expectimax)", 
        font=("Times New Roman", 12, "bold"), 
        bg="cyan", 
        fg="black", 
        width=35, 
        height=5, 
        relief=RAISED, 
        cursor="hand2", 
        command=show_adversarial_visualizer
    )
    btn_adversarial.grid(row=1, column=1, padx=20, pady=15)

def show_others_visualizer():
    global text_area, solution_text, cells, current_group
    current_group = "others"
    reset_view()
    
    # Cấu hình thanh sidebar chọn thuật toán (style cyan)
    but_frame = Frame(window, bg="cyan")
    but_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    Label(
        but_frame,
        text="Algorithms",
        font=("Times New Roman", 14, "bold"),
        bg="cyan"
    ).pack(pady=10)
    
    algorithms = [
        ("BFS_1", "BFS_1"), ("BFS_2", "BFS_2"),
        ("DFS_1", "DFS_1"), ("DFS_2", "DFS_2"),
        ("IDS_1", "IDS_1"), ("IDS_2", "IDS_2"),
        ("UCS", "UCS"), ("Greedy", "Greedy"),
        ("A_star", "A_star"), ("Ids_A_atar", "Ids_A_atar"),
        ("Simple_Hill", "Simple_Hill"), ("Steepest Ascent", "Steepest Ascent"),
        ("Stochastic", "Stochastic"), ("Random Restart", "Random Restart"),
        ("Beam Search", "Beam Search"), ("Simulate Annealing", "Simulate Annealing")
    ]
    
    # Sử dụng Canvas có Scrollbar cho danh sách dài 16 thuật toán (giao diện nhỏ gọn với width=150)
    algo_canvas = Canvas(but_frame, bg="cyan", highlightthickness=0, width=150)
    algo_scrollbar = Scrollbar(but_frame, orient="vertical", command=algo_canvas.yview)
    scroll_frame = Frame(algo_canvas, bg="cyan")
    
    scroll_frame.bind(
        "<Configure>",
        lambda e: algo_canvas.configure(scrollregion=algo_canvas.bbox("all"))
    )
    algo_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    algo_canvas.configure(yscrollcommand=algo_scrollbar.set)
    
    algo_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
    algo_scrollbar.pack(side="right", fill="y")
    
    for display_name, value_name in algorithms:
        Radiobutton(
            scroll_frame,
            text=display_name,
            variable=selected_algo,
            value=value_name,
            font=("Times New Roman", 10, "bold"),
            bg="cyan",
            anchor="w"
        ).pack(fill="x", padx=10, pady=3)
        
    bottom_btn_frame = Frame(but_frame, bg="cyan")
    bottom_btn_frame.pack(side="bottom", fill="x", pady=5)
    
    Button(bottom_btn_frame, text="RUN", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=run_others).pack(pady=5)
    Button(bottom_btn_frame, text="STOP", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=trigger_stop).pack(pady=5)
    Button(bottom_btn_frame, text="EXIT", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=exit_visualizer).pack(pady=5)
    
    # 4x4 Grid Matrix ở giữa
    frame = Frame(window)
    frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    for r in range(4):
        frame.rowconfigure(r, weight=1)
        frame.columnconfigure(r, weight=1)
        
    cells = []
    for row in range(4):
        temp = []
        for col in range(4):
            cell = Frame(frame, width=90, height=90, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            temp.append(cell)
        cells.append(temp)
        
    # Nhật ký log ở bên phải
    text_area = Text(window, width=40, height=18, relief=RAISED, font=("Segoe UI", 11), bg="black", fg="white")
    text_area.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    
    # Panel hiển thị đường đi giải pháp ở dưới
    solution_text = Text(window, width=88, height=9, relief=RAISED, font=("Segoe UI", 11))
    solution_text.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    # Vẽ trạng thái xuất phát mặc định
    reset_others_ui()

def run_others():
    global stop_execution
    stop_execution = False
    
    solution_text.delete(1.0, END)
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()
    algo = selected_algo.get()
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    window.update()
    
    solutions = None
    reached = None
    message = ""
    
    # Gọi hàm thuật toán
    if algo == "BFS_1":
        solutions, reached = bfs_1(matrix, row, col)
    elif algo == "BFS_2":
        solutions, reached = bfs_2(matrix, row, col)
    elif algo == "DFS_1":
        solutions, reached = dfs_1(matrix, row, col)
    elif algo == "DFS_2":
        solutions, reached = dfs_2(matrix, row, col)
    elif algo == "IDS_1":
        solutions, reached = ids_1(matrix, row, col)
    elif algo == "IDS_2":
        solutions, reached = ids_2(matrix, row, col)
    elif algo == "UCS":
        solutions, reached = ucs(matrix, row, col)
    elif algo == "Greedy":
        solutions, reached = greedy(matrix, row, col)
    elif algo == "A_star":
        solutions, reached = a_star(matrix, row, col)
    elif algo == "Ids_A_atar":
        solutions, reached = ida_star(matrix, row, col)
    elif algo == "Simple_Hill":
        reached, message = simple_hill_climbing(matrix, row, col)
        solutions = [(None, s) for s in reached]
    elif algo == "Steepest Ascent":
        reached_tuples, message = steepest_ascent(matrix, row, col)
        solutions = reached_tuples
        reached = [item[1] for item in reached_tuples]
    elif algo == "Stochastic":
        reached_tuples, message = stochastic(matrix, row, col)
        solutions = reached_tuples
        reached = [item[1] for item in reached_tuples]
    elif algo == "Random Restart":
        solutions, reached_list, message = random_restart(matrix, row, col)
    elif algo == "Beam Search":
        solutions, message = beam_search(matrix, row, col, k=2)
    elif algo == "Simulate Annealing":
        solutions, message = simulated_annealing(matrix, row, col)

    # Trực quan hóa quá trình tìm kiếm (Exploration) (Đã ẩn để chỉ in đường đi)
    # if reached and algo not in ["Simple_Hill", "Steepest Ascent", "Stochastic", "Random Restart"]:
    #     for state in reached:
    #         if stop_execution:
    #             text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
    #             return
    #         state_arr = np.array(state)
    #         draw_state(state_arr)
    #         window.update()
    #         time.sleep(0.08)
            
    if algo == "Random Restart" and reached_list:
        for restart_id, history in enumerate(reached_list):
            if stop_execution:
                text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                return
            solution_text.insert(END, f"\n========== RESTART {restart_id + 1} ==========\n")
            for state in history:
                if stop_execution:
                    text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                    return
                draw_state(state)
                window.update()
                solution_text.insert(END, str(state) + "\n\n")
                time.sleep(0.4)
                
    # Trực quan hóa hoạt họa đường đi giải pháp
    if solutions:
        text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        solution_str = 'SOLUTION: '
        
        # Vẽ lại vị trí bắt đầu
        mat, r_v, c_v = create_mat()
        draw_state(mat)
        
        for idx, node in enumerate(solutions):
            if stop_execution:
                text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                return
            action = node[0]
            state = node[1]
            draw_state(state)
            
            if action == 'UP':
                text_area.insert(END, f"Máy đang di chuyển {action} đến vị trí [{r_v - 1}, {c_v}]\n")
                r_v -= 1
            elif action == 'DOWN':
                text_area.insert(END, f"Máy đang di chuyển {action} đến vị trí [{r_v + 1}, {c_v}]\n")
                r_v += 1
            elif action == 'LEFT':
                text_area.insert(END, f"Máy đang di chuyển {action} đến vị trí [{r_v}, {c_v - 1}]\n")
                c_v -= 1
            elif action == 'RIGHT':
                text_area.insert(END, f"Máy đang di chuyển {action} đến vị trí [{r_v}, {c_v + 1}]\n")
                c_v += 1
            elif action == 'SUCK':
                text_area.insert(END, f"Máy đang hút bụi (SUCK)\n")
                
            window.update()
            
            if action is not None:
                solution_str += action + " --> "
                
            solution_text.insert(END, '\n')
            if action is None:
                solution_text.insert(END, "TRẠNG THÁI BAN ĐẦU\n")
            else:
                solution_text.insert(END, "Hướng: " + action + "\n")
            solution_text.insert(END, str(state))
            solution_text.insert(END, '\n\n')
            time.sleep(0.6)
            
        solution_text.insert(END, solution_str[:-5] if solution_str.endswith(" --> ") else solution_str)
    else:
        if algo not in ["Random Restart"]:
            text_area.insert(END, "KHÔNG TÌM THẤY ĐƯỜNG ĐI!\n")
            solution_text.insert(END, "NO SOLUTION")

def draw_blind_states(state1, state2=None, is_sensorless=False):
    # Vẽ Grid 1
    for i in range(4):
        for j in range(4):
            val = state1[i][j]
            cell = cells[i][j]
            if val == '1' or val == 'd':
                cell.config(bg='red')
            elif val == '0':
                cell.config(bg='light green')
            elif val == 'x':
                cell.config(bg='yellow')
            elif val == '?':
                cell.config(bg='gray')

    # Vẽ Grid 2
    if state2 is not None:
        for i in range(4):
            for j in range(4):
                val = state2[i][j]
                cell = cells2[i][j]
                if val == '1' or val == 'd':
                    cell.config(bg='red')
                elif val == '0':
                    cell.config(bg='light green')
                elif val == 'x':
                    cell.config(bg='yellow')
                elif val == '?':
                    cell.config(bg='gray')


def show_blind_visualizer():
    global text_area, solution_text, cells, cells2, current_group
    current_group = "blind"
    reset_view()
    
    # Sidebar chọn thuật toán màu cyan
    but_frame = Frame(window, bg="cyan")
    but_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    Label(
        but_frame,
        text="Blind Search",
        font=("Times New Roman", 14, "bold"),
        bg="cyan"
    ).pack(pady=10)
    
    blind_algos = [
        ("Mù Start", "Mù Start"),
        ("Mù Goal", "Mù Goal"),
        ("Mù Partial", "Mù Partial")
    ]
    
    for display_name, value_name in blind_algos:
        Radiobutton(
            but_frame,
            text=display_name,
            variable=selected_blind_algo,
            value=value_name,
            font=("Times New Roman", 10, "bold"),
            bg="cyan",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
    bottom_btn_frame = Frame(but_frame, bg="cyan")
    bottom_btn_frame.pack(side="bottom", fill="x", pady=5)
    
    Button(bottom_btn_frame, text="RUN", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=run_blind).pack(pady=5)
    Button(bottom_btn_frame, text="STOP", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=trigger_stop).pack(pady=5)
    Button(bottom_btn_frame, text="EXIT", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=exit_visualizer).pack(pady=5)
    
    # Grid Container ở giữa chứa 2 lưới con side-by-side
    frame = Frame(window)
    frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    
    # 2 nhãn tiêu đề Belief A / B để phân biệt 2 lưới
    grid1_box = LabelFrame(frame, text="Belief State A", font=("Times New Roman", 10, "bold"))
    grid1_box.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    for r in range(4):
        grid1_box.rowconfigure(r, weight=1)
        grid1_box.columnconfigure(r, weight=1)
        
    grid2_box = LabelFrame(frame, text="Belief State B / Real", font=("Times New Roman", 10, "bold"))
    grid2_box.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    for r in range(4):
        grid2_box.rowconfigure(r, weight=1)
        grid2_box.columnconfigure(r, weight=1)
        
    cells = []
    for row in range(4):
        temp = []
        for col in range(4):
            cell = Frame(grid1_box, width=70, height=70, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            temp.append(cell)
        cells.append(temp)
        
    cells2 = []
    for row in range(4):
        temp = []
        for col in range(4):
            cell = Frame(grid2_box, width=70, height=70, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            temp.append(cell)
        cells2.append(temp)
        
    # Nhật ký ở bên phải
    text_area = Text(window, width=40, height=18, relief=RAISED, font=("Segoe UI", 11), bg="black", fg="white")
    text_area.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    
    # Kết quả đường đi giải pháp ở dưới
    solution_text = Text(window, width=88, height=9, relief=RAISED, font=("Segoe UI", 11))
    solution_text.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    # Khởi tạo vẽ 2 lưới ban đầu
    reset_blind_ui()

def run_blind():
    global stop_execution
    stop_execution = False
    
    solution_text.delete(1.0, END)
    text_area.delete(1.0, END)
    
    algo = selected_blind_algo.get()
    text_area.insert(END, f"TRẠNG THÁI THUẬT TOÁN MÙ: {algo}\n")
    text_area.insert(END, "SEARCHING TIME... \n")
    window.update()
    
    if algo == "Mù Start" or algo == "Mù Goal":
        start_belief = [
            np.array([['1', '0', '1', '0'],
                      ['0', '0', '0', '1'],
                      ['x', '1', '0', '1'],
                      ['0', '0', '0', '1']]),
            np.array([['1', '0', '0', '0'],
                      ['1', '1', '1', 'x'],
                      ['1', '0', '0', '0'],
                      ['1', '1', '0', '0']])
        ]
        
        if algo == "Mù Start":
            solutions, explored = sensorless_search_bfs(start_belief)
        else:
            solutions, explored = sensorless_search_dfs(start_belief)
            
        # Trực quan duyệt Belief States (Đã ẩn để chỉ in đường đi)
        # for belief in explored:
        #     if stop_execution:
        #         text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
        #         return
        #     s1 = belief[0]
        #     s2 = belief[1] if len(belief) > 1 else belief[0]
        #     draw_blind_states(s1, s2)
        #     window.update()
        #     time.sleep(0.15)
            
        if solutions:
            text_area.insert(END, "ĐÃ TÌM ĐƯỢC CHUỖI HÀNH ĐỘNG THÀNH CÔNG!\n")
            draw_blind_states(start_belief[0], start_belief[1])
            window.update()
            time.sleep(0.5)
            
            solution_str = "SOLUTION: "
            for idx, (action, belief) in enumerate(solutions):
                if stop_execution:
                    text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                    return
                s1 = belief[0]
                s2 = belief[1] if len(belief) > 1 else belief[0]
                draw_blind_states(s1, s2)
                
                text_area.insert(END, f"Bước {idx+1}: Di chuyển {action}\n")
                window.update()
                
                solution_str += action + " --> "
                solution_text.insert(END, f"Bước {idx+1}: Hướng {action}\n")
                solution_text.insert(END, f"Belief State A:\n{str(s1)}\nBelief State B:\n{str(s2)}\n\n")
                time.sleep(0.8)
                
            solution_text.insert(END, solution_str[:-5])
        else:
            text_area.insert(END, "KHÔNG TÌM THẤY ĐƯỜNG ĐI MÙ!\n")
            solution_text.insert(END, "NO SOLUTION")
            
    elif algo == "Mù Partial":
        start_belief = [
            np.array([['1', '0', '1', '0'],
                      ['0', '0', '0', '1'],
                      ['x', '1', '0', '1'],
                      ['0', '0', '0', '1']]),
            np.array([['1', '0', '0', '0'],
                      ['1', '1', '1', 'x'],
                      ['1', '0', '0', '0'],
                      ['1', '1', '0', '0']])
        ]
        real_state = np.array([
            ['1', '?', '1', '0'],
            ['0', '0', '?', '1'],
            ['x', '1', '0', '1'],
            ['?', '?', '?', '?']
        ])
        
        # Grid 1: Hiển thị Belief State (A), Grid 2: Hiển thị trạng thái Thực (Real State)
        grid1_frame = window.nametowidget(".!frame.!labelframe")
        grid1_frame.config(text="Belief State")
        grid2_frame = window.nametowidget(".!frame.!labelframe2")
        grid2_frame.config(text="Real State (With '?')")
        
        solutions, explored = partially_observation_search(start_belief, real_state)
        
        # Trực quan hóa bước duyệt (Đã ẩn để chỉ in đường đi)
        # for belief, real in explored:
        #     if stop_execution:
        #         text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
        #         return
        #     draw_blind_states(belief[0], real)
        #     window.update()
        #     time.sleep(0.2)
            
        if solutions:
            text_area.insert(END, "ĐÃ TÌM THẤY LỜI GIẢI AN TOÀN CHO MÔI TRƯỜNG MỘT PHẦN!\n")
            draw_blind_states(start_belief[0], real_state)
            window.update()
            time.sleep(0.5)
            
            solution_str = "SOLUTION: "
            curr_real = real_state.copy()
            for idx, (action, belief) in enumerate(solutions):
                if stop_execution:
                    text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                    return
                curr_real = transition_partial(curr_real, action)
                s1 = belief[0]
                draw_blind_states(s1, curr_real)
                
                text_area.insert(END, f"Bước {idx+1}: Di chuyển: {action}\n")
                window.update()
                
                solution_str += action + " --> "
                solution_text.insert(END, f"Bước {idx+1}: Hành động {action}\n")
                solution_text.insert(END, f"Niềm tin (Belief A):\n{str(s1)}\nThực tế (Real State):\n{str(curr_real)}\n\n")
                time.sleep(0.8)
                
            solution_text.insert(END, solution_str[:-5])
        else:
            text_area.insert(END, "KHÔNG TÌM THẤY ĐƯỜNG ĐI!\n")
            solution_text.insert(END, "NO SOLUTION")

def show_csp_visualizer():
    global text_area, solution_text, current_group, csp_canvas, csp_tree, tree_items, speed_scale
    current_group = "csp"
    reset_view()
    
    # Sidebar chọn thuật toán màu cyan (Cột 0)
    but_frame = Frame(window, bg="cyan")
    but_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    Label(
        but_frame,
        text="CSP Map Coloring",
        font=("Times New Roman", 14, "bold"),
        bg="cyan"
    ).pack(pady=10)
    
    csp_algos = [
        ("Backtracking", "Backtracking"),
        ("Forward Checking", "Forward Checking"),
        ("AC3", "AC3"),
        ("Min-Conflicts", "Min-Conflicts")
    ]
    
    for display_name, value_name in csp_algos:
        Radiobutton(
            but_frame,
            text=display_name,
            variable=selected_csp_algo,
            value=value_name,
            font=("Times New Roman", 10, "bold"),
            bg="cyan",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
    # Thanh trượt điều chỉnh tốc độ hoạt họa
    Label(but_frame, text="Tốc độ hoạt họa (s):", font=("Times New Roman", 10, "bold"), bg="cyan").pack(anchor="w", padx=10, pady=(15, 0))
    speed_scale = ttk.Scale(but_frame, from_=0.01, to=1.5, value=0.15)
    speed_scale.pack(fill="x", padx=10, pady=5)

    bottom_btn_frame = Frame(but_frame, bg="cyan")
    bottom_btn_frame.pack(side="bottom", fill="x", pady=5)
    
    Button(bottom_btn_frame, text="RUN", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=run_csp).pack(pady=5)
    Button(bottom_btn_frame, text="STOP", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=trigger_stop).pack(pady=5)
    Button(bottom_btn_frame, text="EXIT", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=exit_visualizer).pack(pady=5)
    
    # ---- CỘT 1: CANVAS HIỂN THỊ BẢN ĐỒ ----
    left_frame = Frame(window, bg="#ECEFF1")
    left_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    title_label = Label(left_frame, text="Đồ thị ràng buộc – Tô màu TP.HCM (CSP)", font=("Arial", 12, "bold"), bg="#ECEFF1", anchor="w")
    title_label.pack(fill=X, pady=(0, 5))

    csp_canvas = Canvas(left_frame, bg="#E3F2FD", highlightthickness=1, highlightbackground="#B0BEC5")
    csp_canvas.pack(fill=BOTH, expand=True)

    # ---- CỘT 2: PANEL TRẠNG THÁI & CHÚ GIẢI ----
    right_frame = Frame(window, width=320, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CFD8DC")
    right_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
    right_frame.grid_propagate(False)
    
    # 1. Khung mẫu màu chú thích
    color_group = LabelFrame(right_frame, text="Màu sử dụng", font=("Arial", 10, "bold"), bg="#FFFFFF", padx=10, pady=5)
    color_group.pack(fill=X, padx=5, pady=5)
    for name, hex_code in colors_hex.items():
        f = Frame(color_group, bg="#FFFFFF")
        f.pack(fill=X, pady=2)
        lbl_box = Label(f, bg=hex_code, width=4, relief="groove")
        lbl_box.pack(side=LEFT, padx=(0, 10))
        Label(f, text=name, bg="#FFFFFF", font=("Arial", 9)).pack(side=LEFT)

    # 2. Khung bảng trạng thái màu hiện tại
    status_group = LabelFrame(right_frame, text="Bảng trạng thái màu", font=("Arial", 10, "bold"), bg="#FFFFFF", padx=10, pady=5)
    status_group.pack(fill=BOTH, expand=True, padx=5, pady=5)

    # Treeview hiển thị danh sách vùng
    csp_tree = ttk.Treeview(status_group, columns=("Vùng", "Màu"), show="headings", height=15)
    csp_tree.heading("Vùng", text="Vùng")
    csp_tree.heading("Màu", text="Màu")
    csp_tree.column("Vùng", width=140, anchor="center")
    csp_tree.column("Màu", width=120, anchor="center")
    csp_tree.pack(fill=BOTH, expand=True)
    
    # Khởi tạo vẽ bản đồ trắng và nạp dữ liệu Treeview
    tree_items.clear()
    draw_blank_map()

def draw_blank_map():
    global csp_canvas, csp_tree, tree_items, polygon_ids, node_positions
    if not csp_canvas or not csp_tree:
        return
    csp_canvas.delete("all")
    polygon_ids = {}

    # --- Vẽ các cạnh ràng buộc trước (nền) ---
    drawn_edges = set()
    for area, neighbors in constrain.items():
        if area not in node_positions:
            continue
        x1, y1 = node_positions[area]
        for nb in neighbors:
            if nb not in node_positions:
                continue
            edge_key = tuple(sorted([area, nb]))
            if edge_key in drawn_edges:
                continue
            drawn_edges.add(edge_key)
            x2, y2 = node_positions[nb]
            csp_canvas.create_line(x1, y1, x2, y2, fill="#B0BEC5", width=1.5)

    # --- Vẽ các node (hình tròn) ---
    for area, (cx, cy) in node_positions.items():
        r = NODE_RADIUS
        node_id = csp_canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#ECEFF1", outline="#37474F", width=2
        )
        polygon_ids[area] = node_id
        # Label bên trong node
        short = area.replace("Quận ", "Q.").replace("Huyện ", "H.")
        display = short.replace(" ", "\n") if len(short) > 6 else short
        csp_canvas.create_text(cx, cy, text=display, font=("Arial", 7, "bold"),
                               fill="#1A237E", justify="center")

    # --- Đổ dữ liệu tĩnh vào bảng trạng thái ---
    for item in csp_tree.get_children():
        csp_tree.delete(item)
    for area in variables:
        item_id = csp_tree.insert("", END, values=(area, "Chưa tô"))
        tree_items[area] = item_id

def run_csp():
    algo = selected_csp_algo.get()
    if algo == "Backtracking":
        run_csp_backtracking()
    elif algo == "Forward Checking":
        run_csp_forward_checking()
    elif algo == "AC3":
        run_csp_ac3()
    elif algo == "Min-Conflicts":
        run_csp_min_conflicts()

def color_node(area, fill_color):
    """Tô màu node trên đồ thị ràng buộc và vẽ lại nhãn lên trên."""
    global csp_canvas, polygon_ids, node_positions
    if not csp_canvas or area not in polygon_ids or area not in node_positions:
        return
    csp_canvas.itemconfig(polygon_ids[area], fill=fill_color)
    cx, cy = node_positions[area]
    short = area.replace("Quận ", "Q.").replace("Huyện ", "H.")
    display = short.replace(" ", "\n") if len(short) > 6 else short
    # Xác định màu chữ tương phản
    text_color = "#FFFFFF" if fill_color not in ("#ECEFF1", "#FAFAFA") else "#1A237E"
    csp_canvas.create_text(cx, cy, text=display, font=("Arial", 7, "bold"),
                           fill=text_color, justify="center")

def run_csp_backtracking():
    global stop_execution, result, speed_scale
    stop_execution = False
    
    result.clear()
    draw_blank_map()
    window.update()
    
    def is_valid(area, color):
        for neighbor in constrain[area]:
            if neighbor in result and result[neighbor] == color:
                return False
        return True

    def backtrack(index):
        if stop_execution:
            return False
            
        if index == len(variables):
            return True
            
        area = variables[index]
        
        for color in colors:
            if stop_execution:
                return False
                
            if is_valid(area, color):
                result[area] = color
                print(f"Tô màu {color} cho {area}", flush=True)
                
                # Cập nhật GUI
                if csp_canvas and csp_tree:
                    color_node(area, colors_hex[color])
                    csp_tree.item(tree_items[area], values=(area, color))
                window.update()
                time.sleep(speed_scale.get())
                
                if backtrack(index + 1):
                    return True
                    
                print(f"Backtrack {area} (bỏ màu {color} vì không phù hợp ràng buộc)", flush=True)
                if area in result:
                    del result[area]
                    
                # Cập nhật GUI khi Backtrack
                if csp_canvas and csp_tree:
                    color_node(area, "#ECEFF1")
                    csp_tree.item(tree_items[area], values=(area, "Chưa tô"))
                window.update()
                time.sleep(speed_scale.get())
                
        return False

    print("----- CHẠY CSP BACKTRACKING -----", flush=True)
    if backtrack(0):
        print("Kết quả cuối cùng:", flush=True)
        for area, color in result.items():
            print(f"{area}: {color}", flush=True)
    else:
        print("Không thể tô màu hoặc đã bị dừng.", flush=True)


def run_csp_forward_checking():
    global stop_execution, result, speed_scale
    stop_execution = False
    
    result.clear()
    assigned_areas = set()
    domains = {area: list(colors) for area in constrain.keys()}
    draw_blank_map()
    window.update()

    def forward_checking_func(area, color, assigned):
        removals = []
        for neighbor in constrain[area]:
            if neighbor not in assigned:
                if color in domains[neighbor]:
                    domains[neighbor].remove(color)
                    removals.append((neighbor, color))
                    if not domains[neighbor]:
                        return False, removals
            else:
                if result.get(neighbor) == color:
                    return False, removals
        return True, removals

    def backtrack_fc(index):
        if stop_execution:
            return False
            
        if index == len(variables):
            return True
            
        area = variables[index]
        
        for color in list(domains[area]):
            if stop_execution:
                return False
                
            result[area] = color
            assigned_areas.add(area)
            print(f"Thử tô màu {color} cho {area}", flush=True)
            
            # Cập nhật GUI
            if csp_canvas and csp_tree:
                color_node(area, colors_hex[color])
                csp_tree.item(tree_items[area], values=(area, color))
            window.update()
            time.sleep(speed_scale.get())
            
            success, removals = forward_checking_func(area, color, assigned_areas)
            
            if success:
                if backtrack_fc(index + 1):
                    return True
                
                print(f"-> Nhánh sau thất bại. Backtrack {area}, khôi phục domain...", flush=True)
                for neighbor, removed_color in removals:
                    domains[neighbor].append(removed_color)
            else:
                for neighbor, removed_color in removals:
                    domains[neighbor].append(removed_color)
                    
            # Backtrack visual update
            if area in result:
                del result[area]
            assigned_areas.discard(area)
            
            if csp_canvas and csp_tree:
                color_node(area, "#ECEFF1")
                csp_tree.item(tree_items[area], values=(area, "Chưa tô"))
            window.update()
            time.sleep(speed_scale.get())
            
        return False

    print("----- CHẠY CSP FORWARD CHECKING -----", flush=True)
    if backtrack_fc(0):
        print("Kết quả cuối cùng:", flush=True)
        for area, color in result.items():
            print(f"{area}: {color}", flush=True)
    else:
        print("Không thể tô màu hoặc đã bị dừng.", flush=True)

def run_csp_ac3():
    global stop_execution, result, speed_scale
    stop_execution = False
    
    result.clear()
    assigned_areas = set()
    domains = {area: list(colors) for area in constrain.keys()}
    draw_blank_map()
    window.update()

    def ac3(assigned_area, assigned_color):
        queue = []
        for neighbor in constrain[assigned_area]:
            if neighbor not in assigned_areas:
                queue.append((neighbor, assigned_area))
        
        removals = []
        while queue:
            if stop_execution:
                return False, removals
            
            xi, xj = queue.pop(0)
            revised, removed_colors = revise(xi, xj)
            if revised:
                removals.extend([(xi, c) for c in removed_colors])
                if not domains[xi]:
                    return False, removals
                for neighbor in constrain[xi]:
                    if neighbor != xj and neighbor not in assigned_areas:
                        queue.append((neighbor, xi))
        return True, removals

    def revise(xi, xj):
        revised = False
        removed_colors = []
        for x_color in list(domains[xi]):
            xj_domain = [result[xj]] if xj in assigned_areas else domains[xj]
            has_support = any(y_color != x_color for y_color in xj_domain)
            if not has_support:
                domains[xi].remove(x_color)
                removed_colors.append(x_color)
                revised = True
        return revised, removed_colors

    def backtrack_ac3(index):
        if stop_execution:
            return False
            
        if index == len(variables):
            return True
            
        area = variables[index]
        
        for color in list(domains[area]):
            if stop_execution:
                return False
                
            result[area] = color
            assigned_areas.add(area)
            
            old_domains = {v: list(d) for v, d in domains.items()}
            domains[area] = [color]
            
            print(f"Thử tô màu {color} cho {area} (AC-3)", flush=True)
            
            if csp_canvas and csp_tree:
                color_node(area, colors_hex[color])
                csp_tree.item(tree_items[area], values=(area, color))
            window.update()
            time.sleep(speed_scale.get())
            
            success, removals = ac3(area, color)
            
            if success:
                if backtrack_ac3(index + 1):
                    return True
                print(f"-> Nhánh sau thất bại. Backtrack {area}, khôi phục domains...", flush=True)
            
            for v, d in old_domains.items():
                domains[v] = d
                
            if area in result:
                del result[area]
            assigned_areas.discard(area)
            
            if csp_canvas and csp_tree:
                color_node(area, "#ECEFF1")
                csp_tree.item(tree_items[area], values=(area, "Chưa tô"))
            window.update()
            time.sleep(speed_scale.get())
            
        return False

    print("----- CHẠY CSP AC-3 -----", flush=True)
    if backtrack_ac3(0):
        print("Kết quả cuối cùng:", flush=True)
        for area, color in result.items():
            print(f"{area}: {color}", flush=True)
    else:
        print("Không thể tô màu hoặc đã bị dừng.", flush=True)

def run_csp_min_conflicts():
    global stop_execution, result, speed_scale
    stop_execution = False
    
    result.clear()
    draw_blank_map()
    window.update()
    
    for area in variables:
        color = random.choice(colors)
        result[area] = color
        if csp_canvas and csp_tree:
            color_node(area, colors_hex[color])
            csp_tree.item(tree_items[area], values=(area, color))
    window.update()
    time.sleep(speed_scale.get())
    
    def get_conflicted_variables():
        conflicted = []
        for area in variables:
            current_color = result[area]
            for neighbor in constrain[area]:
                if result.get(neighbor) == current_color:
                    conflicted.append(area)
                    break
        return conflicted

    def count_conflicts(area, color):
        count = 0
        for neighbor in constrain[area]:
            if result.get(neighbor) == color:
                count += 1
        return count

    max_steps = 200
    print("----- CHẠY CSP MIN-CONFLICTS -----", flush=True)
    
    for step in range(max_steps):
        if stop_execution:
            print("Đã bị dừng.", flush=True)
            return
            
        conflicted_vars = get_conflicted_variables()
        if not conflicted_vars:
            print(f"Tìm thấy lời giải sau {step} bước!", flush=True)
            print("Kết quả cuối cùng:", flush=True)
            for area, color in result.items():
                print(f"{area}: {color}", flush=True)
            return
            
        var = random.choice(conflicted_vars)
        
        best_colors = []
        min_conflict = float('inf')
        
        for color in colors:
            conflict_count = count_conflicts(var, color)
            if conflict_count < min_conflict:
                min_conflict = conflict_count
                best_colors = [color]
            elif conflict_count == min_conflict:
                best_colors.append(color)
                
        chosen_color = random.choice(best_colors)
        
        if result[var] != chosen_color:
            result[var] = chosen_color
            print(f"Bước {step+1}: Đổi màu {var} thành {chosen_color} (xung đột tối thiểu = {min_conflict})", flush=True)
            
            if csp_canvas and csp_tree:
                color_node(var, colors_hex[chosen_color])
                csp_tree.item(tree_items[var], values=(var, chosen_color))
            window.update()
            time.sleep(speed_scale.get() * 1.5)
            
    print("Không tìm thấy lời giải sau số bước tối đa.", flush=True)

def show_adversarial_visualizer():
    global text_area, solution_text, cells, current_group, selected_adversarial_algo
    current_group = "adversarial"
    reset_view()
    
    # Sidebar
    but_frame = Frame(window, bg="cyan")
    but_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    Label(
        but_frame,
        text="Adversarial Search",
        font=("Times New Roman", 14, "bold"),
        bg="cyan"
    ).pack(pady=10)
    
    algos = [
        ("Minimax", "Minimax"),
        ("Alpha-Beta", "Alpha-Beta"),
        ("Expectimax", "Expectimax")
    ]
    
    for display_name, value_name in algos:
        Radiobutton(
            but_frame,
            text=display_name,
            variable=selected_adversarial_algo,
            value=value_name,
            font=("Times New Roman", 10, "bold"),
            bg="cyan",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
    bottom_btn_frame = Frame(but_frame, bg="cyan")
    bottom_btn_frame.pack(side="bottom", fill="x", pady=5)
    
    Button(bottom_btn_frame, text="RUN", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=run_adversarial).pack(pady=5)
    Button(bottom_btn_frame, text="STOP", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=trigger_stop).pack(pady=5)
    Button(bottom_btn_frame, text="EXIT", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=exit_visualizer).pack(pady=5)
    
    # Grid Container in the middle
    frame = Frame(window)
    frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    for r in range(3):
        frame.rowconfigure(r, weight=1)
        frame.columnconfigure(r, weight=1)
        
    cells = []
    for row in range(3):
        temp = []
        for col in range(3):
            cell = Frame(frame, width=110, height=110, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            
            lbl = Label(cell, text="", font=("Arial", 36, "bold"), bg="white", fg="black")
            lbl.pack(fill=BOTH, expand=True)
            lbl.bind("<Button-1>", lambda e, r=row, c=col: cell_clicked(r, c))
            temp.append(lbl)
        cells.append(temp)
        
    # Log area on the right
    text_area = Text(window, width=40, height=18, relief=RAISED, font=("Segoe UI", 11), bg="black", fg="white")
    text_area.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    
    # Solution path at the bottom
    solution_text = Text(window, width=88, height=9, relief=RAISED, font=("Segoe UI", 11))
    solution_text.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    reset_adversarial_ui()

def run_adversarial():
    global stop_execution, adversarial_nodes, adversarial_board
    stop_execution = False
    adversarial_nodes = 0
    
    solution_text.delete(1.0, END)
    text_area.delete(1.0, END)
    
    board_copy = [r[:] for r in adversarial_board]
    algo = selected_adversarial_algo.get()
    
    text_area.insert(END, f"TRẠNG THÁI TIẾN TRÌNH ĐỐI KHÁNG: {algo}\n")
    text_area.insert(END, "ĐANG TÍNH TOÁN CÁC BƯỚC ĐI TỐI ƯU...\n")
    window.update()
    
    winner = check_winner(board_copy)
    if winner:
        text_area.insert(END, f"Trò chơi đã kết thúc! Người thắng: {winner}\n")
        return
    if len(find_blank(board_copy)) == 0:
        text_area.insert(END, "Trò chơi hòa!\n")
        return
        
    start_player = current_player(board_copy)
    text_area.insert(END, f"Lượt hiện tại: Người chơi {start_player}\n")
    window.update()
    
    value = 0
    best_path = []
    if algo == "Minimax":
        value, best_path = minimax(board_copy)
    elif algo == "Alpha-Beta":
        value, best_path = alphabeta(board_copy, -float('inf'), float('inf'))
    elif algo == "Expectimax":
        value, best_path = expectimax(board_copy)
        
    text_area.insert(END, f"Tổng số trạng thái đã duyệt (nodes): {adversarial_nodes}\n")
    if algo == "Expectimax":
        text_area.insert(END, f"Điểm mong đợi (Expected Utility): {value:.3f}\n\n")
    else:
        text_area.insert(END, f"Điểm số tối ưu (Utility): {value}\n\n")
    
    if not best_path:
        text_area.insert(END, "Không tìm thấy đường đi/nước đi nào tiếp theo!\n")
        solution_text.insert(END, "NO SOLUTION")
        return
        
    text_area.insert(END, "MÔ PHỎNG NƯỚC ĐI TỐI ƯU:\n")
    solution_str = "SOLUTION: "
    
    curr_board = [r[:] for r in board_copy]
    draw_board_state_to_grid(curr_board)
    window.update()
    time.sleep(0.5)
    
    for idx, move in enumerate(best_path):
        if stop_execution:
            text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
            return
            
        player = current_player(curr_board)
        curr_board[move[0]][move[1]] = player
        draw_board_state_to_grid(curr_board)
        
        text_area.insert(END, f"Bước {idx+1}: {player} đi vào ({move[0]}, {move[1]})\n")
        window.update()
        
        solution_str += f"{player}({move[0]},{move[1]}) --> "
        solution_text.insert(END, f"Bước {idx+1}: {player} tại ({move[0]}, {move[1]})\n")
        
        board_str = "\n".join([f"| {' | '.join([cell if cell != '' else ' ' for cell in row])} |" for row in curr_board])
        solution_text.insert(END, board_str + "\n\n")
        
        w = check_winner(curr_board)
        if w:
            text_area.insert(END, f"\nNgười chiến thắng: {w}!\n")
            break
            
        time.sleep(0.8)
        
    solution_text.insert(END, solution_str[:-5] if solution_str.endswith(" --> ") else solution_str)

def draw_board_state_to_grid(board):
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            lbl = cells[r][c]
            lbl.config(text=val)
            if val == 'X':
                lbl.config(fg='#FF5733')
            elif val == 'O':
                lbl.config(fg='#3498DB')
            else:
                lbl.config(fg='black')

def main():
    global solution_text, text_area, window, cells, cells2, selected_algo, selected_blind_algo, selected_csp_algo, selected_adversarial_algo, current_group

    window = Tk()
    window.config(bg="#eaeaea")
    window.title("Visualizer")
    window.geometry("1100x850")
    window.minsize(850, 550)

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=0)

    window.columnconfigure(0, weight=0)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)

    cells = []
    cells2 = []
    selected_algo = StringVar(value="BFS_1")
    selected_blind_algo = StringVar(value="Mù Start")
    selected_csp_algo = StringVar(value="Backtracking")
    selected_adversarial_algo = StringVar(value="Minimax")
    selected_algo.trace_add("write", on_algo_change)
    selected_blind_algo.trace_add("write", on_blind_algo_change)
    selected_csp_algo.trace_add("write", on_csp_algo_change)
    selected_adversarial_algo.trace_add("write", on_adversarial_algo_change)
    current_group = "menu"

    show_menu()
    window.mainloop()
# === Cell 4 ===
def create_mat():
    
    new_mat = np.array([
        ['1', '1', '1', '0'],
        ['0', '0', 'x', '1'],
        ['1', '1', '0', '0'],
        ['1', '1', '0', '1']
    ])
    
    row, col = find_vacuum(new_mat)
    
    return new_mat, row, col
# === Cell 5 ===
def find_vacuum(matrix):
    pos = np.argwhere(matrix == 'x')[0]
    
    return pos[0], pos[1]
# === Cell 6 ===
def moves(matrix):
    
    lst_move = []
    row, col = find_vacuum(matrix)
    
    directions = [
        ['LEFT', 0, -1],
        ['RIGHT', 0, 1],
        ['UP', -1, 0],
        ['DOWN', 1, 0]
    ]
    
    for dir, x, y in directions:
        row_new = row + x
        col_new = col + y
        
        if row_new < 4 and row_new >= 0 and col_new < 4 and col_new >= 0:
            lst_move.append([dir, row_new, col_new])
            
    return lst_move
# === Cell 7 ===
def solution(node):
    path = []
    
    while node.parent is not None:
        path.append((node.action, node.state))
        
        node = node.parent
    
    path.reverse()
    
    return path
# === Cell 8 ===
def bfs_1(matrix, row, col):
        
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, 0)      
    
    frontier = []
    frontier_state = []
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
    
    frontier.append(node)
    frontier_state.append(tuple(map(tuple, node.state)))
    
    reached = []
    
    while len(frontier) != 0:
        
        node = frontier.pop(0)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in reached:
            reached.append(temp_mat)
        
        if '1' not in node.state:
            solutions = solution(node)
            for action, state in solutions:
                print("HUONG DI: ", action)
                print(state)
            print("DA HOAN THANH!!!")
            return solutions, reached
        
        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, node.cost + 1)
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) and (new_node not in reached):
                frontier_state.append(new_node)
                frontier.append(child)
                
    return None, None
# === Cell 9 ===
def BFS_1():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = bfs_1(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    '''    
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 10 ===
def bfs_2(matrix, row, col):
    
    matrix[row, col] = 'x'
    
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, 0)    
    
    frontier = []
    frontier_state = []
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
    
    frontier.append(node)
    frontier_state.append(tuple(map(tuple, node.state)))
    
    explored = []
    
    while len(frontier) != 0:
        
        node = frontier.pop(0)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in explored:
            explored.append(temp_mat)

        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, node.cost + 1)
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) and (new_node not in explored):
                if '1' not in child.state:
                    solutions = solution(child)
                    for action, state in solutions:
                        print("HUONG DI: ", action)
                        print(state)
                    print("DA HOAN THANH!!!")
                    return solutions, explored
                frontier.append(child)
                frontier_state.append(new_node)
                
    return None, None
# === Cell 11 ===
def BFS_2():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = bfs_2(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    '''    
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 12 ===
def dfs_1(matrix, row, col):
    
    matrix[row, col] = 'x'
    
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, 0)    
    
    frontier = []
    frontier_state = []
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
     
    frontier.append(node)
    frontier_state.append(tuple(map(tuple, node.state)))
    
    reached = []
    
    while len(frontier) != 0:
        
        node = frontier.pop(len(frontier) - 1)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in reached:
            reached.append(temp_mat)
        
        if '1' not in node.state:
            solutions = solution(node)
            for action, state in solutions:
                print("HUONG DI: ", action)
                print(state)
            print("DA HOAN THANH!!!")
            return solutions, reached
        
        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, node.cost + 1)
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) and (new_node not in reached):
                frontier_state.append(new_node)
                frontier.append(child)
    return None, None
# === Cell 13 ===
def DFS_1():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = dfs_1(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.2)
    '''    
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 14 ===
def dfs_2(matrix, row, col):
    
    matrix[row, col] = 'x'
    
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, 0)    
    
    frontier = []
    frontier_state = []
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
    
    frontier.append(node)
    frontier_state.append(tuple(map(tuple, node.state)))
    
    explored = []
    
    while len(frontier) != 0:
        
        node = frontier.pop(len(frontier) - 1)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in explored:
            explored.append(temp_mat)

        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, node.cost + 1)
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) and (new_node not in explored):
                if '1' not in child.state:
                    solutions = solution(child)
                    for action, state in solutions:
                        print("HUONG DI: ", action)
                        print(state)
                    print("DA HOAN THANH!!!")
                    return solutions, explored
                frontier.append(child)
                frontier_state.append(new_node)
                
    return None, None
# === Cell 15 ===
def DFS_2():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = dfs_2(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.2)
    '''    
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 16 ===
def ids_1(matrix, row, col):
    for i in range(0, 1000):
        result, reached = depth_limited_search(matrix, row, col, i)
        
        if result is not None:
            
            return result, reached
        
    return None, None
# === Cell 17 ===
def depth_limited_search(matrix, row, col, limit):

    matrix = matrix.copy()
    matrix[row, col] = 'x'

    node = Node(matrix, None, None, 0)

    frontier = [node]
    frontier_state = [tuple(map(tuple, node.state))]

    reached = []

    while len(frontier) != 0:

        node = frontier.pop(len(frontier) - 1)

        temp_mat = tuple(map(tuple, node.state))

        if temp_mat not in reached:
            reached.append(temp_mat)

        if '1' not in node.state:

            solutions = solution(node)

            print("TIM THAY LOI GIAI !!!")

            for action, state in solutions:
                print("HUONG DI:", action)
                print(state)

            return solutions, reached

        if node.cost >= limit:
            continue

        actions = moves(node.state)

        row, col = find_vacuum(node.state)

        for dir, x, y in actions:

            new_node = node.state.copy()

            new_node[row, col], new_node[x, y] = '0', 'x'

            child = Node(new_node, node, dir, node.cost + 1)

            temp_child = tuple(map(tuple, new_node))

            if (temp_child not in frontier_state) and (temp_child not in reached):

                frontier_state.append(temp_child)

                frontier.append(child)

    return None, reached
# === Cell 18 ===
def IDS_1():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = ids_1(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    '''  
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 19 ===
def ids_2(matrix, row, col):
    for i in range(0, 1000):
        result, reached = depth_limited_search(matrix, row, col, i)
        
        if result is not None:
            
            return result, reached
        
    return None, None
# === Cell 20 ===
def depth_limited_search(matrix, row, col, limit):

    matrix = matrix.copy()
    matrix[row, col] = 'x'

    node = Node(matrix, None, None, 0)

    frontier = [node]
    frontier_state = [tuple(map(tuple, node.state))]

    reached = []

    while len(frontier) != 0:

        node = frontier.pop(len(frontier) - 1)

        temp_mat = tuple(map(tuple, node.state))

        if temp_mat not in reached:
            reached.append(temp_mat)

        if '1' not in node.state:

            solutions = solution(node)

            print("TIM THAY LOI GIAI !!!")

            for action, state in solutions:
                print("HUONG DI:", action)
                print(state)

            return solutions, reached

        if node.cost >= limit:
            continue

        actions = moves(node.state)

        row, col = find_vacuum(node.state)

        for dir, x, y in actions:

            new_node = node.state.copy()

            new_node[row, col], new_node[x, y] = '0', 'x'

            child = Node(new_node, node, dir, node.cost + 1)

            temp_child = tuple(map(tuple, new_node))

            if (temp_child not in frontier_state) and (temp_child not in reached):
                if '1' not in child.state:
                    solutions = solution(child)
                    for action, state in solutions:
                        print("HUONG DI: ", action)
                        print(state)
                    print("DA HOAN THANH!!!")
                    return solutions, reached
                frontier_state.append(temp_child)
                frontier.append(child)

    return None, reached
# === Cell 21 ===
def IDS_2():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = ids_2(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    '''    
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 22 ===
def count_clean_position(matrix):
    count = 0
    for x in range(4):
        for y in range(4):
            if matrix[x][y] == '0':
                count += 1
    return count

def priority_pop(frontier):
    best_cost = 0
    for x in frontier:
        if x.cost > best_cost:
            best_cost = x.cost
            best_node = x
            
    return best_node
# === Cell 23 ===
def ucs(matrix, row, col):
        
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, count_clean_position(matrix))      
    
    frontier = []
    frontier_state = {}
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
    
    frontier.append(node)
    frontier_state[tuple(map(tuple, node.state))] = node.cost
    
    reached = {}
    
    while len(frontier) != 0:
        
        node = priority_pop(frontier)
        frontier.remove(node)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in reached:
            reached[temp_mat] = node.cost
        
        if '1' not in node.state:
            solutions = solution(node)
            for action, state in solutions:
                print("HUONG DI: ", action)
                print(state)
            print("DA HOAN THANH!!!")
            return solutions, reached
        
        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, node.cost + count_clean_position(new_node))
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) or (child.cost < frontier_state[new_node]):
                if (new_node not in reached) or (child.cost < reached[new_node]):

                    if new_node in frontier_state:

                        old_node = frontier_state[new_node]

                        frontier.remove(old_node)
                        del frontier_state[new_node]

                frontier_state[new_node] = child.cost
                frontier.append(child)
                
    return None, None
# === Cell 24 ===
def UCS():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = ucs(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
#    text_area.insert(END, "SEARCHING TIME... \n")
    
#    for reach in reached:
        
#        reach = np.array(reach)
        
#        draw_state(reach)
        
#        window.update()
#        time.sleep(0.08)
        
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 25 ===
def count_dirty_position(matrix):
    count = 0
    for x in range(4):
        for y in range(4):
            if matrix[x][y] == '1':
                count += 1
    return count

def priority_pop(frontier):
    best_cost = 99999999999
    for x in frontier:
        if x.cost < best_cost:
            best_cost = x.cost
            node = x
            
    return node
# === Cell 26 ===
def greedy(matrix, row, col):
        
    print("TRANG THAI BAN DAU")
    print(matrix)
    
    node = Node(matrix, None, None, count_dirty_position(matrix))      
    
    frontier = []
    frontier_state = {}
    
    if '1' not in node.state:
        solutions = solution(node)
        for action, state in solutions:
            print("HUONG DI: ", action)
            print(state)
        print("DA HOAN THANH!!!")
        return node, None
    
    frontier.append(node)
    frontier_state[tuple(map(tuple, node.state))] = node.cost
    
    reached = {}
    
    while len(frontier) != 0:
        
        node = priority_pop(frontier)
        frontier.remove(node)
        
        temp_mat = node.state.copy()
        temp_mat = tuple(map(tuple, temp_mat))
        
        if temp_mat not in reached:
            reached[temp_mat] = node.cost
        
        if '1' not in node.state:
            solutions = solution(node)
            for action, state in solutions:
                print("HUONG DI: ", action)
                print(state)
            print("DA HOAN THANH!!!")
            return solutions, reached
        
        actions = moves(node.state)
        row, col = find_vacuum(node.state)
        
        for dir, x, y in actions:
            
            new_node = node.state.copy()
            
            new_node[row, col], new_node[x, y] = '0', 'x' 
            child = Node(new_node, node, dir, count_dirty_position(new_node))
            
            new_node = tuple(map(tuple, new_node))
            if (new_node not in frontier_state) or (child.cost < frontier_state[new_node]):
                if (new_node not in reached) or (child.cost < reached[new_node]):

                    if new_node in frontier_state:

                        old_node = frontier_state[new_node]

                        frontier.remove(old_node)
                        del frontier_state[new_node]

                frontier_state[new_node] = child.cost
                frontier.append(child)
                
    return None, None
# === Cell 27 ===
def Greedy():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = greedy(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    ''' 
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 28 ===
class Node_A():
    
    def __init__(self, state, parent, action, g, h):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.h = h
# === Cell 29 ===
def distance_to_dirty_cell(matrix, row, col):
    dis = 0
    for i in range(0, 4):
        for j in range(0, 4):
            if matrix[i, j] == '1':
                dis += abs(row - i) + abs(col - j)
    
    return dis

def count_dirty_position(matrix):
    count = 0
    for x in range(4):
        for y in range(4):
            if matrix[x][y] == '1':
                count += 1
    return count

def priority_pop_a(frontier):
    frontier.sort(key=lambda x: x.g + x.h)
    return frontier[0]
# === Cell 30 ===
def a_star(matrix, row, col):

    print("TRANG THAI BAN DAU")
    print(matrix)


    g = count_dirty_position(matrix)
    h = distance_to_dirty_cell(matrix, row, col)

    node = Node_A(matrix, None, None, g, h)

    frontier = [node]

    frontier_state = {}

    temp_start = tuple(map(tuple, matrix))
    frontier_state[temp_start] = g + h

    reached = {}

    while len(frontier) != 0:

        node = priority_pop_a(frontier)
        frontier.remove(node)

        temp_mat = tuple(map(tuple, node.state))

        reached[temp_mat] = node.g + node.h

        if '1' not in node.state:

            solutions = solution(node)

            print("TIM THAY LOI GIAI !!!")

            for action, state in solutions:
                print("HUONG DI:", action)
                print(state)

            return solutions, reached

        row, col = find_vacuum(node.state)

        actions = moves(node.state)

        for dir, x, y in actions:

            new_node = node.state.copy()

            new_node[row][col], new_node[x][y] = '0', 'x'

            temp_node = tuple(map(tuple, new_node))

            g_new = count_dirty_position(new_node)
            h_new = distance_to_dirty_cell(new_node, x, y)

            f_new = g_new + h_new

            if temp_node in reached:

                if f_new >= reached[temp_node]:
                    continue

                else:
                    reached[temp_node] = f_new

            if temp_node in frontier_state:

                if f_new < frontier_state[temp_node]:
                    for i in range(len(frontier)):
                        state = tuple(map(tuple, frontier[i].state))
                        if state == temp_node:

                            frontier[i].g = g_new
                            frontier[i].h = h_new
                            frontier[i].parent = node
                            frontier[i].action = dir

                            frontier_state[temp_node] = f_new
                            break
                else:
                    continue

            if temp_node not in frontier_state and temp_node not in reached:
                child = Node_A(new_node, node, dir, g_new, h_new)

                frontier.append(child)
                frontier_state[temp_node] = f_new

    print("KHONG TIM THAY LOI GIAI")

    return None  
# === Cell 31 ===
def A_star():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = a_star(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    ''' 
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 32 ===
def draw_state(state):
    for i in range(4):
        for j in range(4):
            value = state[i][j]
            if value == '1':
                cells[i][j].config(bg='red')
            elif value == '0':
                cells[i][j].config(bg='light green')
            elif value == 'x':
                cells[i][j].config(bg='yellow')
# === Cell 33 ===
def ida_star(matrix, row, col):

    print("TRANG THAI BAN DAU")
    print(matrix)

    g = count_dirty_position(matrix)
    h = distance_to_dirty_cell(matrix, row, col)

    cost = g + h

    while True:

        result, reached, next_cost = depth_limited_search_ida(matrix, row, col, cost)

        if result is not None:
            return result, reached

        if next_cost == math.inf:

            print("KHONG TIM THAY LOI GIAI")
            return None, reached

        cost = next_cost

        print(f"TANG cost LEN: {cost}")
# === Cell 34 ===
def depth_limited_search_ida(matrix, row, col, cost):

    matrix = matrix.copy()

    matrix[row, col] = 'x'

    g = count_dirty_position(matrix)
    h = distance_to_dirty_cell(matrix, row, col)

    node = Node_A(matrix, None, None, g, h)

    frontier = [node]
    frontier_state = {}
    temp_start = tuple(map(tuple, node.state))
    frontier_state[temp_start] = g + h
    reached = {}
    next_cost = math.inf

    while len(frontier) != 0:

        node = frontier.pop(len(frontier) - 1)

        temp_mat = tuple(map(tuple, node.state))

        frontier_state.pop(temp_mat, None)

        f = node.g + node.h

        if f > cost:

            next_cost = min(next_cost, f)
            continue

        reached[temp_mat] = f

        if '1' not in node.state:
            solutions = solution(node)
            print("TIM THAY LOI GIAI !!!")
            for action, state in solutions:
                print("HUONG DI:", action)
                print(state)
            return solutions, reached, next_cost
        actions = moves(node.state)
        row, col = find_vacuum(node.state)

        for dir, x, y in actions:

            new_node = node.state.copy()
            new_node[row, col], new_node[x, y] = '0', 'x'
            temp_node = tuple(map(tuple, new_node))

            g_new = count_dirty_position(new_node)
            h_new = distance_to_dirty_cell(new_node, x, y)

            f_new = g_new + h_new

            if temp_node in reached:
                if f_new >= reached[temp_node]:
                    continue

                else:
                    reached[temp_node] = f_new

            if temp_node in frontier_state:

                if f_new < frontier_state[temp_node]:
                    for i in range(len(frontier)):
                        state = tuple(map(tuple, frontier[i].state))
                        if state == temp_node:

                            frontier[i].g = g_new
                            frontier[i].h = h_new
                            frontier[i].parent = node
                            frontier[i].action = dir

                            frontier_state[temp_node] = f_new
                            break
                else:
                    continue

            if f_new > cost:
                next_cost = min(next_cost, f_new)
                continue

            if temp_node not in frontier_state and temp_node not in reached:
                child = Node_A(new_node, node, dir, g_new, h_new)
                frontier.append(child)
                frontier_state[temp_node] = f_new

    return None, reached, next_cost
# === Cell 35 ===
def IDA_STAR():
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, reached = ida_star(matrix, row, col)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    ''' 
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = node[1][i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 36 ===
def simple_hill_climbing(matrix, row, col):

    cur_state = matrix.copy()
    visited_states = []

    while True:
        
        visited_states.append(cur_state.copy())
        h = count_dirty_position(cur_state)
        if h == 0:
            print("Nha da sach")
            return visited_states, "TIM THAY LOI GIAI"

        print("Trang thai cha:")
        print(cur_state)
        print(f"h = {h}\n")

        lst_move = moves(cur_state)

        found_better = False

        for dir, x, y in lst_move:

            next_state = cur_state.copy()

            next_state[row][col] = '0'
            next_state[x][y] = 'x'

            h_new = count_dirty_position(next_state)

            print(next_state)
            print(f"h = {h_new}\n")

            if h_new < h:
                cur_state = next_state
                row, col = x, y
                found_better = True
                break

        if not found_better:

            print("Khong ton tai!")

            return visited_states, "KHONG TON TAI LOI GIAI"
# === Cell 37 ===
def Simple_hill():

    solution_text.delete(1.0, END)

    text_area.delete(1.0, END)

    matrix, row, col = create_mat()

    result, message = simple_hill_climbing(matrix, row, col)

    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")

    text_area.insert(END, "SEARCHING TIME... \n")
    
    for node in result:

        for i in range(4):
            for j in range(4):

                value = node[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')

        window.update()

        solution_text.insert(END, str(node))
        solution_text.insert(END, "\n\n")

        time.sleep(0.8)

    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHONG TON TAI LOI GIAI!\n")

        solution_text.insert(END, "NO SOLUTION")
        return

    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI\n")

    solution_text.insert(END, "SOLUTION: ")

    for action, state in result[1:]:
        solution_text.insert(END, action + " ")

    solution_text.insert(END, "\n")
# === Cell 38 ===
def steepest_ascent(matrix, row, col):

    cur_state = matrix.copy()

    visited_states = []

    while True:

        visited_states.append(("START", cur_state.copy()))
        h = count_dirty_position(cur_state)

        if h == 0:
            print("Nha da sach")
            return visited_states, "TIM THAY LOI GIAI"

        print("Trang thai cha:")
        print(cur_state)
        print(f"h = {h}\n")

        lst_move = moves(cur_state)
        best_h = h
        best_states = []
        print("Cac trang thai con:")

        for dir, x, y in lst_move:
            next_state = cur_state.copy()
            next_state[row][col] = '0'
            next_state[x][y] = 'x'

            h_new = count_dirty_position(next_state)

            print(next_state)
            print(f"h = {h_new}\n")

            if h_new < best_h:
                best_h = h_new
                best_states = [(dir, next_state, x, y)]

            elif h_new == best_h and h_new < h:
                best_states.append((dir, next_state, x, y))

        if len(best_states) == 0:
            print("Khong ton tai cach giai!!!")
            return visited_states, "KHONG TON TAI LOI GIAI"
        chosen = random.choice(best_states)

        visited_states.append(
            (chosen[0], chosen[1].copy())
        )

        cur_state = chosen[1]

        row = chosen[2]
        col = chosen[3]
# === Cell 39 ===
def Steepest_Ascent():

    solution_text.delete(1.0, END)

    text_area.delete(1.0, END)

    matrix, row, col = create_mat()

    result, message = steepest_ascent(matrix, row, col)

    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")

    text_area.insert(END, "SEARCHING TIME... \n")
    
    for node in result:

        for i in range(4):
            for j in range(4):

                value = node[1][i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')

        window.update()

        solution_text.insert(END, str(node))
        solution_text.insert(END, "\n\n")

        time.sleep(0.8)

    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHONG TON TAI LOI GIAI!\n")

        solution_text.insert(END, "NO SOLUTION")
        return

    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI\n")

    solution_text.insert(END, "SOLUTION: ")

    for action, state in result[1:]:
        solution_text.insert(END, action + " ")

    solution_text.insert(END, "\n")
# === Cell 40 ===
def stochastic(matrix, row, col):

    cur_state = matrix.copy()

    visited_states = []

    while True:

        h = count_dirty_position(cur_state)
        visited_states.append(("START", cur_state.copy()))

        if h == 0:
            print("Nha da sach!!!")
            return visited_states, "TIM THAY LOI GIAI"

        print("Trang thai cha:")
        print(cur_state)
        print(f"h = {h}\n")
        lst_move = moves(cur_state)
        better_states = []
        print("Cac trang thai con:")

        for dir, x, y in lst_move:

            next_state = cur_state.copy()
            next_state[row][col] = '0'
            next_state[x][y] = 'x'

            h_new = count_dirty_position(next_state)

            print(next_state)
            print(f"h = {h_new}\n")

            if h_new < h:
                better_states.append((dir, next_state, x, y))

        if len(better_states) == 0:
            print("Khong ton tai cach giai!!!")
            return visited_states, "KHONG TON TAI LOI GIAI"
        chosen = random.choice(better_states)

        visited_states.append((chosen[0], chosen[1].copy()))
        
        cur_state = chosen[1]
        row = chosen[2]
        col = chosen[3]
# === Cell 41 ===
def Stochastic():

    solution_text.delete(1.0, END)

    text_area.delete(1.0, END)

    matrix, row, col = create_mat()

    result, message = stochastic(matrix, row, col)

    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")

    text_area.insert(END, "SEARCHING TIME... \n")
    
    for node in result:

        for i in range(4):
            for j in range(4):

                value = node[1][i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')

        window.update()
        solution_text.insert(END, f"Huong di: {node[0]} \n")
        solution_text.insert(END, node[1])
        solution_text.insert(END, "\n\n")

        time.sleep(0.8)

    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHONG TON TAI LOI GIAI!\n")

        solution_text.insert(END, "NO SOLUTION")
        return

    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI\n")

    solution_text.insert(END, "SOLUTION: ")

    for action, state in result[1:]:
        solution_text.insert(END, action + " ")

    solution_text.insert(END, "\n")
# === Cell 42 ===
def random_restart(matrix, row, col):
    
    print("Trang thai ban dau: ")
    print(matrix)
    
    all_history = []
    for i in range(0, 10):
        print(f"\n========== RESTART {i+1} ==========")
        node = Node(matrix, None, None, count_dirty_position(matrix))
        cur_state = node
        history = []
        while True:
            
            h = count_dirty_position(cur_state.state)
            better = []
            
            if h == 0:
                print("Nha da sach!!!")
                solutions = solution(cur_state)
                for action, state in solutions:
                    print("HUONG DI: ", action)
                    print(state)
                print("DA HOAN THANH!!!")
                return solutions, all_history, "TIM THAY LOI GIAI"
            
            actions = moves(cur_state.state)
            
            for dir, x, y in actions:
                
                new_node = cur_state.state.copy()
                row, col = find_vacuum(new_node)
                new_node[row, col], new_node[x, y] = '0', 'x' 
                
                child = Node(new_node, cur_state, dir, count_dirty_position(new_node))
                
                if child.cost < h:
                    better.append(child)
                    history.append(new_node)
            
            if len(better) == 0:
                print(f"\nDuong di o lan thu {i+1}")

                solutions = solution(cur_state)

                for action, state in solutions:
                    print("HUONG DI:", action)
                    print(state)

                break
            
            next_state = random.choice(better)
            cur_state = next_state
            
        all_history.append(history)
        
    return None, all_history, "KHONG TON TAI LOI GIAI"
# === Cell 43 ===
def Random_Res():

    solution_text.delete(1.0, END)

    text_area.delete(1.0, END)

    matrix, row, col = create_mat()

    result, his ,message = random_restart(matrix, row, col)

    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")

    text_area.insert(END, "SEARCHING TIME... \n")
    
    for restart_id, history in enumerate(his):

        solution_text.insert(END, f"\n========== RESTART {restart_id + 1} ==========\n")

        for state in history:

            for i in range(4):
                for j in range(4):

                    value = state[i][j]

                    if value == '1':
                        cells[i][j].config(bg='red')

                    elif value == '0':
                        cells[i][j].config(bg='light green')

                    elif value == 'x':
                        cells[i][j].config(bg='white')

            window.update()

            solution_text.insert(END, str(state))
            solution_text.insert(END, "\n\n")

            time.sleep(0.8)

    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHONG TON TAI LOI GIAI!\n")

        solution_text.insert(END,"NO SOLUTION")
        return

    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI \n")
    solution = "SOLUTION: "

    solution_text.insert(END, solution)
# === Cell 44 ===
def beam_search(matrix, row, col, k):
    node = Node(matrix, None, None, count_dirty_position(matrix))
    current_state = []
    
    print("TRANG THAI BAN DAU: ")
    print(matrix)
    
    actions = moves(node.state)
    for dir, x, y in actions:
        row, col = find_vacuum(node.state)
        new_node = node.state.copy()
        new_node[row, col], new_node[x, y] = '0', 'x'
        
        child = Node(new_node, node, dir, count_dirty_position(new_node))
        current_state.append(child)
    
    current_state = current_state[:k]
       
    print(f"{k} TRANG THAI CON TU BEAM: \n")
    for i in range(0, k):
        print(f"{current_state[i].state} + Huong: {current_state[i].action}")
        print('\n')
    
    while True:
        neighbors_state = []
        for node in current_state:
            
            if node.cost == 0:
                print("DA TIM DUOC HUONG GIAI!!!")
                solutions = solution(node)
                for action, state in solutions:
                    print("HUONG DI: ", action)
                    print(state)
                print("DA HOAN THANH!!!")
                return solutions, "TIM THAY LOI GIAI"
      
            actions = moves(node.state)
            for dir, x, y in actions:
                row, col = find_vacuum(node.state)
                new_state = node.state.copy()
                new_state[row, col], new_state[x, y] = '0', 'x'
                
                child = Node(new_state, node, dir, count_dirty_position(new_state))
                neighbors_state.append(child)
            
        neighbors_state.sort(key = lambda z : z.cost)
        current_state = neighbors_state[:k]
        
        print(f"{k} TRANG THAI CON TU BEAM: \n")
        for i in range(0, k):
            print(f"{current_state[i].state} + Huong: {current_state[i].action}")
            print('\n')
        
        if len(current_state) == 0:
            print("KHONG TON TAI GIAI PHAP")
            return None, "KHONG TON TAI LOI GIAI"
# === Cell 45 ===
def Beam_Search():
    
    solution_text.delete(1.0, END)
    
    text_area.delete(1.0, END)
    
    matrix, row, col = create_mat()

    result, message = beam_search(matrix, row, col, k = 2)
    
    solution = 'SOLUTION: '
    
    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME... \n")
    
    '''
    for reach in reached:
        
        reach = np.array(reach)
        
        draw_state(reach)
        
        window.update()
        time.sleep(0.1)
    ''' 
    
    text_area.insert(END, "ĐÃ TÌM ĐƯỢC ĐƯỜNG ĐI NGẮT NHẤT \n")
        
    for node in result:
        
        for i in range(4):
            for j in range(4):

                value = (node[1])[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')
                    
                    
        if node[0] == 'UP':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row -1}, {col}]\n")
            row, col = row - 1, col
        elif node[0] == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row + 1}, {col}]\n")
            row, col = row + 1, col
        elif node[0] == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col - 1}]\n")
            row, col = row, col - 1
        else:
            text_area.insert(END, f"Máy đang di chuyển {node[0]} đến vị trí [{row}, {col + 1}]\n")
            row, col = row, col + 1
        
        window.update()
        
        solution += node[0] + " --> "
        solution_text.insert(END, '\n')
        
        solution_text.insert(END, "Hướng: " + node[0])
        solution_text.insert(END, '\n')
        solution_text.insert(END, node[1])
        solution_text.insert(END, '\n\n')
        
        time.sleep(0.8)
        
    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHONG TON TAI LOI GIAI!\n")

        solution_text.insert(END,"NO SOLUTION")
        return
        
    solution_text.insert(END, solution)
    solution_text.delete("end-6c", "end-1c")
# === Cell 46 ===
def simulated_annealing(matrix, row, col):

    print("Trang thai ban dau:")
    print(matrix)

    T = 100.0
    T_min = 10.0
    alpha = 0.95

    node = Node(matrix, None, None, count_dirty_position(matrix))
    cur_state = node

    best_state = cur_state
    best_h = cur_state.cost

    while T > T_min:

        h = count_dirty_position(cur_state.state)

        print("\nTrang thai cha:")
        print(cur_state.state)
        print(f"h = {h}, T = {T:.2f}")

        if h == 0:

            print("NHA DA SACH!!!")

            solutions = solution(cur_state)

            for action, state in solutions:
                print("HUONG DI:", action)
                print(state)

            print("DA HOAN THANH!!!")

            return solutions, "TIM THAY LOI GIAI"

        actions = moves(cur_state.state)

        if len(actions) == 0:
            break

        dir, x, y = random.choice(actions)
        new_state = cur_state.state.copy()
        vac_row, vac_col = find_vacuum(new_state)
        new_state[vac_row, vac_col], new_state[x, y] = '0', 'x'

        child = Node(new_state, cur_state, dir, count_dirty_position(new_state))
        delta = child.cost - h

        if delta < 0:

            print(f"Chap nhan trang thai tot hon: {dir}")

            cur_state = child

        else:

            p = math.exp(-delta / T)
            rand = random.random()
            print(
                f"Trang thai xau hon ({dir}) "
                f"=> P = {p:.4f}, random = {rand:.4f}"
            )
            if rand < p:
                print("Chap nhan")
                cur_state = child

            else:
                print("Tu choi")

        if cur_state.cost < best_h:
            best_h = cur_state.cost
            best_state = cur_state

        T *= alpha

    print("\nKHONG TIM THAY LOI GIAI")
    print(f"So o ban con lai: {best_h}")

    solutions = solution(best_state)

    for action, state in solutions:
        print("HUONG DI:", action)
        print(state)

    return solutions, "KHONG TON TAI LOI GIAI"
# === Cell 47 ===
def Simulated_Annealing():

    solution_text.delete(1.0, END)
    text_area.delete(1.0, END)

    matrix, row, col = create_mat()

    result, message = simulated_annealing(matrix, row, col)

    text_area.insert(END, f"VỊ TRÍ BAN ĐẦU CỦA MÁY HÚT BỤI [{row}, {col}] \n")
    text_area.insert(END, "SEARCHING TIME...\n")

    if result is None:

        text_area.insert(END, "KHÔNG THỂ TÌM THẤY ĐƯỜNG ĐI!\n")
        solution_text.insert(END, "NO SOLUTION")

        return

    if message == "KHONG TON TAI LOI GIAI":

        text_area.insert(END, "KHÔNG TÌM THẤY LỜI GIẢI HOÀN CHỈNH!\n")
        text_area.insert(END, "HIỂN THỊ ĐƯỜNG ĐI TỐT NHẤT TÌM ĐƯỢC...\n")

    solution = "SOLUTION: "

    for node in result:

        action = node[0]
        state = node[1]

        for i in range(4):
            for j in range(4):

                value = state[i][j]

                if value == '1':
                    cells[i][j].config(bg='red')

                elif value == '0':
                    cells[i][j].config(bg='light green')

                elif value == 'x':
                    cells[i][j].config(bg='white')

        if action == 'UP':
            text_area.insert(END, f"Máy đang di chuyển UP đến vị trí [{row - 1}, {col}]\n")
            row -= 1

        elif action == 'DOWN':
            text_area.insert(END, f"Máy đang di chuyển DOWN đến vị trí [{row + 1}, {col}]\n")
            row += 1

        elif action == 'LEFT':
            text_area.insert(END, f"Máy đang di chuyển LEFT đến vị trí [{row}, {col - 1}]\n")
            col -= 1

        elif action == 'RIGHT':
            text_area.insert(END, f"Máy đang di chuyển RIGHT đến vị trí [{row}, {col + 1}]\n")
            col += 1

        window.update()

        if action is not None:
            solution += action + " --> "

        solution_text.insert(END, "\n")

        if action is None:
            solution_text.insert(END, "TRẠNG THÁI BAN ĐẦU\n")
        else:
            solution_text.insert(END, "Hướng: " + action + "\n")

        solution_text.insert(END, str(state))
        solution_text.insert(END, "\n\n")

        time.sleep(0.8)

    if message == "TIM THAY LOI GIAI":
        text_area.insert(END, "ĐÃ TÌM THẤY LỜI GIẢI!\n")
    else:
        solution_text.insert(END, "ĐƯỜNG ĐI TỐT NHẤT TÌM ĐƯỢC DÙ KHÔNG THỂ GIẢI!")
        text_area.insert(END, "ĐÃ HIỂN THỊ ĐƯỜNG ĐI TỐT NHẤT TÌM ĐƯỢC!\n")

    if solution.endswith(" --> "):
        solution = solution[:-5]

    solution_text.insert(END, "\n" + solution)
# === Cell 48 ===
# ==========================================
# THUẬT TOÁN CHO PHẦN "TÌM KIẾM MÙ" (BLIND SEARCH)
# ==========================================

def create_start_sensorless():
    S = []
    for i in range(0, 2):
        arr = np.random.randint(0, 2, (4, 4))
        arr = arr.astype(str)
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        arr[x, y] = 'x'
        S.append(arr)
    return S  

def check_goal_sensorless(lst):
    count = 0
    for x in lst:
        if count_dirty_position(x) == 0:
            count += 1
    return count == len(lst)

def sensorless_search_bfs(start):
    root = Node(start, None, None, 0)
    if check_goal_sensorless(root.state):
        return solution(root), [root.state]
    
    frontier = [root]
    reached = []
    explored_history = []
    
    while frontier:
        node = frontier.pop(0)
        belief = node.state
        key = tuple(tuple(map(tuple, s)) for s in belief)
        if key in reached:
            continue
        reached.append(key)
        explored_history.append(belief)
        
        if check_goal_sensorless(belief):
            return solution(node), explored_history
            
        actions = set()
        for state in belief:
            for dir_name, _, _ in moves(state):
                actions.add(dir_name)
                
        for action in actions:
            new_belief = []
            for state in belief:
                child = state.copy()
                row, col = find_vacuum(child)
                found = False
                for dir_name, x, y in moves(child):
                    if dir_name == action:
                        child[row, col] = '0'
                        child[x, y] = 'x'
                        found = True
                        break
                if not found:
                    child = state.copy()
                new_belief.append(child)
                
            unique_belief = []
            seen_states = set()
            for s in new_belief:
                s_tuple = tuple(map(tuple, s))
                if s_tuple not in seen_states:
                    seen_states.add(s_tuple)
                    unique_belief.append(s)
                    
            child_key = tuple(tuple(map(tuple, s)) for s in unique_belief)
            if child_key not in reached:
                child_node = Node(unique_belief, node, action, node.cost + 1)
                frontier.append(child_node)
    return None, explored_history

def sensorless_search_dfs(start):
    root = Node(start, None, None, 0)
    if check_goal_sensorless(root.state):
        return solution(root), [root.state]
    
    frontier = [root]
    reached = []
    explored_history = []
    
    while frontier:
        node = frontier.pop()
        belief = node.state
        key = tuple(tuple(map(tuple, s)) for s in belief)
        if key in reached:
            continue
        reached.append(key)
        explored_history.append(belief)
        
        if check_goal_sensorless(belief):
            return solution(node), explored_history
            
        actions = set()
        for state in belief:
            for dir_name, _, _ in moves(state):
                actions.add(dir_name)
                
        for action in actions:
            new_belief = []
            for state in belief:
                child = state.copy()
                row, col = find_vacuum(child)
                found = False
                for dir_name, x, y in moves(child):
                    if dir_name == action:
                        child[row, col] = '0'
                        child[x, y] = 'x'
                        found = True
                        break
                if not found:
                    child = state.copy()
                new_belief.append(child)
                
            unique_belief = []
            seen_states = set()
            for s in new_belief:
                s_tuple = tuple(map(tuple, s))
                if s_tuple not in seen_states:
                    seen_states.add(s_tuple)
                    unique_belief.append(s)
                    
            child_key = tuple(tuple(map(tuple, s)) for s in unique_belief)
            if child_key not in reached:
                child_node = Node(unique_belief, node, action, node.cost + 1)
                frontier.append(child_node)
    return None, explored_history

def find_vacuum_position_partial(matrix):
    pos = np.argwhere((matrix == 'x') | (matrix == 'd'))
    if len(pos) == 0:
        return 0, 0
    return pos[0][0], pos[0][1]

def moves_partial(matrix):
    lst_move = []
    row, col = find_vacuum_position_partial(matrix)
    directions = [
        ['LEFT', 0, -1],
        ['RIGHT', 0, 1],
        ['UP', -1, 0],
        ['DOWN', 1, 0],
        ['SUCK', 0, 0] 
    ]
    for dir_name, x, y in directions:
        row_new = row + x
        col_new = col + y
        if 0 <= row_new < 4 and 0 <= col_new < 4:
            lst_move.append([dir_name, row_new, col_new])
    return lst_move

def transition_partial(state, action):
    child = state.copy()
    row, col = find_vacuum_position_partial(child)
    for dir_name, x, y in moves_partial(child):
        if dir_name == action:
            child[row, col] = '0' 
            child[x, y] = 'x'
            break
    return child

def observe_partial(current_state, action):
    row, col = find_vacuum_position_partial(current_state)
    for dir_name, x, y in moves_partial(current_state):
        if dir_name == action:
            return current_state[x, y]
    return 'WALL'

def partially_observation_search(start, partial):
    root = Node(start, None, None, 0)
    root.partial = partial.copy()
    frontier = [root]
    reached = set()
    explored_history = []
    
    while frontier:
        node = frontier.pop()
        belief = node.state
        current_real = node.partial
        
        key = tuple(tuple(map(tuple, s)) for s in belief)
        if key in reached:
            continue
        reached.add(key)
        explored_history.append((belief, current_real))
        
        if check_goal_sensorless(belief):
            return solution(node), explored_history
            
        actions = {dir_name for state in belief for dir_name, _, _ in moves_partial(state)}
        for action in actions:
            real_child = transition_partial(current_real, action)
            observation = observe_partial(real_child, action) 
            
            new_belief = []
            for state in belief:
                next_state = transition_partial(state, action)
                if observe_partial(next_state, action) == observation:
                    new_belief.append(next_state)
                    
            if not new_belief:
                continue
                
            unique_belief = []
            seen_states = set()
            for s in new_belief:
                s_tuple = tuple(map(tuple, s))
                if s_tuple not in seen_states:
                    seen_states.add(s_tuple)
                    unique_belief.append(s)
                    
            child_key = tuple(tuple(map(tuple, s)) for s in unique_belief)
            if child_key not in reached:
                child_node = Node(unique_belief, node, action, node.cost + 1)
                child_node.partial = real_child
                frontier.append(child_node)
    return None, explored_history
# === Cell 49 ===
# ==============================================================================
# PHẦN CODE BỔ SUNG: LIÊN KẾT THUẬT TOÁN SENSORLESS VÀ PARTIAL VÀO VISUALIZER
# Cập nhật vẽ trạng thái, dừng lưới không tương thích với thực tế,
# và cấu hình ô màu đen cho trạng thái chưa biết '?' của Sensorless.
# Sử dụng Sensorless DFS cho "Mù Start" để tránh bị đơ/treo màn hình (do BFS bùng nổ trạng thái).
# In kết quả ra cả giao diện và terminal.
# ==============================================================================

import numpy as np
import random
import time
from tkinter import *

# ----------------- THUẬT TOÁN SENSORLESS (TỪ FILE sensorless.ipynb) -----------------

def find_vaccuum_position_sensorless(matrix):
    pos = np.argwhere(matrix == 'x')[0]
    return pos[0], pos[1]

def moves_sensorless(matrix):
    lst_move = []
    row, col = find_vaccuum_position_sensorless(matrix)
    directions = [
        ['LEFT', 0, -1],
        ['RIGHT', 0, 1],
        ['UP', -1, 0],
        ['DOWN', 1, 0]
    ]
    for dir_name, x, y in directions:
        row_new = row + x
        col_new = col + y
        if 0 <= row_new < 4 and 0 <= col_new < 4:
            lst_move.append([dir_name, row_new, col_new])
    return lst_move

def count_dirty_sensorless(matrix):
    count = 0
    for x in range(0, 4):
        for y in range(0, 4):
            if matrix[x][y] == '1':
                count += 1
    return count

def check_goal_sensorless(lst):
    count = 0
    for x in lst:
        if count_dirty_sensorless(x) == 0:
            count += 1
    return count == len(lst)

def sensorless_search_dfs(start):
    root = Node(start, None, None, 0)
    if check_goal_sensorless(root.state):
        return solution_blind(root), [root.state]
    
    frontier = [root]
    reached = set()
    explored_history = []
    
    while frontier:
        node = frontier.pop()
        belief = node.state
        key = tuple(tuple(map(tuple, s)) for s in belief)
        if key in reached:
            continue
        reached.add(key)
        explored_history.append(belief)
        
        if check_goal_sensorless(belief):
            return solution_blind(node), explored_history
            
        actions = set()
        for state in belief:
            for dir_name, _, _ in moves_sensorless(state):
                actions.add(dir_name)
                
        # Sắp xếp các hành động để DFS chạy ổn định và nhất quán
        for action in sorted(list(actions)):
            new_belief = []
            for state in belief:
                child = state.copy()
                row, col = find_vaccuum_position_sensorless(child)
                found = False
                for dir_name, x, y in moves_sensorless(child):
                    if dir_name == action:
                        child[row, col] = '0'
                        child[x, y] = 'x'
                        found = True
                        break
                if not found:
                    child = state.copy()
                new_belief.append(child)
                
            unique_belief = []
            seen_states = set()
            for s in new_belief:
                s_tuple = tuple(map(tuple, s))
                if s_tuple not in seen_states:
                    seen_states.add(s_tuple)
                    unique_belief.append(s)
                    
            child_key = tuple(tuple(map(tuple, s)) for s in unique_belief)
            if child_key not in reached:
                child_node = Node(unique_belief, node, action, node.cost + 1)
                frontier.append(child_node)
    return None, explored_history

# ------------- THUẬT TOÁN PARTIAL (TỪ FILE partially_observation.ipynb) -------------

def find_vacuum_position_partial(matrix):
    pos = np.argwhere((matrix == 'x') | (matrix == 'd'))
    if len(pos) == 0:
        return 0, 0
    return pos[0][0], pos[0][1]

def moves_partial(matrix):
    lst_move = []
    row, col = find_vacuum_position_partial(matrix)
    directions = [
        ['LEFT', 0, -1],
        ['RIGHT', 0, 1],
        ['UP', -1, 0],
        ['DOWN', 1, 0],
        ['SUCK', 0, 0] 
    ]
    for dir_name, x, y in directions:
        row_new = row + x
        col_new = col + y
        if 0 <= row_new < 4 and 0 <= col_new < 4:
            lst_move.append([dir_name, row_new, col_new])
    return lst_move

def count_dirty_partial(matrix):
    count = 0
    for x in range(0, 4):
        for y in range(0, 4):
            if matrix[x][y] == '1' or matrix[x][y] == 'd':
                count += 1
    return count

def check_goal_partial(lst):
    count = 0
    for x in lst:
        if count_dirty_partial(x) == 0:
            count += 1
    return count == len(lst)

def observe_partial(current_state, action):
    row, col = find_vacuum_position_partial(current_state)
    for dir_name, x, y in moves_partial(current_state):
        if dir_name == action:
            return current_state[x, y]
    return 'WALL'

def transition_partial(state, action):
    child = state.copy()
    row, col = find_vacuum_position_partial(child)
    for dir_name, x, y in moves_partial(child):
        if dir_name == action:
            child[row, col] = '0' 
            child[x, y] = 'x'
            break
    return child

def solution_blind(node):
    path = []
    while node.parent is not None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path

def partially_observation_search(start, partial):
    root = Node(start, None, None, 0)
    root.partial = partial.copy()
    frontier = [root]
    reached = set()
    explored_history = []
    
    while frontier:
        node = frontier.pop()
        belief = node.state
        current_real = node.partial
        
        key = tuple(tuple(map(tuple, s)) for s in belief)
        if key in reached:
            continue
        reached.add(key)
        explored_history.append((node, belief, current_real))
        
        if check_goal_partial(belief):
            return solution_blind(node), explored_history
            
        actions = {dir_name for state in belief for dir_name, _, _ in moves_partial(state)}
        for action in actions:
            real_child = transition_partial(current_real, action)
            observation = observe_partial(real_child, action) 
            
            new_belief = []
            for state in belief:
                next_state = transition_partial(state, action)
                if observe_partial(next_state, action) == observation:
                    new_belief.append(next_state)
                    
            if not new_belief:
                continue
                
            unique_belief = []
            seen_states = set()
            for s in new_belief:
                s_tuple = tuple(map(tuple, s))
                if s_tuple not in seen_states:
                    seen_states.add(s_tuple)
                    unique_belief.append(s)
                    
            child_key = tuple(tuple(map(tuple, s)) for s in unique_belief)
            if child_key not in reached:
                child_node = Node(unique_belief, node, action, node.cost + 1)
                child_node.partial = real_child
                frontier.append(child_node)
    return None, explored_history

# ----------------- HÀM PHỤ TRỢ CHO QUÁ TRÌNH TRỰC QUAN HÓA -----------------

def trace_survival(node, start_belief, real_state):
    path_nodes = []
    curr = node
    while curr is not None:
        path_nodes.append(curr)
        curr = curr.parent
    path_nodes.reverse()
    
    actions = [n.action for n in path_nodes[1:]]
    
    curr_real = real_state.copy()
    b0_state = start_belief[0].copy()
    b1_state = start_belief[1].copy()
    
    grid1_active = True
    grid2_active = True
    
    for action in actions:
        if action is None:
            continue
        curr_real = transition_partial(curr_real, action)
        obs = observe_partial(curr_real, action)
        
        if grid1_active:
            b0_state = transition_partial(b0_state, action)
            if observe_partial(b0_state, action) != obs:
                grid1_active = False
        if grid2_active:
            b1_state = transition_partial(b1_state, action)
            if observe_partial(b1_state, action) != obs:
                grid2_active = False
                
    return grid1_active, grid2_active, b0_state, b1_state

# ----------------- CẬP NHẬT VÀ GHI ĐÈ PHƯƠNG THỨC TRÊN GIAO DIỆN GUI -----------------

def draw_blind_states(state1, state2=None, is_sensorless=False):
    # Lưới 1 (Belief A)
    for i in range(4):
        for j in range(4):
            val = state1[i][j]
            cell = cells[i][j]
            if val == '1' or val == 'd':
                cell.config(bg='red')
            elif val == '0':
                cell.config(bg='light green')
            elif val == 'x':
                cell.config(bg='yellow')
            elif val == '?':
                if is_sensorless:
                    cell.config(bg='black')  # Đối với sensorless '?' thay thành ô đen
                else:
                    cell.config(bg='gray')

    # Lưới 2 (Belief B hoặc Real)
    if state2 is not None:
        for i in range(4):
            for j in range(4):
                val = state2[i][j]
                cell = cells2[i][j]
                if val == '1' or val == 'd':
                    cell.config(bg='red')
                elif val == '0':
                    cell.config(bg='light green')
                elif val == 'x':
                    cell.config(bg='yellow')
                elif val == '?':
                    if is_sensorless:
                        cell.config(bg='black')  # Đối với sensorless '?' thay thành ô đen
                    else:
                        cell.config(bg='gray')

def show_blind_visualizer():
    global text_area, solution_text, cells, cells2, current_group
    current_group = "blind"
    reset_view()
    
    # Sidebar chọn thuật toán màu cyan
    but_frame = Frame(window, bg="cyan")
    but_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
    
    Label(
        but_frame,
        text="Blind Search",
        font=("Times New Roman", 14, "bold"),
        bg="cyan"
    ).pack(pady=10)
    
    blind_algos = [
        ("Mù Start", "Mù Start"),
        ("Mù Partial", "Mù Partial")
    ]
    
    for display_name, value_name in blind_algos:
        Radiobutton(
            but_frame,
            text=display_name,
            variable=selected_blind_algo,
            value=value_name,
            font=("Times New Roman", 10, "bold"),
            bg="cyan",
            anchor="w"
        ).pack(fill="x", padx=10, pady=5)
        
    bottom_btn_frame = Frame(but_frame, bg="cyan")
    bottom_btn_frame.pack(side="bottom", fill="x", pady=5)
    
    Button(bottom_btn_frame, text="RUN", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=run_blind).pack(pady=5)
    Button(bottom_btn_frame, text="STOP", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=trigger_stop).pack(pady=5)
    Button(bottom_btn_frame, text="EXIT", width=10, font=("Times New Roman", 12, "bold"), relief=RAISED, command=exit_visualizer).pack(pady=5)
    
    # Grid Container ở giữa chứa 2 lưới con side-by-side
    frame = Frame(window)
    frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    
    # 2 nhãn tiêu đề Belief A / B để phân biệt 2 lưới
    grid1_box = LabelFrame(frame, text="Belief State A", font=("Times New Roman", 10, "bold"))
    grid1_box.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    for r in range(4):
        grid1_box.rowconfigure(r, weight=1)
        grid1_box.columnconfigure(r, weight=1)
        
    grid2_box = LabelFrame(frame, text="Belief State B / Real", font=("Times New Roman", 10, "bold"))
    grid2_box.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    for r in range(4):
        grid2_box.rowconfigure(r, weight=1)
        grid2_box.columnconfigure(r, weight=1)
        
    cells = []
    for row in range(4):
        temp = []
        for col in range(4):
            cell = Frame(grid1_box, width=70, height=70, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            temp.append(cell)
        cells.append(temp)
        
    cells2 = []
    for row in range(4):
        temp = []
        for col in range(4):
            cell = Frame(grid2_box, width=70, height=70, bg="white", highlightthickness=2, highlightbackground="black")
            cell.grid(row=row, column=col, sticky="nsew")
            cell.grid_propagate(False)
            temp.append(cell)
        cells2.append(temp)
        
    # Nhật ký ở bên phải
    text_area = Text(window, width=40, height=18, relief=RAISED, font=("Segoe UI", 11), bg="black", fg="white")
    text_area.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    
    # Kết quả đường đi giải pháp ở dưới
    solution_text = Text(window, width=88, height=9, relief=RAISED, font=("Segoe UI", 11))
    solution_text.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
    
    # Khởi tạo vẽ 2 lưới ban đầu
    reset_blind_ui()

def run_blind():
    global stop_execution
    stop_execution = False
    
    print("[GUI] Clicked RUN button in Blind Search", flush=True)
    solution_text.delete(1.0, END)
    text_area.delete(1.0, END)
    
    algo = selected_blind_algo.get()
    print(f"[GUI] Selected Algorithm: {algo}", flush=True)
    
    text_area.insert(END, f"TRẠNG THÁI THUẬT TOÁN MÙ: {algo}\n")
    text_area.insert(END, "SEARCHING TIME... \n")
    window.update()
    
    start_belief = [
        np.array([['1', '0', '1', '0'],
                  ['0', '0', '0', '1'],
                  ['x', '1', '0', '1'],
                  ['0', '0', '0', '1']]),
        np.array([['1', '0', '0', '0'],
                  ['1', '1', '1', 'x'],
                  ['1', '0', '0', '0'],
                  ['1', '1', '0', '0']])
    ]
    
    if algo == "Mù Start":
        # In trạng thái ban đầu ra Terminal theo đúng phong cách file sensorless.ipynb
        print("TRANG THAI BAN DAU", flush=True)
        for state in start_belief:
            print(state, flush=True)
            print("", flush=True)
            
        # Cấu hình nhãn tiêu đề lưới
        try:
            grid1_frame = window.nametowidget(".!frame.!labelframe")
            grid1_frame.config(text="Belief State A")
            grid2_frame = window.nametowidget(".!frame.!labelframe2")
            grid2_frame.config(text="Belief State B")
        except Exception:
            pass

        print("[DFS] Running sensorless_search_dfs...", flush=True)
        solutions, explored = sensorless_search_dfs(start_belief)
        print(f"[DFS] Done. solutions length: {len(solutions) if solutions else 0}, explored: {len(explored)}", flush=True)
            
        # Bỏ qua hoạt họa duyệt (Exploration) để tránh đơ màn hình vì số lượng explored có thể lên tới hàng ngàn
        # time.sleep(0.15)
            
        # Trực quan hóa Solution Path (Đường đi kết quả)
        if solutions:
            text_area.insert(END, "ĐÃ TÌM ĐƯỢC CHUỒI HÀNH ĐỘNG THÀNH CÔNG!\n")
            draw_blind_states(start_belief[0], start_belief[1], is_sensorless=True)
            window.update()
            time.sleep(0.5)
            
            # In ra Terminal theo phong cách sensorless.ipynb
            print("TIM THAY LOI GIAI", flush=True)
            print(f"Huong di chuyen: {[x[0] for x in solutions]}", flush=True)
            
            solution_str = "SOLUTION: "
            s1 = start_belief[0].copy()
            s2 = start_belief[1].copy()
            
            for idx, (action, belief_state) in enumerate(solutions):
                if stop_execution:
                    text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                    return
                
                # Di chuyển đồng thời trên cả 2 ma trận
                row1, col1 = find_vaccuum_position_sensorless(s1)
                found1 = False
                for dir_name, x, y in moves_sensorless(s1):
                    if dir_name == action:
                        s1[row1, col1] = '0'
                        s1[x, y] = 'x'
                        found1 = True
                        break
                
                row2, col2 = find_vaccuum_position_sensorless(s2)
                found2 = False
                for dir_name, x, y in moves_sensorless(s2):
                    if dir_name == action:
                        s2[row2, col2] = '0'
                        s2[x, y] = 'x'
                        found2 = True
                        break
                
                # In danh sách các ma trận trạng thái niềm tin ra Terminal
                print([s1, s2], flush=True)
                print("", flush=True)
                
                draw_blind_states(s1, s2, is_sensorless=True)
                text_area.insert(END, f"Bước {idx+1}: Di chuyển {action}\n")
                window.update()
                
                solution_str += action + " --> "
                solution_text.insert(END, f"Bước {idx+1}: Hướng {action}\n")
                solution_text.insert(END, f"Belief State A:\n{str(s1)}\nBelief State B:\n{str(s2)}\n\n")
                time.sleep(0.8)
                
            solution_text.insert(END, solution_str[:-5])
        else:
            print("KHONG TIM THAY LOI GIAI", flush=True)
            text_area.insert(END, "KHÔNG TÌM THẤY ĐƯỜNG ĐI MÙ!\n")
            solution_text.insert(END, "NO SOLUTION")
            
    elif algo == "Mù Partial":
        real_state = np.array([
            ['1', '?', '1', '0'],
            ['0', '0', '?', '1'],
            ['x', '1', '0', '1'],
            ['?', '?', '?', '?']
        ])
        
        # In trạng thái ban đầu ra Terminal theo đúng phong cách file partially_observation.ipynb
        print("TRANG THAI BAN DAU AN DUNG (BELIEF):", flush=True)
        for state in start_belief:
            print(state, flush=True)
            print("", flush=True)
        print("TRANG THAI THUC (CO O AN '?'):", flush=True)
        print(real_state, flush=True)
        print("", flush=True)

        try:
            grid1_frame = window.nametowidget(".!frame.!labelframe")
            grid1_frame.config(text="Belief State A")
            grid2_frame = window.nametowidget(".!frame.!labelframe2")
            grid2_frame.config(text="Belief State B")
        except Exception:
            pass

        print("[Partial] Running partially_observation_search...", flush=True)
        solutions, explored = partially_observation_search(start_belief, real_state)
        print(f"[Partial] Done. solutions length: {len(solutions) if solutions else 0}, explored: {len(explored)}", flush=True)
        
        # Bỏ qua phần hoạt họa duyệt để tránh đơ màn hình
        # time.sleep(0.2)
        
        # Trực quan hóa Solution Path (Đường đi kết quả)
        if solutions:
            text_area.insert(END, "ĐÃ TÌM THẤY LỜI GIẢI AN TOÀN CHO MÔI TRƯỜNG MỘT PHẦN!\n")
            
            # In ra Terminal theo phong cách partially_observation.ipynb
            print("TIM THAY LOI GIAI", flush=True)
            print(f"Huong di chuyen: {[x[0] for x in solutions]}", flush=True)
            
            g1_active = True
            g2_active = True
            s1 = start_belief[0].copy()
            s2 = start_belief[1].copy()
            curr_real = real_state.copy()
            
            draw_blind_states(s1, s2, is_sensorless=False)
            window.update()
            time.sleep(0.5)
            
            solution_str = "SOLUTION: "
            
            for idx, (action, belief_state) in enumerate(solutions):
                if stop_execution:
                    text_area.insert(END, "\nĐÃ DỪNG THUẬT TOÁN!\n")
                    return
                
                curr_real = transition_partial(curr_real, action)
                obs = observe_partial(curr_real, action)
                
                # Di chuyển ma trận A nếu còn hoạt động
                if g1_active:
                    s1 = transition_partial(s1, action)
                    if observe_partial(s1, action) != obs:
                        g1_active = False
                        text_area.insert(END, f"Bước {idx+1}: Lưới A khác thực tế -> DỪNG LƯỚI A!\n")
                
                # Di chuyển ma trận B nếu còn hoạt động
                if g2_active:
                    s2 = transition_partial(s2, action)
                    if observe_partial(s2, action) != obs:
                        g2_active = False
                        text_area.insert(END, f"Bước {idx+1}: Lưới B khác thực tế -> DỪNG LƯỚI B!\n")
                
                # Cập nhật tiêu đề lưới trên GUI để thể hiện trạng thái dừng (không bôi đen cả lưới)
                try:
                    grid1_frame = window.nametowidget(".!frame.!labelframe")
                    grid1_frame.config(text="Belief State A" if g1_active else "Belief State A (STOPPED)")
                    grid2_frame = window.nametowidget(".!frame.!labelframe2")
                    grid2_frame.config(text="Belief State B" if g2_active else "Belief State B (STOPPED)")
                except Exception:
                    pass

                # In các ma trận trạng thái niềm tin còn sống ra Terminal
                active_beliefs = []
                if g1_active:
                    active_beliefs.append(s1)
                if g2_active:
                    active_beliefs.append(s2)
                print(active_beliefs, flush=True)
                print("", flush=True)
                
                # Vẽ trạng thái lên giao diện Tkinter (Giữ nguyên trạng thái cuối cùng, không đổi màu đen toàn lưới)
                draw_blind_states(s1, s2, is_sensorless=False)
                text_area.insert(END, f"Bước {idx+1}: Di chuyển {action} (Obs: {obs})\n")
                window.update()
                
                solution_str += action + " --> "
                solution_text.insert(END, f"Bước {idx+1}: Hành động {action} (Obs: {obs})\n")
                solution_text.insert(END, f"Lưới A:\n{str(s1) if g1_active else 'STOPPED'}\nLưới B:\n{str(s2) if g2_active else 'STOPPED'}\n\n")
                time.sleep(0.8)
                
            solution_text.insert(END, solution_str[:-5])
        else:
            print("KHONG TIM THAY LOI GIAI", flush=True)
            text_area.insert(END, "KHÔNG TÌM THẤY ĐƯỜNG ĐI!\n")
            solution_text.insert(END, "NO SOLUTION")
# === Adversarial Search Logic ===
def find_blank(matrix):
    blank = []
    for x in range(0, 3):
        for y in range(0, 3):
            if matrix[x][y] == "":
                blank.append((x, y))
    return blank

def check_winner(matrix):
    for row in matrix:
        if row[0] == row[1] == row[2] != "":
            return row[0]
        
    for col in range(0, 3):
        if matrix[0][col] == matrix[1][col] == matrix[2][col] != "":
            return matrix[0][col]
        
    if matrix[0][0] == matrix[1][1] == matrix[2][2] != "":
        return matrix[0][0]
    
    if matrix[0][2] == matrix[1][1] == matrix[2][0] != "":
        return matrix[0][2]
    
    return False

def utility(matrix):
    winner = check_winner(matrix)
    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    return 0

def current_player(board):
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == 'X':
                x_count += 1
            elif cell == 'O':
                o_count += 1
    if x_count == o_count:
        return "X"
    else:
        return "O"

def result_board(board, row, col, sign):
    temp = [r[:] for r in board]
    temp[row][col] = sign
    return temp

def minimax(board):
    global adversarial_nodes
    adversarial_nodes += 1
    
    if len(find_blank(board)) == 0 or check_winner(board) is not False:
        return utility(board), []
    
    turn = current_player(board)
    
    if turn == 'X':
        value = -float('inf')
        best_path = []
        
        blank_position = find_blank(board)
        for x in blank_position:
            child = result_board(board, x[0], x[1], 'X')
            score, path = minimax(child)
            if score > value:
               value = score
               best_path = [x] + path
        return value, best_path
    else:
        value = float('inf')
        best_path = []
        
        blank_position = find_blank(board)
        for x in blank_position:
            child = result_board(board, x[0], x[1], 'O')
            score, path = minimax(child)
            if score < value:
               value = score
               best_path = [x] + path
        return value, best_path

def alphabeta(board, alpha, beta):
    global adversarial_nodes
    adversarial_nodes += 1

    if len(find_blank(board)) == 0 or check_winner(board) is not False:
        return utility(board), []

    turn = current_player(board)

    if turn == 'X':
        value = -float('inf')
        best_path = []
        for move in find_blank(board):
            child = result_board(board, move[0], move[1], 'X')
            score, path = alphabeta(child, alpha, beta)
            if score > value:
                value = score
                best_path = [move] + path
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_path
    else:
        value = float('inf')
        best_path = []
        for move in find_blank(board):
            child = result_board(board, move[0], move[1], 'O')
            score, path = alphabeta(child, alpha, beta)
            if score < value:
                value = score
                best_path = [move] + path
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_path

def expectimax(board):
    global adversarial_nodes
    adversarial_nodes += 1

    if len(find_blank(board)) == 0 or check_winner(board) is not False:
        return utility(board), []

    turn = current_player(board)

    if turn == 'X':
        value = -float('inf')
        best_path = []
        for move in find_blank(board):
            child = result_board(board, move[0], move[1], 'X')
            score, path = expectimax(child)
            if score > value:
                value = score
                best_path = [move] + path
        return value, best_path
    else:
        blank_position = find_blank(board)
        expected_value = 0
        best_path = []
        rate = 1 / len(blank_position)
        for move in blank_position:
            child = result_board(board, move[0], move[1], 'O')
            score, path = expectimax(child)
            expected_value += rate * score
            if best_path == []:
                best_path = [move] + path
        return expected_value, best_path

# === Cell 50 ===
if __name__ == "__main__":
    main()
