import customtkinter as ctk
import psutil
import GPUtil

# Configuration du thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PCWatcher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Moniteur Système")
        self.geometry("480x650")
        self.resizable(False, False)

        # Titre Principal
        self.title_label = ctk.CTkLabel(self, text="📊 MONITEUR SYSTÈME", font=("Arial", 22, "bold"))
        self.title_label.pack(pady=20)

        # --- SECTION CPU ---
        self.cpu_label = ctk.CTkLabel(self, text="Processeur (CPU) : 0%", font=("Arial", 15, "bold"))
        self.cpu_label.pack(pady=5)
        self.cpu_bar = ctk.CTkProgressBar(self, width=380)
        self.cpu_bar.pack(pady=2)
        self.cpu_sub = ctk.CTkLabel(self, text="Conso : -- W", font=("Arial", 12, "italic"), text_color="gray")
        self.cpu_sub.pack(pady=(0, 15))

        # --- SECTION GPU ---
        self.gpu_label = ctk.CTkLabel(self, text="Carte Graphique (GPU) : 0%", font=("Arial", 15, "bold"))
        self.gpu_label.pack(pady=5)
        self.gpu_bar = ctk.CTkProgressBar(self, width=380)
        self.gpu_bar.pack(pady=2)
        self.gpu_sub = ctk.CTkLabel(self, text="Conso : -- W", font=("Arial", 12, "italic"), text_color="gray")
        self.gpu_sub.pack(pady=(0, 15))

        # --- SECTION RAM ---
        self.ram_label = ctk.CTkLabel(self, text="Mémoire (RAM) : 0%", font=("Arial", 15, "bold"))
        self.ram_label.pack(pady=5)
        self.ram_bar = ctk.CTkProgressBar(self, width=380)
        self.ram_bar.pack(pady=2)
        self.ram_sub = ctk.CTkLabel(self, text="Utilisé : -- Go / -- Go", font=("Arial", 12, "italic"), text_color="gray")
        self.ram_sub.pack(pady=(0, 15))

        # --- SECTION STOCKAGE ---
        self.disk_label = ctk.CTkLabel(self, text="Disque (C:) : 0%", font=("Arial", 15, "bold"))
        self.disk_label.pack(pady=5)
        self.disk_bar = ctk.CTkProgressBar(self, width=380)
        self.disk_bar.pack(pady=2)
        self.disk_sub = ctk.CTkLabel(self, text="Espace : -- Go libres", font=("Arial", 12, "italic"), text_color="gray")
        self.disk_sub.pack(pady=(0, 15))

        # Lancer l'actualisation
        self.update_stats()

    def get_progress_color(self, percentage):
        if percentage < 50: return "#2ecc71"  # Vert
        elif percentage < 80: return "#e67e22" # Orange
        else: return "#e74c3c"                # Rouge

    def update_stats(self):
        # 1. CPU
        cpu_usage = psutil.cpu_percent()
        # Estimation approximative du wattage CPU basée sur la charge (ex: TDP max de 65W à 100%)
        # Note : Pour les watts exacts hardware, Windows demande un accès noyau spécifique (ex: OpenHardwareMonitor API)
        cpu_watts = (cpu_usage / 100) * 65  
        
        self.cpu_label.configure(text=f"Processeur (CPU) : {cpu_usage}%")
        self.cpu_sub.configure(text=f"Consommation estimée : {cpu_watts:.1f} W")
        self.cpu_bar.set(cpu_usage / 100)
        self.cpu_bar.configure(progress_color=self.get_progress_color(cpu_usage))

        # 2. GPU
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_usage = gpus[0].load * 100
            # Certains GPU rapportent la conso en Watts, sinon on l'estime sur une base de 200W max
            gpu_watts = (gpu_usage / 100) * 200 
            self.gpu_label.configure(text=f"Carte Graphique (GPU) : {gpu_usage:.1f}%")
            self.gpu_sub.configure(text=f"Estimation Puissance : {gpu_watts:.1f} W")
            self.gpu_bar.set(gpu_usage / 100)
            self.gpu_bar.configure(progress_color=self.get_progress_color(gpu_usage))
        else:
            self.gpu_label.configure(text="Carte Graphique (GPU) : Introuvable")
            self.gpu_sub.configure(text="Pas de données de consommation")

        # 3. RAM
        ram = psutil.virtual_memory()
        ram_used_gb = ram.used / (1024 ** 3)
        ram_total_gb = ram.total / (1024 ** 3)
        
        self.ram_label.configure(text=f"Mémoire (RAM) : {ram.percent}%")
        self.ram_sub.configure(text=f"Utilisé : {ram_used_gb:.1f} Go / {ram_total_gb:.1f} Go")
        self.ram_bar.set(ram.percent / 100)
        self.ram_bar.configure(progress_color=self.get_progress_color(ram.percent))

        # 4. DISQUE
        disk = psutil.disk_usage('C:')
        disk_free_gb = disk.free / (1024 ** 3)
        disk_total_gb = disk.total / (1024 ** 3)
        
        self.disk_label.configure(text=f"Disque (C:) : {disk.percent}%")
        self.disk_sub.configure(text=f"Libre : {disk_free_gb:.1f} Go sur {disk_total_gb:.1f} Go au total")
        self.disk_bar.set(disk.percent / 100)
        self.disk_bar.configure(progress_color=self.get_progress_color(disk.percent))

        # Relancer dans 1 seconde
        self.after(1000, self.update_stats)

if __name__ == "__main__":
    app = PCWatcher()
    app.mainloop()