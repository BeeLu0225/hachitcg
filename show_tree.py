import os
import tkinter as tk
from tkinter import scrolledtext


def get_tree_string(start_path):
    """
    遞迴生成目錄樹狀圖的字串，並忽略不必要的目錄。
    """
    tree_string = ""
    ignore_dirs = set(["node_modules", "__pycache__", ".git", ".vscode"])

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        level = root.replace(start_path, "").count(os.sep)
        indent = "│   " * level

        tree_string += f"{indent}├── {os.path.basename(root)}/\n"

        sub_indent = "│   " * (level + 1)

        for file in files:
            tree_string += f"{sub_indent}├── {file}\n"

    return tree_string


def on_mousewheel(event):
    """
    處理滑鼠滾輪事件，檢查是否按住 Ctrl 鍵。
    """
    # 檢查事件物件的 state 屬性，判斷 Ctrl 鍵是否被按住
    # `event.state` 的值為一個位元遮罩 (bitwise mask)
    # 0x4 (或 4) 代表 Ctrl 鍵被按下
    if event.state & 0x4:
        text_area = event.widget
        current_font = text_area.cget("font")
        # 這裡需要處理字體名稱可能包含空格的情況
        font_parts = text_area.cget("font").split()
        font_name = font_parts[0]
        font_size = int(font_parts[1])

        if event.delta > 0:
            new_size = font_size + 2
        else:
            new_size = max(1, font_size - 2)

        text_area.configure(font=(font_name, new_size))


def show_tree_window():
    """
    建立並顯示一個 tkinter 視窗，內含檔案樹狀圖。
    """
    root = tk.Tk()
    root.title("專案檔案樹狀圖")
    root.geometry("600x800")

    text_area = scrolledtext.ScrolledText(
        root,
        wrap=tk.WORD,
        width=80,
        height=40,
        bg="black",
        fg="white",
        font=("Courier", 10),
    )
    text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # 綁定「按住 Ctrl + 滑鼠滾輪」事件
    # `<Control-MouseWheel>` 只在 Ctrl 鍵被按住時才會觸發 on_mousewheel 函式
    text_area.bind("<Control-MouseWheel>", on_mousewheel)

    tree_content = get_tree_string(".")

    text_area.insert(tk.END, tree_content)

    root.mainloop()


if __name__ == "__main__":
    show_tree_window()
