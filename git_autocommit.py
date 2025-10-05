import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import tkinter.font as tk_font


class GitGUIApp:
    """一個簡單的 Git GUI 應用程式，用於執行 Git 操作。"""

    def __init__(self, master):
        self.master = master
        master.title("Git 上傳與資料夾選擇工具")
        master.geometry("480x600")

        self.default_font_size = 12
        self.current_font = tk_font.Font(
            family="Helvetica", size=self.default_font_size
        )
        self.create_widgets()

    def create_widgets(self):
        # --- 儲存庫路徑選擇區塊 ---
        repo_frame = tk.LabelFrame(
            self.master,
            text="Git 儲存庫路徑選擇",
            padx=10,
            pady=10,
            font=self.current_font,
        )
        repo_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(
            repo_frame, text="請選擇您的 Git 儲存庫資料夾：", font=self.current_font
        ).pack(pady=5)

        repo_path_frame = tk.Frame(repo_frame)
        repo_path_frame.pack(pady=5)

        self.repo_path_entry = tk.Entry(
            repo_path_frame, width=40, font=self.current_font
        )
        self.repo_path_entry.pack(side=tk.LEFT, padx=(0, 5))

        self.select_button = tk.Button(
            repo_path_frame,
            text="選擇資料夾路徑",
            command=self.select_repo_path,
            font=self.current_font,
        )
        self.select_button.pack(side=tk.LEFT)

        # --- 自動上傳區塊 ---
        default_git_frame = tk.LabelFrame(
            self.master,
            text="一鍵上傳 Git 指令",
            padx=10,
            pady=10,
            font=self.current_font,
        )
        default_git_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(
            default_git_frame, text="請選擇一個一鍵指令：", font=self.current_font
        ).pack(pady=5)
        self.one_click_options = [
            "git pull, add, commit & push",
            "git pull --rebase",
            "git push",
        ]
        self.one_click_var = tk.StringVar(self.master)
        self.one_click_var.set(self.one_click_options[0])  # 預設值

        # 追蹤下拉式選單的變動，以更新說明文字
        self.one_click_var.trace("w", self.update_one_click_description)

        self.one_click_menu = tk.OptionMenu(
            default_git_frame, self.one_click_var, *self.one_click_options
        )
        self.one_click_menu.pack(pady=5)
        self.one_click_menu.config(font=self.current_font)

        # 新增一個標籤用於顯示指令說明
        self.one_click_description_var = tk.StringVar(self.master)
        self.one_click_description_label = tk.Label(
            default_git_frame,
            textvariable=self.one_click_description_var,
            wraplength=450,
            fg="gray",
            font=self.current_font,
        )
        self.one_click_description_label.pack(pady=5)
        self.update_one_click_description()  # 初始設定說明文字

        tk.Label(
            default_git_frame, text="請輸入 commit 訊息：", font=self.current_font
        ).pack(pady=5)

        self.default_commit_entry = tk.Entry(
            default_git_frame, width=50, font=self.current_font
        )
        self.default_commit_entry.pack(pady=5)
        self.default_commit_entry.focus_set()

        self.default_button = tk.Button(
            default_git_frame,
            text="執行選定指令",
            command=self.run_one_click_git,
            font=self.current_font,
        )
        self.default_button.pack(pady=5)

        # --- 自定義指令區塊 ---
        custom_git_frame = tk.LabelFrame(
            self.master,
            text="自定義 Git 指令",
            padx=10,
            pady=10,
            font=self.current_font,
        )
        custom_git_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(
            custom_git_frame,
            text="在此輸入您想執行的任何 Git 指令：",
            font=self.current_font,
        ).pack(pady=5)

        self.custom_command_entry = tk.Entry(
            custom_git_frame, width=50, font=self.current_font
        )
        self.custom_command_entry.pack(pady=5)

        # 使用 StringVar 來動態更新按鈕文字
        self.custom_button_text = tk.StringVar(self.master, value="執行：")
        self.custom_command_entry.bind("<KeyRelease>", self.update_custom_button_text)

        self.custom_button = tk.Button(
            custom_git_frame,
            textvariable=self.custom_button_text,
            command=self.run_custom_git,
            font=self.current_font,
        )
        self.custom_button.pack(pady=5)

        # --- 字體大小調整區塊 ---
        font_frame = tk.LabelFrame(
            self.master, text="字體大小調整", padx=10, pady=10, font=self.current_font
        )
        font_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(font_frame, text="調整字體大小：", font=self.current_font).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.font_size_var = tk.IntVar(self.master, value=self.default_font_size)
        self.font_size_spinbox = tk.Spinbox(
            font_frame,
            from_=8,
            to=24,
            textvariable=self.font_size_var,
            command=self.update_font_size,
            width=5,
            font=self.current_font,
        )
        self.font_size_spinbox.pack(side=tk.LEFT)

        # --- 狀態顯示區塊 ---
        self.status_label = tk.Label(self.master, text="", font=self.current_font)
        self.status_label.pack(pady=5)

        # --- 指令輸出日誌區塊 ---
        log_frame = tk.LabelFrame(
            self.master, text="指令輸出日誌", padx=10, pady=10, font=self.current_font
        )
        log_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame, wrap="word", state="disabled", height=10, font=self.current_font
        )
        self.log_text.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def _apply_font_recursively(self, widget):
        """遞迴地將字體應用於所有子元件。"""
        try:
            if hasattr(widget, "config"):
                # 只有可以設定字體的元件才執行
                widget.config(font=self.current_font)
        except tk.TclError:
            # 忽略無法設定字體的元件錯誤
            pass

        # 遞迴地對子元件執行
        for child in widget.winfo_children():
            self._apply_font_recursively(child)

    def update_font_size(self):
        """根據 Spinbox 的值更新所有元件的字體大小。"""
        try:
            new_size = self.font_size_var.get()
            if new_size > 0:
                self.current_font.config(size=new_size)
                # 遍歷所有元件並更新字體
                self._apply_font_recursively(self.master)
        except tk.TclError:
            pass

    def update_one_click_description(self, *args):
        """根據下拉式選單的選擇更新指令說明文字。"""
        selected_option = self.one_click_var.get()
        descriptions = {
            "git pull, add, commit & push": "此指令會依序執行 git pull --rebase, git add ., git commit 及 git push。",
            "git pull --rebase": "此指令會從遠端儲存庫拉取最新變更，並重新基礎化（rebase）您的本地提交。",
            "git push": "此指令會將您本地的提交推送到遠端儲存庫。",
        }
        self.one_click_description_var.set(descriptions.get(selected_option, ""))

    def update_custom_button_text(self, event=None):
        """根據輸入框的內容更新自定義按鈕的文字。"""
        command = self.custom_command_entry.get().strip()
        if command:
            self.custom_button_text.set(f"執行：{command}")
        else:
            self.custom_button_text.set("執行：")

    def select_repo_path(self):
        """打開資料夾選擇對話框，並將選擇的路徑填入輸入框。"""
        repo_path = filedialog.askdirectory()
        if repo_path:
            self.repo_path_entry.delete(0, tk.END)
            self.repo_path_entry.insert(0, repo_path)
            self.log("info", f"已選擇儲存庫路徑：{repo_path}")

    def log(self, type, message):
        """將訊息添加到日誌文本框。"""
        self.log_text.config(state="normal")
        if type == "error":
            self.log_text.tag_config("error", foreground="red")
            self.log_text.insert(tk.END, f"❌ 錯誤：{message}\n", "error")
        elif type == "success":
            self.log_text.tag_config("success", foreground="green")
            self.log_text.insert(tk.END, f"✅ 成功：{message}\n", "success")
        elif type == "info":
            self.log_text.insert(tk.END, f"👉 資訊：{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def run_git_command(self, command, message):
        """
        封裝執行 Git 指令的邏輯，統一處理狀態回饋和錯誤。
        """
        repo_path = self.repo_path_entry.get().strip()
        if not repo_path or not os.path.isdir(repo_path):
            messagebox.showwarning("路徑錯誤", "請先選擇一個有效的資料夾路徑。")
            self.log("error", "操作失敗：未選擇有效的資料夾路徑。")
            return None

        # 檢查是否為 Git 儲存庫
        is_git_repo = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            cwd=repo_path,
        )
        if is_git_repo.returncode != 0:
            messagebox.showerror(
                "Git 錯誤", f"選擇的路徑不是一個 Git 儲存庫：\n{repo_path}"
            )
            self.log("error", f"操作失敗：路徑 '{repo_path}' 不是一個 Git 儲存庫。")
            return None

        self.status_label.config(text=f"正在執行：{message}", fg="blue")
        self.master.update_idletasks()
        self.log("info", f"開始執行：{message}")

        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=repo_path,
            )
            self.log("info", f"標準輸出：\n{result.stdout}")
            self.log("info", f"標準錯誤：\n{result.stderr}")
            return result
        except subprocess.CalledProcessError as e:
            error_message = (
                f"❌ 錯誤：Git 操作失敗。\n\n錯誤訊息：\n{e.stdout}\n{e.stderr}"
            )
            self.status_label.config(text="❌ 失敗：請檢查終端機輸出。", fg="red")
            self.log("error", f"操作失敗。\n標準輸出：{e.stdout}\n標準錯誤：{e.stderr}")
            messagebox.showerror("Git 錯誤", error_message)
            return None
        except FileNotFoundError:
            self.status_label.config(text="❌ 失敗：找不到 'git' 指令。", fg="red")
            self.log("error", "操作失敗：找不到 'git' 指令，請確認已安裝 Git。")
            messagebox.showerror("Git 錯誤", "找不到 'git' 指令，請確認已安裝 Git。")
            return None

    def run_one_click_git(self):
        """執行根據下拉式選單選擇的 Git 指令。"""
        selected_command = self.one_click_var.get()
        self.default_button.config(state=tk.DISABLED)
        self.custom_button.config(state=tk.DISABLED)
        self.select_button.config(state=tk.DISABLED)

        try:
            if selected_command == "git pull, add, commit & push":
                # 步驟 1: git pull --rebase
                if (
                    self.run_git_command(
                        ["git", "pull", "--rebase"], "git pull --rebase"
                    )
                    is None
                ):
                    return

                # 步驟 2: git add .
                if self.run_git_command(["git", "add", "."], "git add .") is None:
                    return

                # 步驟 3: git commit -m
                commit_message = (
                    self.default_commit_entry.get().strip() or "Auto-commit"
                )
                commit_result = self.run_git_command(
                    ["git", "commit", "-m", commit_message],
                    f"git commit -m '{commit_message}'",
                )
                if commit_result is None:
                    return
                if "nothing to commit" in commit_result.stdout:
                    self.status_label.config(
                        text="✅ 成功：沒有新的變更需要提交。", fg="green"
                    )
                    self.log("success", "沒有新的變更需要提交。")
                    return

                # 步驟 4: git push
                if self.run_git_command(["git", "push"], "git push") is None:
                    return

                self.status_label.config(
                    text="🎉 成功：程式碼已上傳至 GitHub！", fg="green"
                )
                self.log("success", "所有變更已成功上傳至遠端儲存庫！")

            elif selected_command == "git pull --rebase":
                if (
                    self.run_git_command(
                        ["git", "pull", "--rebase"], "git pull --rebase"
                    )
                    is None
                ):
                    return
                self.status_label.config(
                    text="✅ 成功：已執行 git pull --rebase。", fg="green"
                )
                self.log("success", "已成功執行 git pull --rebase。")

            elif selected_command == "git push":
                if self.run_git_command(["git", "push"], "git push") is None:
                    return
                self.status_label.config(text="✅ 成功：已執行 git push。", fg="green")
                self.log("success", "已成功執行 git push。")

        finally:
            self.default_button.config(state=tk.NORMAL)
            self.custom_button.config(state=tk.NORMAL)
            self.select_button.config(state=tk.NORMAL)

    def run_custom_git(self):
        """執行使用者輸入的自定義指令。"""
        self.default_button.config(state=tk.DISABLED)
        self.custom_button.config(state=tk.DISABLED)
        self.select_button.config(state=tk.DISABLED)

        try:
            command_input = self.custom_command_entry.get().strip()
            if not command_input:
                messagebox.showwarning("輸入錯誤", "請輸入 Git 指令後再執行。")
                self.status_label.config(text="❌ 失敗：沒有輸入任何指令。")
                self.log("error", "操作失敗：沒有輸入任何指令。")
                return

            # 將輸入的字串分割成指令列表
            commands = command_input.split()
            # 如果第一個詞不是 "git"，則自動添加，確保指令在 Git 環境下執行
            if commands[0] != "git":
                commands.insert(0, "git")

            self.run_git_command(commands, command_input)
            self.status_label.config(
                text=f"✅ 成功執行指令：{command_input}", fg="green"
            )
            self.log("success", f"指令 '{command_input}' 執行完成。")

        finally:
            self.default_button.config(state=tk.NORMAL)
            self.custom_button.config(state=tk.NORMAL)
            self.select_button.config(state=tk.NORMAL)


# 主程式
if __name__ == "__main__":
    root = tk.Tk()
    app = GitGUIApp(root)
    root.mainloop()
