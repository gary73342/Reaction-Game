import tkinter as tk
from tkinter import messagebox
import random
import time

class ColorfulSpeedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("極速點擊挑戰")
        self.root.configure(bg="#f0f0f0")
        
        # 定義 16 種顏色 (原本9種 + 新增7種)
        self.colors = [
            "#FF9999", "#FFCC99", "#FFFF99", "#99FF99", # 紅/橘/黃/綠
            "#99FFFF", "#99CCFF", "#CC99FF", "#FF99CC", # 青/藍/紫/粉
            "#FFD700",                                  # 金 (原本的第9色)
            # --- 新增的 7 種顏色 ---
            "#87CEEB", # 天空藍 (SkyBlue)
            "#FFA07A", # 淺鮭紅 (LightSalmon)
            "#90EE90", # 淺綠 (LightGreen)
            "#DDA0DD", # 梅紅 (Plum)
            "#F0E68C", # 卡其色 (Khaki)
            "#20B2AA", # 淺海綠 (LightSeaGreen)
            "#B0C4DE"  # 鋼藍色 (LightSteelBlue)
        ]

        # 遊戲變數
        self.current_mode = 3 # 預設 3x3
        self.current_target = 1
        self.start_time = 0
        self.buttons = []
        
        # 啟動時先顯示主選單
        self.show_menu()

    def show_menu(self):
        """顯示選擇難度的主選單"""
        # 清除視窗內所有物件
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # 設定選單視窗大小
        self.root.geometry("400x350")
        
        # 標題
        title = tk.Label(
            self.root, 
            text="請選擇挑戰模式", 
            font=("微軟正黑體", 20, "bold"), 
            bg="#f0f0f0", fg="#333"
        )
        title.pack(pady=50)

        # 按鈕區塊
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack()

        # 3x3 按鈕
        btn3 = tk.Button(
            btn_frame, 
            text="3 x 3\n(簡單)", 
            font=("Arial", 14), 
            bg="#99FF99",
            width=10, height=3,
            command=lambda: self.start_game_ui(3)
        )
        btn3.grid(row=0, column=0, padx=15)

        # 4x4 按鈕
        btn4 = tk.Button(
            btn_frame, 
            text="4 x 4\n(進階)", 
            font=("Arial", 14), 
            bg="#FF9999",
            width=10, height=3,
            command=lambda: self.start_game_ui(4)
        )
        btn4.grid(row=0, column=1, padx=15)

    def start_game_ui(self, mode):
        """建立遊戲畫面"""
        self.current_mode = mode
        
        # 根據模式調整視窗大小
        if mode == 3:
            self.root.geometry("450x550")
        else:
            self.root.geometry("550x650") # 4x4 需要大一點的空間

        # 清除選單畫面
        for widget in self.root.winfo_children():
            widget.destroy()

        # --- 遊戲介面配置 ---
        
        # 上方資訊區
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=15)
        
        self.info_label = tk.Label(
            top_frame, 
            text=f"模式: {mode}x{mode} | 請依序點擊 1", 
            font=("微軟正黑體", 16, "bold"),
            bg="#f0f0f0"
        )
        self.info_label.pack()

        # 遊戲區 (格子)
        self.game_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.game_frame.pack(pady=10)

        # 底部按鈕區
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.pack(pady=20)

        # 重新開始按鈕
        tk.Button(
            bottom_frame, text="⟳ 重新洗牌", 
            command=self.reset_game,
            font=("微軟正黑體", 12), width=10
        ).pack(side=tk.LEFT, padx=10)

        # 回主選單按鈕
        tk.Button(
            bottom_frame, text="回主選單", 
            command=self.show_menu,
            font=("微軟正黑體", 12), width=10
        ).pack(side=tk.LEFT, padx=10)

        # 開始這一局
        self.reset_game()

    def reset_game(self):
        """重置遊戲數據與按鈕"""
        self.current_target = 1
        self.start_time = 0
        total_cells = self.current_mode * self.current_mode
        
        self.info_label.config(text="準備好了嗎？請點擊 1")

        # 清除舊格子
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # 準備數字 (1 ~ N*N)
        numbers = list(range(1, total_cells + 1))
        random.shuffle(numbers)
        
        # 準備顏色 (取出前 N*N 個顏色並洗牌)
        current_colors = self.colors[:total_cells]
        random.shuffle(current_colors)
        
        self.buttons = []
        
        # 動態生成格子
        for row in range(self.current_mode):
            for col in range(self.current_mode):
                num = numbers.pop()
                color = current_colors.pop()
                
                # 4x4 時字體稍微縮小一點，避免太擠
                font_size = 28 if self.current_mode == 3 else 22
                
                btn = tk.Button(
                    self.game_frame,
                    text=str(num),
                    font=("Arial", font_size, "bold"),
                    bg=color,
                    fg="#333",
                    activebackground="white",
                    width=4, height=2,
                    relief="raised", bd=3,
                    command=lambda n=num: self.on_btn_click(n)
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append((num, btn))

    def on_btn_click(self, number):
        total_cells = self.current_mode * self.current_mode
        
        if number == self.current_target:
            # 視覺回饋
            for val, btn in self.buttons:
                if val == number:
                    btn.config(bg="white", fg="#ddd", relief="sunken", state="disabled")
                    break
            
            # 計時邏輯
            if number == 1:
                self.start_time = time.perf_counter()
                self.info_label.config(text="計時中...加油！")
            
            # 結束邏輯
            if number == total_cells:
                end_time = time.perf_counter()
                elapsed = end_time - self.start_time
                self.info_label.config(text="挑戰成功！")
                messagebox.showinfo("完成", f"【{self.current_mode}x{self.current_mode} 模式】\n\n花費時間：{elapsed:.3f} 秒")
                return

            self.current_target += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorfulSpeedGame(root)
    root.mainloop()