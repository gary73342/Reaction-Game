import tkinter as tk
from tkinter import messagebox
import random
import time

class ColorfulSpeedGame:
    def __init__(self, root):
        self.root = root
        self.root.title("1-9 速點")
        self.root.geometry("450x600")
        self.root.configure(bg="#f0f0f0") # 設定背景為淡灰，讓彩色格子更明顯
        
        # 遊戲變數
        self.current_target = 1
        self.start_time = 0
        self.buttons = []
        
        # 定義 9 種不含黑色的顏色 (採用較柔和的色碼)
        self.colors = [
            "#FF9999", # 粉紅
            "#FFCC99", # 粉橘
            "#FFFF99", # 淡黃
            "#99FF99", # 淡綠
            "#99FFFF", # 淡青
            "#99CCFF", # 淡藍
            "#CC99FF", # 淡紫
            "#FF99CC", # 桃紅
            "#FFD700"  # 金色
        ]

        self.setup_ui()
        self.start_new_game()

    def setup_ui(self):
        # 標題與提示
        self.top_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.top_frame.pack(pady=20)
        
        self.info_label = tk.Label(
            self.top_frame, 
            text="請依序點擊 1 → 9", 
            font=("微軟正黑體", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.info_label.pack()

        # 遊戲區 (九宮格)
        self.game_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.game_frame.pack(pady=10)

        # 底部控制區
        self.reset_btn = tk.Button(
            self.root, 
            text="⟳ 重新開始", 
            command=self.start_new_game, 
            font=("微軟正黑體", 12),
            bg="white",
            relief="groove",
            width=15
        )
        self.reset_btn.pack(pady=20)

    def start_new_game(self):
        # 重置數據
        self.current_target = 1
        self.start_time = 0
        self.info_label.config(text="準備好了嗎？請點擊 1")
        
        # 清除舊按鈕
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # 準備數字與顏色並洗牌
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        current_game_colors = self.colors[:] # 複製一份顏色清單
        random.shuffle(current_game_colors)  # 洗牌顏色
        
        self.buttons = []
        
        # 建立 3x3 按鈕
        for row in range(3):
            for col in range(3):
                num = numbers.pop()
                color = current_game_colors.pop()
                
                btn = tk.Button(
                    self.game_frame,
                    text=str(num),
                    font=("Arial", 28, "bold"),
                    bg=color,          # 設定背景顏色
                    fg="#333333",      # 文字深灰 (對比清晰)
                    activebackground="white", # 點擊時的效果
                    width=4,
                    height=2,
                    relief="raised",   # 浮起效果
                    bd=3,
                    command=lambda n=num: self.on_btn_click(n)
                )
                btn.grid(row=row, column=col, padx=8, pady=8)
                
                # 存入列表以便後續操作
                self.buttons.append((num, btn))

    def on_btn_click(self, number):
        # 檢查順序
        if number == self.current_target:
            
            # 視覺效果：點對了變成白色並「凹」下去
            for val, btn in self.buttons:
                if val == number:
                    btn.config(
                        bg="white", 
                        fg="#dddddd", # 文字變淡
                        relief="sunken", # 凹陷
                        state="disabled" # 鎖定不能再點
                    )
                    break
            
            # 邏輯處理
            if number == 1:
                self.start_time = time.time()
                self.info_label.config(text="計時中...")
            
            if number == 9:
                end_time = time.time()
                elapsed = end_time - self.start_time
                self.info_label.config(text=f"完成！")
                messagebox.showinfo("挑戰成功", f"你的反應時間：\n\n{elapsed:.3f} 秒")
                return

            self.current_target += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorfulSpeedGame(root)
    root.mainloop()