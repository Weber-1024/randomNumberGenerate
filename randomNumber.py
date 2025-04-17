import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from PIL import Image, ImageTk

class RandomNumberGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ビンゴゲーム")
        self.root.state('zoomed')  # ウィンドウを最大化
        
        # レイアウトの設定（左:右 = 3:1）
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        
        # メインフレームの作成
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # メインフレームのレイアウト設定
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # 数字表示用のコンテナ
        self.number_container = ttk.Frame(self.main_frame)
        self.number_container.grid(row=0, column=0, sticky="nsew")
        self.number_container.grid_rowconfigure(0, weight=1)
        self.number_container.grid_columnconfigure(0, weight=1)
        
        # キャンバスの作成（数字表示用）
        self.canvas = tk.Canvas(
            self.number_container,
            width=600,
            height=600,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # 背景画像の読み込み
        try:
            self.background_image = Image.open("background.jpg")
            self.background_image_original = self.background_image.copy()
            self.resize_background()
            self.canvas.bind('<Configure>', self.on_canvas_resize)
        except Exception as e:
            messagebox.showwarning("警告", f"背景图片加载失败: {str(e)}")
            self.canvas.configure(bg='#f0f0f0')
        
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # 初期テキストの表示
        self.canvas_text = self.canvas.create_text(
            canvas_width // 2,
            canvas_height // 2,
            text="ビンゴゲーム",
            font=("Arial", 80),
            anchor="center",
            fill='black',
            tags="text"
        )
        
        # ボタンフレームの作成
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=1, column=0, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        # スタートボタンの作成
        self.generate_button = tk.Button(
            self.button_frame,
            text="スタート",
            command=self.generate_number,
            font=("Arial", 24),
            height=2,
            width=15,
            bg='#f0f0f0',
            activebackground='#e0e0e0'
        )
        self.generate_button.grid(row=0, column=0, pady=30)
        
        # 履歴表示用フレーム
        self.history_frame = ttk.Frame(root)
        self.history_frame.grid(row=0, column=1, sticky="nsew", padx=20)
        
        # 履歴ラベルの作成
        self.history_label = ttk.Label(
            self.history_frame,
            text="これまでに出て数字",
            font=("Arial", 24, "bold")
        )
        self.history_label.pack(pady=10)
        
        # 履歴表示用テキストウィジェット
        self.history_text = tk.Text(
            self.history_frame,
            width=20,
            height=20,
            font=("Arial", 28),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg='#f0f0f0',
            fg='black'
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        # カスタム数字入力用フレーム
        self.custom_frame = ttk.Frame(self.history_frame)
        self.custom_frame.pack(fill=tk.X, pady=10)
        
        # 数字入力用エントリー
        self.custom_entry = ttk.Entry(
            self.custom_frame,
            width=10,
            font=("Arial", 20)
        )
        self.custom_entry.pack(side=tk.LEFT, padx=10)
        
        # 追加ボタンの作成
        self.add_button = tk.Button(
            self.custom_frame,
            text="追加",
            command=self.add_custom_number,
            font=("Arial", 24),
            height=2,
            width=6,
            bg='#f0f0f0',
            activebackground='#e0e0e0'
        )
        self.add_button.pack(side=tk.LEFT)
        
        # 変数の初期化
        self.is_animating = False
        self.animation_count = 0
        self.final_number = None
        self.history = []
        self.available_numbers = set(range(1, 76))  # 1から75までの数字
        self.numbers_per_line = 5  # 1行に表示する数字の数
        
    def resize_background(self):
        # 背景画像のリサイズ処理
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            resized_image = self.background_image_original.resize(
                (canvas_width, canvas_height),
                Image.LANCZOS
            )
            self.background_photo = ImageTk.PhotoImage(resized_image)
            
            self.canvas.delete("background")
            self.canvas.create_image(
                0, 0,
                image=self.background_photo,
                anchor="nw",
                tags="background"
            )
            
            self.canvas.tag_raise("text")
    
    def on_canvas_resize(self, event):
        # キャンバスサイズ変更時の処理
        self.resize_background()
        
    def generate_number(self):
        # ランダム数字生成処理
        if not self.is_animating:
            if not self.available_numbers:
                messagebox.showinfo("情報", "すべての数字が使用されました！")
                return
                
            self.is_animating = True
            self.animation_count = 0
            self.final_number = random.choice(list(self.available_numbers))
            self.generate_button.config(state=tk.DISABLED)
            self.animate_number()
            
    def animate_number(self):
        # 数字表示のアニメーション処理
        if self.is_animating:
            if self.animation_count < 30:
                available = list(self.available_numbers)
                random_num = random.choice(available)
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                self.canvas.itemconfig(
                    self.canvas_text,
                    text=str(random_num),
                    font=("Arial", 200),
                    fill='white'
                )
                self.canvas.coords(
                    self.canvas_text,
                    canvas_width // 2,
                    canvas_height // 2
                )
                
                self.animation_count += 1
                self.root.after(60, self.animate_number)
            else:
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                self.canvas.itemconfig(
                    self.canvas_text,
                    text=str(self.final_number),
                    font=("Arial", 200),
                    fill='white'
                )
                self.canvas.coords(
                    self.canvas_text,
                    canvas_width // 2,
                    canvas_height // 2
                )
                self.is_animating = False
                self.generate_button.config(state=tk.NORMAL)
                self.add_to_history(self.final_number)
                
    def add_to_history(self, number):
        # 履歴への数字追加処理
        if number in self.history:
            return
            
        self.history.append(number)
        self.history.sort()
        self.available_numbers.remove(number)
        self.update_history_display()
        
    def update_history_display(self):
        # 履歴表示の更新処理
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for i, number in enumerate(self.history):
            self.history_text.insert(tk.END, f"{number:4d} ")
            
            if (i + 1) % self.numbers_per_line == 0:
                self.history_text.insert(tk.END, "\n")
                
        self.history_text.config(state=tk.DISABLED)
            
    def add_custom_number(self):
        # カスタム数字追加処理
        try:
            number = int(self.custom_entry.get())
            if number < 1 or number > 75:
                messagebox.showerror("エラー", "1から75までの数字を入力してください")
                return
                
            if number in self.history:
                messagebox.showerror("エラー", "この数字は既に使用されています")
                return
                
            if number not in self.available_numbers:
                messagebox.showerror("エラー", "この数字は使用できません")
                return
                
            self.add_to_history(number)
            self.custom_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("エラー", "有効な数字を入力してください")

def main():
    root = tk.Tk()
    app = RandomNumberGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
