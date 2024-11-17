import tkinter as tk
from tkinter import ttk
import requests
import time
from datetime import datetime
import threading

class CryptoTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Kripto Para Takip Uygulaması")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Arka plan rengi
        self.root.configure(bg="#c6e2ff")  # Koyu mavi-gri arka plan
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('clam')  # Modern görünüm
        
        # Treeview stili
        style.configure("Treeview",
                       background="#34495E",
                       foreground="white",
                       fieldbackground="#b9d3ee",
                       rowheight=30,
                       font=('Arial', 11))
        
        style.configure("Treeview.Heading",
                       background="#2980B9",
                       foreground="white",
                       font=('Arial', 12, 'bold'))
        
        # Ana frame
        main_frame = tk.Frame(root, bg="#2C3E50")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Başlık
        title_label = tk.Label(main_frame, 
                             text="KRİPTO PARA TAKİP UYGULAMASI",
                             font=("Arial", 24, "bold"),
                             fg="#ECF0F1",  # Beyaza yakın
                             bg="#6c7b8b")  # Arka planla aynı
        title_label.pack(pady=20)

        # Son güncelleme zamanı etiketi
        self.time_label = tk.Label(main_frame,
                                 text="",
                                 font=("Arial", 12),
                                 fg="#9fb6cd",  # Açık mavi
                                 bg="#6c7b8b")
        self.time_label.pack(pady=10)

        # Treeview frame
        tree_frame = tk.Frame(main_frame, bg="#6c7b8b")
        tree_frame.pack(pady=20)

        # Treeview (tablo) oluşturma
        columns = ("Kripto Para", "USD", "TRY", "Değişim (%24s)")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Sütun başlıkları
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        # Treeview ve scrollbar yerleştirme
        self.tree.pack(side="left")
        scrollbar.pack(side="right", fill="y")

        # Tag'ler için renk ayarları
        self.tree.tag_configure("positive", foreground="#2ECC71")  # Yeşil
        self.tree.tag_configure("negative", foreground="#E74C3C")  # Kırmızı

        # Yenile butonu
        refresh_button = tk.Button(main_frame,
                                 text="YENİLE",
                                 command=self.manual_refresh,
                                 font=("Arial", 12, "bold"),
                                 bg="#3498DB",
                                 fg="white",
                                 activebackground="#2980B9",
                                 activeforeground="white",
                                 width=15,
                                 height=2,
                                 relief=tk.RAISED,
                                 bd=0)
        refresh_button.pack(pady=20)

        # Durum çubuğu
        self.status_label = tk.Label(main_frame,
                                   text="",
                                   font=("Arial", 11),
                                   fg="#ECF0F1",
                                   bg="#2C3E50")
        self.status_label.pack(pady=10)

        # Takip edilecek kripto paralar
        self.crypto_ids = ['bitcoin', 'ethereum', 'binancecoin', 'ripple', 'cardano','solana', 'dogecoin','polkadot','avalanche-2','tron','chainlink','polygon','litecoin','shiba-inu','uniswap','aptos']
        
        # Hover efekti için binding
        refresh_button.bind("<Enter>", lambda e: refresh_button.config(bg="#2980B9"))
        refresh_button.bind("<Leave>", lambda e: refresh_button.config(bg="#3498DB"))
        
        # Otomatik güncelleme için thread başlatma
        self.update_thread = threading.Thread(target=self.auto_update, daemon=True)
        self.update_thread.start()

    def get_crypto_prices(self):
        try:
            ids = ",".join(self.crypto_ids)
            response = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={ids}"
                f"&vs_currencies=usd,try&include_24h_change=true"
            )
            return response.json()
        except Exception as e:
            self.status_label.config(text=f"Hata: {str(e)}", fg="#E74C3C")
            return None

    def update_prices(self):
        # Tüm mevcut satırları temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Yeni fiyatları al
        data = self.get_crypto_prices()
        if data:
            for crypto_id in self.crypto_ids:
                if crypto_id in data:
                    crypto_data = data[crypto_id]
                    change_24h = crypto_data.get('usd_24h_change', 0)
                    change_text = f"{change_24h:.2f}%" if change_24h else "N/A"
                    
                    # Değişim rengi için tag belirleme
                    tag = "positive" if change_24h and change_24h > 0 else "negative"
                    
                    self.tree.insert("", "end", values=(
                        crypto_id.title(),
                        f"${crypto_data['usd']:,.2f}",
                        f"₺{crypto_data['try']:,.2f}",
                        change_text
                    ), tags=(tag,))

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=f"Son Güncelleme: {current_time}")
            self.status_label.config(text="Veriler başarıyla güncellendi", fg="#2ECC71")

    def manual_refresh(self):
        self.update_prices()

    def auto_update(self):
        while True:
            self.root.after(0, self.update_prices)
            time.sleep(60)

def main():
    root = tk.Tk()
    app = CryptoTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()

