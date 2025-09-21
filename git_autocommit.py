import subprocess
import tkinter as tk
from tkinter import messagebox


def git_push_simplified():
    """
    執行 git add, git commit, git push 的指令，並在視窗中顯示進度。
    """
    commit_message = entry.get()

    if not commit_message:
        commit_message = "Auto-commit"

    # 設定初始狀態訊息
    status_label.config(text="正在處理...")

    try:
        # 指令 1: git add .
        # 用途：將所有變更加入到暫存區
        status_label.config(text="正在執行：git add .")
        root.update_idletasks()  # 更新視窗，立即顯示訊息
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)

        # 指令 2: git commit -m "commit_message"
        # 用途：將暫存區的變更提交到本地倉庫
        status_label.config(text=f"正在執行：git commit -m '{commit_message}'")
        root.update_idletasks()
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )

        # 指令 3: git push
        # 用途：將本地提交推送到遠端倉庫
        status_label.config(text="正在執行：git push")
        root.update_idletasks()
        subprocess.run(["git", "push"], check=True, capture_output=True, text=True)

        # 成功訊息
        status_label.config(text="🎉 成功：程式碼已上傳至 GitHub！")

    except subprocess.CalledProcessError as e:
        # 處理任何可能發生的 Git 指令錯誤
        error_message = f"❌ 錯誤：Git 操作失敗。\n\n錯誤訊息：\n{e.stdout}\n{e.stderr}"
        status_label.config(text="❌ 失敗：請檢查終端機輸出。")
        messagebox.showerror("Git 錯誤", error_message)
    except FileNotFoundError:
        # 處理找不到 git 執行檔的情況
        status_label.config(text="❌ 失敗：找不到 'git' 指令。")
        messagebox.showerror("Git 錯誤", "找不到 'git' 指令，請確認已安裝 Git。")


# 建立主視窗
root = tk.Tk()
root.title("Git 上傳工具")
root.geometry("400x150")

# 建立說明文字
label = tk.Label(root, text="請輸入 commit 訊息：")
label.pack(pady=10)

# 建立輸入框
entry = tk.Entry(root, width=50)
entry.pack(pady=5)
entry.focus_set()

# 建立按鈕
button = tk.Button(root, text="上傳至 GitHub", command=git_push_simplified)
button.pack(pady=5)

# 建立狀態標籤
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# 啟動主迴圈
root.mainloop()
