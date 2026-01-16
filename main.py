import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import calendar
from analysis_service import AnalysisService


class Colors:
    PRIMARY = "#3498db"
    SECONDARY = "#2ecc71"
    ACCENT = "#e67e22"
    DANGER = "#e74c3c"
    BG_LIGHT = "#ecf0f1"
    TEXT_DARK = "#2c3e50"
    WHITE = "#ffffff"
    TABLE_HEADER = "#bdc3c7"
    HOVER = "#d1d8e0"

class CalendarPopup(tk.Toplevel):
    def __init__(self, parent, on_select, initial_day=None, initial_month=None, initial_year=None):
        super().__init__(parent)
        self.on_select = on_select
        self.title("Tarih Seç")
        self.geometry("300x250")
        self.configure(bg=Colors.WHITE)
        self.resizable(False, False)
        
        # Center popup
        x = parent.winfo_rootx() + 50
        y = parent.winfo_rooty() + 50
        self.geometry(f"+{x}+{y}")

        now = datetime.now()
        self.year = int(initial_year) if initial_year else now.year
        self.month = int(initial_month) if initial_month else now.month
        
        self.create_widgets()
        
        # Modal logic
        self.transient(parent)
        self.grab_set()
        self.focus_set()

    def create_widgets(self):
        # Header (Month Year + Nav)
        header_frame = tk.Frame(self, bg=Colors.PRIMARY, height=40)
        header_frame.pack(fill="x")
        
        # Navigation Buttons: << (Year-), < (Month-), Label, > (Month+), >> (Year+)
        btn_style = {"bg": Colors.PRIMARY, "fg": "white", "bd": 0, "font": ("bold", 12)}
        
        tk.Button(header_frame, text="<<", command=self.prev_year, **btn_style).pack(side="left", padx=2)
        tk.Button(header_frame, text="<", command=self.prev_month, **btn_style).pack(side="left", padx=2)
        
        self.header_label = tk.Label(header_frame, text=f"", bg=Colors.PRIMARY, fg="white", font=("Segoe UI", 14, "bold"))
        self.header_label.pack(side="left", expand=True)
        
        tk.Button(header_frame, text=">", command=self.next_month, **btn_style).pack(side="right", padx=2)
        tk.Button(header_frame, text=">>", command=self.next_year, **btn_style).pack(side="right", padx=2)
        
        # Days
        self.cal_frame = tk.Frame(self, bg=Colors.WHITE)
        self.cal_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.update_calendar()

    def update_calendar(self):
        self.header_label.config(text=f"{calendar.month_name[self.month]} {self.year}")
        
        for widget in self.cal_frame.winfo_children():
            widget.destroy()

        # Weekdays header
        days = ["M", "T", "W", "T", "F", "S", "S"]
        days_tr = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        
        for i, d in enumerate(days_tr):
            tk.Label(self.cal_frame, text=d, bg=Colors.WHITE, font=("Segoe UI", 9, "bold")).grid(row=0, column=i, sticky="nsew")

        # Days
        month_days = calendar.monthrange(self.year, self.month)[1]
        first_weekday = calendar.monthrange(self.year, self.month)[0]
        
        row = 1
        col = first_weekday
        
        for day in range(1, month_days + 1):
            btn = tk.Button(self.cal_frame, text=str(day), command=lambda d=day: self.select_date(d),
                            bg=Colors.WHITE, relief="flat", font=("Segoe UI", 10))
            btn.grid(row=row, column=col, sticky="nsew")
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Colors.HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Colors.WHITE))

            col += 1
            if col > 6:
                col = 0
                row += 1
        
        # Grid weights
        for i in range(7): self.cal_frame.columnconfigure(i, weight=1)
        
    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.update_calendar()
        
    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.update_calendar()

    def prev_year(self):
        self.year -= 1
        self.update_calendar()

    def next_year(self):
        self.year += 1
        self.update_calendar()

    def select_date(self, day):
        self.on_select(day, self.month, self.year)
        self.destroy()


class CocukGelisimApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Çocuk Gelişim Takip ve Analiz")
        
        # Center Window
        w, h = 1100, 750
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        self.root.configure(bg=Colors.BG_LIGHT)
        
        self.setup_styles()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=Colors.BG_LIGHT)
        style.configure("Card.TFrame", background=Colors.WHITE, relief="flat")
        
        style.configure("Header.TLabel", font=("Segoe UI", 28, "bold"), background=Colors.BG_LIGHT, foreground=Colors.TEXT_DARK)
        style.configure("SubHeader.TLabel", font=("Segoe UI", 14), background=Colors.BG_LIGHT, foreground="#7f8c8d")
        
        style.configure("TLabel", font=("Segoe UI", 15), background=Colors.WHITE, foreground=Colors.TEXT_DARK)
        style.configure("TButton", font=("Segoe UI", 14, "bold"), background=Colors.PRIMARY, foreground=Colors.WHITE, borderwidth=0)
        style.map("TButton", background=[('active', '#2980b9')])
        
        style.configure("TRadiobutton", background=Colors.WHITE, font=("Segoe UI", 15))

    def create_layout(self):
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill="x", pady=(0, 20))
        ttk.Label(header_frame, text="Çocuk Gelişim Analiz Aracı", style="Header.TLabel").pack(side="left")
        
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill="both", expand=True)

        left_col = ttk.Frame(content_frame, width=300)
        left_col.pack(side="left", fill="y", padx=(0, 20))
        
        self.create_input_panel(left_col)

        right_col = ttk.Frame(content_frame)
        right_col.pack(side="left", fill="both", expand=True)
        
        self.create_result_panel(right_col)

    def open_calendar(self, day_var, month_var, year_var):
        def on_date_select(day, month, year):
            day_var.set(str(day))
            month_var.set(str(month))
            year_var.set(str(year))
        
        # Try to parse current values
        d, m, y = None, None, None
        try:
            if day_var.get() and month_var.get() and year_var.get():
                d = int(day_var.get())
                m = int(month_var.get())
                y = int(year_var.get())
        except ValueError:
            pass            
            
        CalendarPopup(self.root, on_date_select, d, m, y)

    def create_date_entry(self, parent, label_text, d_var, m_var, y_var):
        ttk.Label(parent, text=label_text).pack(anchor="w", pady=(15, 0))
        date_frame = ttk.Frame(parent, style="Card.TFrame")
        date_frame.pack(fill="x", pady=5)
        
        # Entries
        ttk.Entry(date_frame, textvariable=d_var, width=3, justify="center", font=("Segoe UI", 14)).pack(side="left", padx=2)
        ttk.Label(date_frame, text="/", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Entry(date_frame, textvariable=m_var, width=3, justify="center", font=("Segoe UI", 14)).pack(side="left", padx=2)
        ttk.Label(date_frame, text="/", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Entry(date_frame, textvariable=y_var, width=6, justify="center", font=("Segoe UI", 14)).pack(side="left", padx=2)
        
        # Calendar Button (Bigger)
        ttk.Button(date_frame, text="📅", width=4, command=lambda: self.open_calendar(d_var, m_var, y_var)).pack(side="left", padx=10)

    def create_input_panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.pack(fill="both", expand=True)
        
        ttk.Label(card, text="Çocuk Bilgileri", font=("Segoe UI", 18, "bold"), foreground=Colors.PRIMARY).pack(anchor="w", pady=(0, 15))

        # Cinsiyet
        ttk.Label(card, text="Cinsiyet").pack(anchor="w", pady=(5, 0))
        self.cinsiyet_var = tk.StringVar(value="kiz")
        radio_frame = ttk.Frame(card, style="Card.TFrame")
        radio_frame.pack(fill="x", pady=5)
        ttk.Radiobutton(radio_frame, text="Kız", variable=self.cinsiyet_var, value="kiz").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(radio_frame, text="Erkek", variable=self.cinsiyet_var, value="erkek").pack(side="left")

        # Doğum Tarihi
        self.gun_var = tk.StringVar()
        self.ay_var = tk.StringVar()
        self.yil_var = tk.StringVar()
        self.create_date_entry(card, "Doğum Tarihi (GG/AA/YYYY)", self.gun_var, self.ay_var, self.yil_var)

        # Kontrol Tarihi
        self.k_gun_var = tk.StringVar(value=str(datetime.now().day))
        self.k_ay_var = tk.StringVar(value=str(datetime.now().month))
        self.k_yil_var = tk.StringVar(value=str(datetime.now().year))
        self.create_date_entry(card, "Kontrol Tarihi (GG/AA/YYYY)", self.k_gun_var, self.k_ay_var, self.k_yil_var)

        # Boy
        ttk.Label(card, text="Boy (cm)").pack(anchor="w", pady=(15, 0))
        self.boy_var = tk.DoubleVar()
        ttk.Entry(card, textvariable=self.boy_var, font=("Segoe UI", 14)).pack(fill="x", pady=5)

        # Kilo
        ttk.Label(card, text="Kilo (kg)").pack(anchor="w", pady=(15, 0))
        self.kilo_var = tk.DoubleVar()
        ttk.Entry(card, textvariable=self.kilo_var, font=("Segoe UI", 14)).pack(fill="x", pady=5)

        # Hesapla Butonu
        ttk.Button(card, text="ANALİZ ET", command=self.hesapla).pack(fill="x", pady=(30, 0), ipady=5)

    def create_result_panel(self, parent):
        card = ttk.Frame(parent, style="Card.TFrame", padding="20")
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="Gelişim Raporu", font=("Segoe UI", 14, "bold"), foreground=Colors.PRIMARY).pack(anchor="w", pady=(0, 15))

        self.scroll_frame = tk.Canvas(card, bg=Colors.WHITE, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.scroll_frame.yview)
        self.results_content = ttk.Frame(self.scroll_frame, style="Card.TFrame")

        self.results_content.bind(
            "<Configure>",
            lambda e: self.scroll_frame.configure(
                scrollregion=self.scroll_frame.bbox("all")
            )
        )

        self.scroll_frame.create_window((0, 0), window=self.results_content, anchor="nw", width=parent.winfo_reqwidth())
        self.scroll_frame.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scroll_frame.configure(yscrollcommand=self.scrollbar.set)
        
        card.bind("<Configure>", lambda e: self.scroll_frame.create_window((0, 0), window=self.results_content, anchor="nw", width=e.width-40))

        self.lbl_placeholder = ttk.Label(self.results_content, text="Sonuçları görmek için verileri girip 'ANALİZ ET' butonuna basınız.", foreground="#95a5a6", wraplength=400, font=("Segoe UI", 14, "italic"))
        self.lbl_placeholder.pack(pady=50)


    def create_detail_table(self, parent, title, rows):
        frame = ttk.LabelFrame(parent, text=title, padding="10")
        frame.pack(fill="x", pady=10)
        
        # Header
        h_frame = ttk.Frame(frame)
        h_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(h_frame, text="Tanım", font=("Segoe UI", 11, "bold"), width=20, background=Colors.BG_LIGHT).pack(side="left", padx=5)
        ttk.Label(h_frame, text="Sonuç", font=("Segoe UI", 11, "bold"), background=Colors.BG_LIGHT).pack(side="left", padx=5)
        
        for k, v in rows:
            r_frame = ttk.Frame(frame)
            r_frame.pack(fill="x", pady=2)
            ttk.Label(r_frame, text=k, font=("Segoe UI", 12), width=20).pack(side="left", padx=5)
            
            # Use Entry for copyable text
            val_entry = tk.Entry(r_frame, font=("Segoe UI", 12, "bold"), width=30, bd=0, relief="flat", bg=Colors.WHITE, fg=Colors.TEXT_DARK, readonlybackground=Colors.WHITE)
            val_entry.pack(side="left", padx=5)
            val_entry.insert(0, v)
            val_entry.config(state="readonly")


    def hesapla(self):
        try:
            # Temizle
            for widget in self.results_content.winfo_children():
                widget.destroy()

            # Verileri Al
            gun = int(self.gun_var.get())
            ay = int(self.ay_var.get())
            yil = int(self.yil_var.get())
            
            k_gun = int(self.k_gun_var.get())
            k_ay = int(self.k_ay_var.get())
            k_yil = int(self.k_yil_var.get())
            
            boy = self.boy_var.get()
            kilo = self.kilo_var.get()
            cinsiyet = self.cinsiyet_var.get()

            results = AnalysisService.perform_analysis(gun, ay, yil, k_gun, k_ay, k_yil, boy, kilo, cinsiyet)
            
            if "error" in results:
                 messagebox.showerror("Hata", f"Girdi Hatası: {results['error']}")
                 return

            if results.get("warning"):
                 messagebox.showwarning("Uyarı", results["warning"])

            yas_str = results["yas_str"]

            # 1. BMI Alanı
            if "bmi" in results and results["bmi"]:
                bmi_data = results["bmi"]
                self.create_detail_table(self.results_content, "Çocuk BMI Hesapla", [
                    ("Yaş", yas_str),
                    ("BMI", f"{bmi_data['val']:.2f}"),
                    ("Z-Score", f"{bmi_data['z']:.2f}"),
                    ("Persentil", f"% {bmi_data['p']:.2f}")
                ])
                ttk.Label(self.results_content, text=f"BMI Durumu: {bmi_data['yorum']}", font=("Segoe UI", 10, "italic"), foreground="#7f8c8d").pack(anchor="w", padx=10)
            else:
                ttk.Label(self.results_content, text="BMI verisi bulunamadı.", foreground="red").pack()

            # 2. Kilo Alanı
            if "kilo" in results and results["kilo"]:
                kilo_data = results["kilo"]
                self.create_detail_table(self.results_content, "Çocuk Kilosu Hesapla", [
                     ("Yaş", yas_str),
                     ("Kilo", f"{kilo_data['val']} kg"),
                     ("Z-Score", f"{kilo_data['z']:.2f}"),
                     ("Persentil", f"% {kilo_data['p']:.2f}")
                ])
            else:
                 msg = ""
                 if results["yas_ay_total"] > 120:
                     msg = "Kilo verisi 10 yaş üstü için hesaplanmaz (BMI kullanın)."
                 else:
                     msg = "Kilo verisi bulunamadı."
                 
                 if msg: ttk.Label(self.results_content, text=msg, foreground="red").pack(pady=10)

            # 3. Boy Alanı
            if "boy" in results and results["boy"]:
                boy_data = results["boy"]
                self.create_detail_table(self.results_content, "Çocuk Boyu Hesapla", [
                    ("Yaş", yas_str),
                    ("Boy", f"{boy_data['val']} cm"),
                    ("Z-Score", f"{boy_data['z']:.2f}"),
                    ("Persentil", f"% {boy_data['p']:.2f}")
                ])
            else:
                ttk.Label(self.results_content, text="Boy verisi bulunamadı.", foreground="red").pack()

        except ValueError as ve:
             messagebox.showerror("Hata", f"Girdi Hatası: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = CocukGelisimApp(root)
    root.mainloop()