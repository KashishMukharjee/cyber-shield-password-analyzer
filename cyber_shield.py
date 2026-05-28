import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import string
from datetime import datetime
import math

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class CyberShield:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CYBER SHIELD - Password Strength Analyzer")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state("zoomed")
        self.root.configure(fg_color="#000000")
        
        self.pulse = 0
        self.animation_running = False
        
        self.setup_ui()
        self.setup_animations()
        self.bind_events()
        self.update_datetime()
        
    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#000000", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        self.background = tk.Canvas(self.main_frame, bg="#000000", highlightthickness=0)
        self.background.pack(fill="both", expand=True)
        
        self.particles = []
        for _ in range(50):
            x, y = random.randint(0, self.root.winfo_screenwidth()), random.randint(0, self.root.winfo_screenheight())
            size = random.randint(1, 3)
            particle = self.background.create_oval(x, y, x+size, y+size, fill="#00ffea", outline="")
            self.particles.append((particle, random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)))
        
        self.glow_frame = ctk.CTkFrame(self.main_frame, fg_color="#05050f", corner_radius=0, border_width=2, border_color="#00ffea")
        self.glow_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.92)
        
        self.header = ctk.CTkFrame(self.glow_frame, fg_color="#0d0d1d", height=140, corner_radius=0)
        self.header.pack(fill="x", pady=(20, 15), padx=20)
        
        self.title_label = ctk.CTkLabel(self.header, text="🛡 CYBER SHIELD", font=("Orbitron", 56, "bold"), text_color="#00ffea")
        self.title_label.pack(pady=(25, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.header, text="ADVANCED PASSWORD SECURITY ANALYZER", font=("Segoe UI", 16), text_color="#60a5fa")
        self.subtitle_label.pack()
        
        self.datetime_label = ctk.CTkLabel(self.header, text="", font=("Consolas", 12), text_color="#40e0d0")
        self.datetime_label.pack(pady=(8, 0))
        
        self.status_frame = ctk.CTkFrame(self.glow_frame, fg_color="#001a1a", height=65, corner_radius=0)
        self.status_frame.pack(fill="x", pady=(0, 10), padx=20)
        
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", font=("Arial", 28, "bold"), text_color="#00ff00")
        self.status_dot.pack(side="left", padx=(20, 10))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="SYSTEM SECURE", font=("Orbitron", 18, "bold"), text_color="#00ff00")
        self.status_label.pack(side="left")
        
        self.level_label = ctk.CTkLabel(self.status_frame, text="SECURITY: MAXIMUM", font=("Consolas", 12), text_color="#40e0d0")
        self.level_label.pack(side="right", padx=20)
        
        self.content = ctk.CTkFrame(self.glow_frame, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)
        
        self.input_panel = ctk.CTkFrame(self.content, fg_color="#0f0f1f", corner_radius=20, border_width=1, border_color="#00aaff")
        self.input_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.input_header = ctk.CTkFrame(self.input_panel, fg_color="#1a1a2e", height=55, corner_radius=15)
        self.input_header.pack(fill="x", pady=(20, 15), padx=20)
        
        self.input_title = ctk.CTkLabel(self.input_header, text="PASSWORD ANALYSIS", font=("Orbitron", 20, "bold"), text_color="#00ffea")
        self.input_title.pack(expand=True)
        
        self.pw_frame = ctk.CTkFrame(self.input_panel, fg_color="transparent")
        self.pw_frame.pack(pady=(0, 15), padx=25, fill="x")
        
        self.pw_label = ctk.CTkLabel(self.pw_frame, text="ENTER PASSWORD:", font=("Orbitron", 13, "bold"), text_color="#40e0d0")
        self.pw_label.pack(anchor="w", pady=(0, 8))
        
        self.entry_row = ctk.CTkFrame(self.pw_frame, fg_color="transparent")
        self.entry_row.pack(fill="x")
        
        self.password_entry = ctk.CTkEntry(self.entry_row, height=55, font=("Consolas", 18), fg_color="#000000", border_color="#00ffea", text_color="#ffffff", show="●")
        self.password_entry.pack(side="left", fill="x", expand=True)
        
        self.eye_btn = ctk.CTkButton(self.entry_row, text="👁", width=50, height=55, font=("Segoe UI", 18), fg_color="#1a1a2e", hover_color="#00ffea", text_color="#00ffea", corner_radius=12, border_color="#00ffea", border_width=1, command=self.toggle_pw)
        self.eye_btn.pack(side="right", padx=(10, 0))
        
        self.btn_panel = ctk.CTkFrame(self.input_panel, fg_color="transparent")
        self.btn_panel.pack(pady=(10, 20), padx=15, fill="x")
        
        self.analyze_btn = ctk.CTkButton(self.btn_panel, text="ANALYZE", font=("Orbitron", 15, "bold"), fg_color="#00aa88", hover_color="#00ffea", text_color="#000000", height=50, width=150, corner_radius=12, command=self.analyze)
        self.analyze_btn.pack(side="left", padx=5)
        
        self.gen_btn = ctk.CTkButton(self.btn_panel, text="GENERATE", font=("Orbitron", 15, "bold"), fg_color="#1a1a2e", hover_color="#00aa88", text_color="#00ffea", height=50, width=150, corner_radius=12, border_color="#00ffea", border_width=1, command=self.generate)
        self.gen_btn.pack(side="left", padx=5)
        
        self.reset_btn = ctk.CTkButton(self.btn_panel, text="RESET", font=("Orbitron", 15, "bold"), fg_color="#1a1a2e", hover_color="#ff4444", text_color="#ff6b6b", height=50, width=120, corner_radius=12, border_color="#ff6b6b", border_width=1, command=self.reset)
        self.reset_btn.pack(side="left", padx=5)
        
        self.strength_sec = ctk.CTkFrame(self.input_panel, fg_color="transparent")
        self.strength_sec.pack(pady=(15, 10), padx=25, fill="x")
        
        self.strength_lbl = ctk.CTkLabel(self.strength_sec, text="STRENGTH LEVEL", font=("Orbitron", 16, "bold"), text_color="#ffffff")
        self.strength_lbl.pack(anchor="w", pady=(0, 10))
        
        self.strength_box = ctk.CTkFrame(self.strength_sec, fg_color="#000000", height=55, corner_radius=12, border_width=1, border_color="#333333")
        self.strength_box.pack(fill="x", pady=(0, 15))
        
        self.strength_indicator = ctk.CTkLabel(self.strength_box, text="— NOT ANALYZED —", font=("Orbitron", 20, "bold"), text_color="#606060")
        self.strength_indicator.pack(expand=True)
        
        self.progress_bg = ctk.CTkFrame(self.input_panel, fg_color="#000000", height=22, corner_radius=15)
        self.progress_bg.pack(fill="x", padx=25, pady=(10, 25))
        
        self.progress_fill = tk.Canvas(self.progress_bg, bg="#000000", highlightthickness=0, height=22)
        self.progress_fill.pack(fill="x")
        self.progress_rect = self.progress_fill.create_rectangle(0, 0, 0, 22, fill="#00ffea", outline="")
        
        self.score_label = ctk.CTkLabel(self.input_panel, text="SCORE: 0/100", font=("Orbitron", 26, "bold"), text_color="#00ffea")
        self.score_label.pack(pady=(0, 20))
        
        self.result_panel = ctk.CTkFrame(self.content, fg_color="#0f0f1f", corner_radius=20, border_width=1, border_color="#00aaff")
        self.result_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        self.result_header = ctk.CTkFrame(self.result_panel, fg_color="#1a1a2e", height=55, corner_radius=15)
        self.result_header.pack(fill="x", pady=(20, 15), padx=20)
        
        self.result_title = ctk.CTkLabel(self.result_header, text="SECURITY VERIFICATION", font=("Orbitron", 20, "bold"), text_color="#00ffea")
        self.result_title.pack(expand=True)
        
        self.checks_box = ctk.CTkScrollableFrame(self.result_panel, fg_color="#000000", corner_radius=15)
        self.checks_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.check_items = {}
        checks = [("Min 8 Characters", "length"), ("Uppercase (A-Z)", "uppercase"), ("Lowercase (a-z)", "lowercase"), ("Number (0-9)", "number"), ("Special ( !@#$ )", "special"), ("Not Common", "common")]
        
        for txt, key in checks:
            row = ctk.CTkFrame(self.checks_box, fg_color="#1a1a2e", height=55, corner_radius=12)
            row.pack(fill="x", pady=5)
            row.pack_propagate(False)
            
            lbl = ctk.CTkLabel(row, text=txt, font=("Segoe UI", 13), text_color="#cccccc")
            lbl.pack(side="left", padx=20)
            
            ind = ctk.CTkLabel(row, text="○", font=("Arial", 22, "bold"), text_color="#ff4444", width=35)
            ind.pack(side="right", padx=20)
            
            self.check_items[key] = ind
            
        self.suggest_panel = ctk.CTkFrame(self.result_panel, fg_color="#000000", corner_radius=15)
        self.suggest_panel.pack(fill="x", padx=15, pady=(0, 20))
        
        self.suggest_title = ctk.CTkLabel(self.suggest_panel, text="RECOMMENDATIONS", font=("Orbitron", 16, "bold"), text_color="#40e0d0")
        self.suggest_title.pack(pady=(15, 5))
        
        self.suggestions = ctk.CTkTextbox(self.suggest_panel, height=120, font=("Segoe UI", 12), fg_color="#0d0d1d", text_color="#ffffff", corner_radius=10, wrap="word")
        self.suggestions.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.pw_visible = False
        self.analyzed = False
        
    def setup_animations(self):
        self.animate_particles()
        self.animate_border()
        
    def animate_particles(self):
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        
        for p, dx, dy in self.particles:
            self.background.move(p, dx, dy)
            coords = self.background.coords(p)
            if coords[0] < 0 or coords[2] > w:
                self.background.move(p, -2*dx, 0)
            if coords[1] < 0 or coords[3] > h:
                self.background.move(p, 0, -2*dy)
                
        self.root.after(100, self.animate_particles)
        
    def animate_border(self):
        colors = ["#00ffea", "#00d9ff", "#00bfff"]
        idx = int(self.pulse * 3) % len(colors)
        try:
            self.glow_frame.configure(border_color=colors[idx])
        except:
            pass
        self.pulse += 0.02
        self.root.after(100, self.animate_border)
        
    def bind_events(self):
        self.password_entry.bind("<KeyRelease>", lambda e: setattr(self, "analyzed", True) if self.password_entry.get() else None)
        self.password_entry.bind("<KeyRelease>", self.realtime_analyze)
        
    def realtime_analyze(self, event=None):
        if self.analyzed and len(self.password_entry.get()) >= 3:
            self.analyze()
            
    def update_datetime(self):
        now = datetime.now().strftime("%Y-%m-%d │ %H:%M:%S")
        self.datetime_label.configure(text=f"⏱ {now}")
        self.root.after(1000, self.update_datetime)
        
    def toggle_pw(self):
        self.pw_visible = not self.pw_visible
        self.password_entry.configure(show="" if self.pw_visible else "●")
        
    def analyze(self):
        pw = self.password_entry.get()
        if not pw:
            return
            
        score, checks = self.get_score(pw)
        self.update_ui(score, checks)
        self.animate_bar(score)
        
    def get_score(self, pw):
        score = 0
        checks = {
            "length": len(pw) >= 8,
            "uppercase": any(c.isupper() for c in pw),
            "lowercase": any(c.islower() for c in pw),
            "number": any(c.isdigit() for c in pw),
            "special": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pw),
            "common": pw.lower() not in self.common_passwords()
        }
        
        if checks["length"]: score += 15
        if len(pw) >= 12: score += 10
        if len(pw) >= 16: score += 10
        if checks["uppercase"]: score += 15
        if checks["lowercase"]: score += 15
        if checks["number"]: score += 15
        if checks["special"]: score += 15
        if checks["common"]: score += 15
        
        if score >= 90:
            self.status_label.configure(text="SYSTEM SECURE", text_color="#00ff00")
            self.status_dot.configure(text_color="#00ff00")
            self.level_label.configure(text="SECURITY: MAXIMUM")
        else:
            self.status_label.configure(text="VULNERABLE", text_color="#ff4444")
            self.status_dot.configure(text_color="#ff4444")
            self.level_label.configure(text="SECURITY: COMPROMISED")
            
        return min(score, 100), checks
        
    def common_passwords(self):
        return {"password", "password1", "password123", "123456", "12345678", "qwerty", "abc123", "admin", "letmein", "welcome", "monkey", "dragon", "master", "login", "iloveyou", "shadow", "sunshine", "princess", "football", "superman", "batman", "trustno1", "passw0rd", "admin123", "qwerty123"}
        
    def update_ui(self, score, checks):
        if score >= 90:
            txt, color = "VERY STRONG", "#00ff00"
        elif score >= 70:
            txt, color = "STRONG", "#7cfc00"
        elif score >= 50:
            txt, color = "MEDIUM", "#ffd700"
        elif score >= 30:
            txt, color = "WEAK", "#ff8c00"
        else:
            txt, color = "VERY WEAK", "#ff4444"
            
        self.strength_indicator.configure(text=txt, text_color=color)
        self.score_label.configure(text=f"SCORE: {score}/100")
        
        for k, v in checks.items():
            self.check_items[k].configure(text="✓" if v else "✗", text_color="#00ff00" if v else "#ff4444")
            
        sgs = self.get_suggestions(checks)
        self.suggestions.delete("0.0", "end")
        self.suggestions.insert("0.0", "\n".join(sgs))
        
    def get_suggestions(self, checks):
        sgs = []
        if not checks["length"]: sgs.append("⚠ Increase length to 8+ characters")
        elif len(self.password_entry.get()) < 12: sgs.append("ℹ Use 12+ chars for better security")
        if not checks["uppercase"]: sgs.append("⚠ Add uppercase letters (A-Z)")
        if not checks["lowercase"]: sgs.append("⚠ Add lowercase letters (a-z)")
        if not checks["number"]: sgs.append("⚠ Include numbers (0-9)")
        if not checks["special"]: sgs.append("⚠ Add special characters (!@#$)")
        if not checks["common"]: sgs.append("⚠ Avoid common passwords")
        if not sgs:
            sgs = ["✓ All security checks passed", "✓ Password is highly secure"]
        return sgs
        
    def animate_bar(self, target):
        if self.animation_running: return
        self.animation_running = True
        cur = 0
        
        def step():
            nonlocal cur
            if cur < target:
                cur += 3
                w = self.progress_bg.winfo_width() * (cur / 100)
                self.progress_fill.coords(self.progress_rect, 0, 0, w, 22)
                colors = ["#ff4444", "#ff8c00", "#ffd700", "#7cfc00", "#00ff00"]
                cidx = min(int(cur / 25), 4)
                self.progress_fill.itemconfig(self.progress_rect, fill=colors[cidx])
                self.root.after(15, step)
            else:
                w = self.progress_bg.winfo_width() * (target / 100)
                self.progress_fill.coords(self.progress_rect, 0, 0, w, 22)
                self.animation_running = False
                
        step()
        
    def generate(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        pw = [random.choice(string.ascii_uppercase), random.choice(string.ascii_lowercase), random.choice(string.digits), random.choice("!@#$%^&*")]
        for _ in range(random.randint(12, 16) - 4):
            pw.append(random.choice(chars))
        random.shuffle(pw)
        gen = "".join(pw)
        
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, gen)
        self.pw_visible = False
        self.password_entry.configure(show="●")
        self.analyze()
        
    def reset(self):
        self.password_entry.delete(0, "end")
        self.progress_fill.coords(self.progress_rect, 0, 0, 0, 22)
        self.strength_indicator.configure(text="— NOT ANALYZED —", text_color="#606060")
        self.score_label.configure(text="SCORE: 0/100")
        self.suggestions.delete("0.0", "end")
        for k in self.check_items:
            self.check_items[k].configure(text="○", text_color="#ff4444")
        self.status_label.configure(text="SYSTEM SECURE", text_color="#00ff00")
        self.status_dot.configure(text_color="#00ff00")
        self.level_label.configure(text="SECURITY: MAXIMUM")
        self.analyzed = False
        
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CyberShield().run()