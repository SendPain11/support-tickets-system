# 🎫 Support Ticket System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

Aplikasi web berbasis **Streamlit** untuk mengelola support tickets secara efisien dan profesional. Sistem ini dirancang untuk memudahkan tim support dalam menangani permintaan, keluhan, dan pertanyaan dari pelanggan.

## 📸 Screenshot

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/667eea/ffffff?text=Dashboard+Overview)

### Daftar Tiket
![Ticket List](https://via.placeholder.com/800x400/764ba2/ffffff?text=Ticket+Management)

*Note: Ganti placeholder di atas dengan screenshot aplikasi Anda*

## ✨ Fitur Utama

### 🎯 Dashboard Interaktif
- **Real-time metrics** - Statistik tiket yang diperbarui secara otomatis
- **Visual analytics** - Grafik distribusi prioritas dan status
- **Recent tickets** - Tampilan tiket terbaru dengan color-coding

### 📝 Manajemen Tiket
- **Buat tiket baru** dengan form yang lengkap dan tervalidasi
- **Update status** tiket (Open, In Progress, Resolved, Closed)
- **Assign tickets** ke anggota tim tertentu
- **Kategori fleksibel** (Teknis, Billing, Produk, Akun, Lainnya)
- **Prioritas bertingkat** (Low, Medium, High)

### 💬 Sistem Komunikasi
- **Comment system** untuk diskusi antar tim dan pelanggan
- **Timestamp tracking** untuk setiap aktivitas
- **Email notifications** (dapat dikembangkan)

### 🔍 Pencarian & Filter
- Pencarian berdasarkan **ID tiket**
- Pencarian berdasarkan **email pelanggan**
- Pencarian berdasarkan **kata kunci**
- Filter multi-dimensi (status, prioritas, kategori)

### 📊 Analytics & Reporting
- **Tren tiket** berdasarkan waktu
- **Distribusi kategori** dan prioritas
- **Analisis waktu respons** (average, min, max)
- **Export data** ke format CSV dan JSON
- **Grafik interaktif** untuk visualisasi data

### 💾 Penyimpanan Data
- **Persistent storage** menggunakan JSON
- **Auto-save** setiap perubahan
- **Data integrity** terjaga

## 🚀 Quick Start

### Prerequisites

Pastikan Anda telah menginstal:
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/username/support-ticket-system.git
   cd support-ticket-system
   ```

2. **Buat virtual environment** (opsional tapi disarankan)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi**
   ```bash
   streamlit run support_ticket_system.py
   ```

5. **Buka browser**
   
   Aplikasi akan otomatis terbuka di `http://localhost:8501`

## 📖 Cara Penggunaan

### Membuat Tiket Baru

1. Pilih menu **"Buat Tiket Baru"** di sidebar
2. Isi form dengan informasi lengkap:
   - Nama dan email (wajib)
   - Kategori permasalahan
   - Tingkat prioritas
   - Subjek dan deskripsi detail
3. Klik **"Kirim Tiket"**
4. Sistem akan generate ID unik untuk tiket Anda

### Mengelola Tiket

1. Buka **"Daftar Tiket"** dari sidebar
2. Gunakan filter untuk menyaring tiket
3. Klik expand pada tiket untuk melihat detail
4. Update status atau assign ke tim member
5. Tambahkan komentar untuk komunikasi

### Mencari Tiket

1. Pilih **"Cari Tiket"** di sidebar
2. Pilih metode pencarian:
   - Berdasarkan ID tiket (contoh: TKT-001)
   - Berdasarkan email pelanggan
   - Berdasarkan kata kunci dalam subjek/deskripsi
3. Lihat hasil pencarian lengkap dengan detail

### Melihat Analytics

1. Buka menu **"Analitik"**
2. Lihat berbagai grafik dan statistik
3. Download laporan dalam format CSV atau JSON

## 🏗️ Struktur Project

```
support-ticket-system/
│
├── support_ticket_system.py    # Main application file
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
├── tickets_data.json           # Data storage (auto-generated)
│
└── screenshots/                # (optional) Screenshot folder
    ├── dashboard.png
    ├── ticket-list.png
    └── analytics.png
```

## 🛠️ Teknologi yang Digunakan

- **[Streamlit](https://streamlit.io/)** - Framework web app untuk Python
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation dan analysis
- **Python JSON** - Data persistence
- **HTML/CSS** - Custom styling

## 🔧 Konfigurasi

### Customisasi Kategori

Edit bagian kategori di file `support_ticket_system.py`:

```python
category = st.selectbox(
    "Kategori *",
    ["Teknis", "Billing", "Produk", "Akun", "Lainnya"]  # Edit sesuai kebutuhan
)
```

### Customisasi Departemen

```python
department = st.selectbox(
    "Departemen Tujuan",
    ["IT Support", "Customer Service", "Billing", "Technical", "Sales"]  # Edit sesuai kebutuhan
)
```

## 📊 Data Model

Setiap tiket memiliki struktur data sebagai berikut:

```json
{
  "id": "TKT-001",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+62 812-3456-7890",
  "category": "Teknis",
  "priority": "High",
  "department": "IT Support",
  "subject": "Login Error",
  "description": "Cannot login to the system...",
  "status": "Open",
  "created_at": "2024-02-04 10:30:00",
  "updated_at": "2024-02-04 10:30:00",
  "comments": [],
  "assigned_to": null
}
```

## 🎨 Customisasi Tampilan

### Mengubah Color Scheme

Edit CSS di bagian awal file:

```python
st.markdown("""
<style>
    .ticket-high { border-left-color: #dc3545; }  /* Red */
    .ticket-medium { border-left-color: #ffc107; } /* Yellow */
    .ticket-low { border-left-color: #28a745; }    /* Green */
</style>
""", unsafe_allow_html=True)
```

### Mengubah Theme Streamlit

Buat file `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

## 🚀 Deployment

### Deploy ke Streamlit Cloud

1. Push code ke GitHub repository
2. Kunjungi [share.streamlit.io](https://share.streamlit.io)
3. Login dengan GitHub
4. Deploy aplikasi dengan beberapa klik
5. Dapatkan URL publik untuk aplikasi Anda

### Deploy ke Heroku

1. Buat file `Procfile`:
   ```
   web: sh setup.sh && streamlit run support_ticket_system.py
   ```

2. Buat file `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy ke Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## 🤝 Contributing

Kontribusi selalu diterima! Berikut cara berkontribusi:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

## 📝 Roadmap

- [ ] Integrasi email notifications
- [ ] Multi-user authentication system
- [ ] File attachment support
- [ ] Advanced analytics dashboard
- [ ] SLA (Service Level Agreement) tracking
- [ ] Export PDF reports
- [ ] Mobile responsive optimization
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Integration dengan Slack/Discord
- [ ] REST API endpoints
- [ ] Database support (PostgreSQL/MongoDB)

## 🐛 Known Issues

- Upload file attachment belum fully implemented
- Email notification masih dalam development
- Mobile view perlu optimisasi lebih lanjut

## 💡 Future Improvements

- **Authentication**: Implementasi login system untuk multi-user
- **Database**: Migrasi dari JSON ke database (PostgreSQL/MongoDB)
- **Real-time**: WebSocket untuk update real-time
- **Notifications**: Email dan push notifications
- **AI Integration**: Auto-categorization menggunakan ML

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**Sendy Prismana Nurferian**

- GitHub: [@SendPain11](https://github.com/SendPain11)
- LinkedIn: [Sendy Prismana Nurferian](https://linkedin.com/in/sendy-prismana-nurferian)
- Email: sendyprisma02@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Framework yang amazing
- [Pandas](https://pandas.pydata.org/) - Data manipulation library
- Inspirasi dari berbagai ticket system populer
- Open source community

## 📞 Support

Jika Anda menemukan bug atau memiliki saran:

- **Buat Issue** di GitHub
- **Email** ke: sendyprisma02@gmail.com
- **Diskusi** di GitHub Discussions

---

<div align="center">

**⭐ Jangan lupa beri star jika project ini bermanfaat! ⭐**

Made with ❤️ using Streamlit and Python

</div>