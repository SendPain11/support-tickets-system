import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# Konfigurasi halaman
st.set_page_config(
    page_title="Support Ticket System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
<style>
    .ticket-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid;
        margin: 10px 0;
        background-color: #f8f9fa;
    }
    .ticket-high { border-left-color: #dc3545; }
    .ticket-medium { border-left-color: #ffc107; }
    .ticket-low { border-left-color: #28a745; }
    
    .status-open { background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px; }
    .status-progress { background-color: #ffc107; color: white; padding: 5px 10px; border-radius: 5px; }
    .status-resolved { background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; }
    .status-closed { background-color: #6c757d; color: white; padding: 5px 10px; border-radius: 5px; }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi file penyimpanan
TICKETS_FILE = "tickets_data.json"

def load_tickets():
    """Memuat data tiket dari file JSON"""
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tickets(tickets):
    """Menyimpan data tiket ke file JSON"""
    with open(TICKETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tickets, f, ensure_ascii=False, indent=2)

def generate_ticket_id(tickets):
    """Generate ID tiket unik"""
    if not tickets:
        return "TKT-001"
    last_id = max([int(t['id'].split('-')[1]) for t in tickets])
    return f"TKT-{str(last_id + 1).zfill(3)}"

# Inisialisasi session state
if 'tickets' not in st.session_state:
    st.session_state.tickets = load_tickets()

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Dashboard"

# Sidebar Navigation
with st.sidebar:
    st.title("🎫 Support Ticket System")
    st.markdown("---")
    
    view_mode = st.radio(
        "Menu Navigasi",
        ["Dashboard", "Buat Tiket Baru", "Daftar Tiket", "Cari Tiket", "Analitik"],
        index=["Dashboard", "Buat Tiket Baru", "Daftar Tiket", "Cari Tiket", "Analitik"].index(st.session_state.view_mode)
    )
    st.session_state.view_mode = view_mode
    
    st.markdown("---")
    st.markdown("### 📊 Statistik Cepat")
    
    tickets = st.session_state.tickets
    total_tickets = len(tickets)
    open_tickets = len([t for t in tickets if t['status'] == 'Open'])
    resolved_tickets = len([t for t in tickets if t['status'] == 'Resolved'])
    
    st.metric("Total Tiket", total_tickets)
    st.metric("Tiket Terbuka", open_tickets)
    st.metric("Tiket Selesai", resolved_tickets)
    
    st.markdown("---")
    st.markdown("### ℹ️ Informasi")
    st.info("Sistem ini membantu Anda mengelola support tickets dengan mudah dan efisien.")

# DASHBOARD
if st.session_state.view_mode == "Dashboard":
    st.title("🚨 Dashboard Support Tickets")
    
    tickets = st.session_state.tickets
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Tiket", len(tickets))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        open_count = len([t for t in tickets if t['status'] == 'Open'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Terbuka", open_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        progress_count = len([t for t in tickets if t['status'] == 'In Progress'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Dalam Proses", progress_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        resolved_count = len([t for t in tickets if t['status'] == 'Resolved'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Selesai", resolved_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Tickets
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Tiket Terbaru")
        if tickets:
            recent_tickets = sorted(tickets, key=lambda x: x['created_at'], reverse=True)[:5]
            
            for ticket in recent_tickets:
                priority_class = f"ticket-{ticket['priority'].lower()}"
                status_class = f"status-{ticket['status'].lower().replace(' ', '')}"
                
                st.markdown(f"""
                <div class="ticket-card {priority_class}">
                    <h4>{ticket['id']} - {ticket['subject']}</h4>
                    <p><strong>Kategori:</strong> {ticket['category']} | <strong>Prioritas:</strong> {ticket['priority']}</p>
                    <p><strong>Status:</strong> <span class="{status_class}">{ticket['status']}</span></p>
                    <p><strong>Dibuat:</strong> {ticket['created_at']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada tiket yang dibuat.")
    
    with col2:
        st.subheader("📈 Distribusi Prioritas")
        if tickets:
            priority_counts = pd.DataFrame(tickets)['priority'].value_counts()
            st.bar_chart(priority_counts)
        else:
            st.info("Tidak ada data untuk ditampilkan")
        
        st.subheader("🔄 Distribusi Status")
        if tickets:
            status_counts = pd.DataFrame(tickets)['status'].value_counts()
            st.bar_chart(status_counts)

# BUAT TIKET BARU
elif st.session_state.view_mode == "Buat Tiket Baru":
    st.title("✏️ Buat Tiket Support Baru")
    
    with st.form("new_ticket_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nama Anda *", placeholder="Masukkan nama lengkap")
            email = st.text_input("Email *", placeholder="email@example.com")
            phone = st.text_input("No. Telepon", placeholder="+62 812-3456-7890")
        
        with col2:
            category = st.selectbox(
                "Kategori *",
                ["Teknis", "Billing", "Produk", "Akun", "Lainnya"]
            )
            priority = st.selectbox(
                "Prioritas *",
                ["Low", "Medium", "High"]
            )
            department = st.selectbox(
                "Departemen Tujuan",
                ["IT Support", "Customer Service", "Billing", "Technical", "Sales"]
            )
        
        subject = st.text_input("Subjek Permasalahan *", placeholder="Jelaskan masalah Anda secara singkat")
        description = st.text_area(
            "Deskripsi Detail *",
            placeholder="Jelaskan masalah Anda secara detail...",
            height=150
        )
        
        attachment = st.file_uploader("Lampiran (opsional)", type=['png', 'jpg', 'pdf', 'docx'])
        
        st.markdown("**_* = wajib diisi_**")
        
        submitted = st.form_submit_button("🚀 Kirim Tiket", use_container_width=True)
        
        if submitted:
            if not name or not email or not subject or not description:
                st.error("❌ Mohon lengkapi semua field yang wajib diisi!")
            else:
                new_ticket = {
                    'id': generate_ticket_id(st.session_state.tickets),
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'category': category,
                    'priority': priority,
                    'department': department,
                    'subject': subject,
                    'description': description,
                    'status': 'Open',
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'comments': [],
                    'assigned_to': None
                }
                
                st.session_state.tickets.append(new_ticket)
                save_tickets(st.session_state.tickets)
                
                st.success(f"✅ Tiket berhasil dibuat! ID Tiket: **{new_ticket['id']}**")
                st.balloons()
                
                with st.expander("📄 Detail Tiket"):
                    st.json(new_ticket)

# DAFTAR TIKET
elif st.session_state.view_mode == "Daftar Tiket":
    st.title("📋 Daftar Semua Tiket")
    
    tickets = st.session_state.tickets
    
    if tickets:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "Filter Status",
                ["Open", "In Progress", "Resolved", "Closed"],
                default=["Open", "In Progress"]
            )
        
        with col2:
            priority_filter = st.multiselect(
                "Filter Prioritas",
                ["Low", "Medium", "High"],
                default=["Low", "Medium", "High"]
            )
        
        with col3:
            category_filter = st.multiselect(
                "Filter Kategori",
                ["Teknis", "Billing", "Produk", "Akun", "Lainnya"],
                default=["Teknis", "Billing", "Produk", "Akun", "Lainnya"]
            )
        
        # Filter tickets
        filtered_tickets = [
            t for t in tickets
            if t['status'] in status_filter
            and t['priority'] in priority_filter
            and t['category'] in category_filter
        ]
        
        st.markdown(f"**Menampilkan {len(filtered_tickets)} dari {len(tickets)} tiket**")
        st.markdown("---")
        
        # Display tickets
        for ticket in sorted(filtered_tickets, key=lambda x: x['created_at'], reverse=True):
            with st.expander(f"🎫 {ticket['id']} - {ticket['subject']} ({ticket['status']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Nama:** {ticket['name']}")
                    st.markdown(f"**Email:** {ticket['email']}")
                    st.markdown(f"**Kategori:** {ticket['category']}")
                    st.markdown(f"**Deskripsi:**")
                    st.write(ticket['description'])
                
                with col2:
                    st.markdown(f"**Prioritas:** {ticket['priority']}")
                    st.markdown(f"**Status:** {ticket['status']}")
                    st.markdown(f"**Dibuat:** {ticket['created_at']}")
                    st.markdown(f"**Diupdate:** {ticket['updated_at']}")
                
                st.markdown("---")
                
                # Update status
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    new_status = st.selectbox(
                        "Update Status",
                        ["Open", "In Progress", "Resolved", "Closed"],
                        index=["Open", "In Progress", "Resolved", "Closed"].index(ticket['status']),
                        key=f"status_{ticket['id']}"
                    )
                
                with col2:
                    assigned_to = st.text_input(
                        "Assign ke",
                        value=ticket.get('assigned_to', '') or '',
                        key=f"assign_{ticket['id']}"
                    )
                
                with col3:
                    if st.button("💾 Simpan Update", key=f"save_{ticket['id']}"):
                        for t in st.session_state.tickets:
                            if t['id'] == ticket['id']:
                                t['status'] = new_status
                                t['assigned_to'] = assigned_to if assigned_to else None
                                t['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_tickets(st.session_state.tickets)
                        st.success("✅ Tiket berhasil diupdate!")
                        st.rerun()
                
                # Comments section
                st.markdown("### 💬 Komentar")
                
                if ticket.get('comments'):
                    for comment in ticket['comments']:
                        st.markdown(f"""
                        <div style='background-color: #e9ecef; padding: 10px; border-radius: 5px; margin: 5px 0;'>
                            <strong>{comment['author']}</strong> - <small>{comment['timestamp']}</small>
                            <p>{comment['text']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                new_comment = st.text_area("Tambah komentar", key=f"comment_{ticket['id']}")
                comment_author = st.text_input("Nama Anda", key=f"author_{ticket['id']}")
                
                if st.button("➕ Tambah Komentar", key=f"add_comment_{ticket['id']}"):
                    if new_comment and comment_author:
                        for t in st.session_state.tickets:
                            if t['id'] == ticket['id']:
                                if 'comments' not in t:
                                    t['comments'] = []
                                t['comments'].append({
                                    'author': comment_author,
                                    'text': new_comment,
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                t['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        save_tickets(st.session_state.tickets)
                        st.success("✅ Komentar ditambahkan!")
                        st.rerun()
    else:
        st.info("📭 Belum ada tiket yang dibuat. Silakan buat tiket baru!")

# CARI TIKET
elif st.session_state.view_mode == "Cari Tiket":
    st.title("🔍 Cari Tiket")
    
    search_method = st.radio("Cari berdasarkan:", ["ID Tiket", "Email", "Kata Kunci"])
    
    if search_method == "ID Tiket":
        ticket_id = st.text_input("Masukkan ID Tiket", placeholder="TKT-001")
        
        if st.button("🔍 Cari"):
            found = False
            for ticket in st.session_state.tickets:
                if ticket['id'].upper() == ticket_id.upper():
                    found = True
                    st.success(f"✅ Tiket ditemukan!")
                    
                    with st.container():
                        st.markdown(f"### 🎫 {ticket['id']} - {ticket['subject']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Nama:** {ticket['name']}")
                            st.markdown(f"**Email:** {ticket['email']}")
                            st.markdown(f"**Kategori:** {ticket['category']}")
                        
                        with col2:
                            st.markdown(f"**Prioritas:** {ticket['priority']}")
                            st.markdown(f"**Status:** {ticket['status']}")
                            st.markdown(f"**Dibuat:** {ticket['created_at']}")
                        
                        st.markdown("**Deskripsi:**")
                        st.write(ticket['description'])
                    break
            
            if not found:
                st.error("❌ Tiket tidak ditemukan!")
    
    elif search_method == "Email":
        email = st.text_input("Masukkan Email", placeholder="email@example.com")
        
        if st.button("🔍 Cari"):
            results = [t for t in st.session_state.tickets if email.lower() in t['email'].lower()]
            
            if results:
                st.success(f"✅ Ditemukan {len(results)} tiket dengan email tersebut")
                
                for ticket in results:
                    with st.expander(f"{ticket['id']} - {ticket['subject']}"):
                        st.json(ticket)
            else:
                st.error("❌ Tidak ada tiket dengan email tersebut!")
    
    else:  # Kata Kunci
        keyword = st.text_input("Masukkan Kata Kunci", placeholder="masalah login")
        
        if st.button("🔍 Cari"):
            results = [
                t for t in st.session_state.tickets
                if keyword.lower() in t['subject'].lower() or keyword.lower() in t['description'].lower()
            ]
            
            if results:
                st.success(f"✅ Ditemukan {len(results)} tiket")
                
                for ticket in results:
                    with st.expander(f"{ticket['id']} - {ticket['subject']}"):
                        st.json(ticket)
            else:
                st.error("❌ Tidak ada tiket yang cocok!")

# ANALITIK
elif st.session_state.view_mode == "Analitik":
    st.title("📊 Analitik & Laporan")
    
    tickets = st.session_state.tickets
    
    if tickets:
        df = pd.DataFrame(tickets)
        
        # Time-based analytics
        st.subheader("📅 Analisis Berdasarkan Waktu")
        
        df['created_date'] = pd.to_datetime(df['created_at']).dt.date
        tickets_per_day = df.groupby('created_date').size()
        
        st.line_chart(tickets_per_day)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Distribusi Kategori")
            category_counts = df['category'].value_counts()
            st.bar_chart(category_counts)
        
        with col2:
            st.subheader("⚡ Distribusi Prioritas")
            priority_counts = df['priority'].value_counts()
            st.bar_chart(priority_counts)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Status Tiket")
            status_counts = df['status'].value_counts()
            st.bar_chart(status_counts)
        
        with col2:
            st.subheader("🏢 Distribusi Departemen")
            dept_counts = df['department'].value_counts()
            st.bar_chart(dept_counts)
        
        # Response time analytics
        st.markdown("---")
        st.subheader("⏱️ Analisis Waktu Respons")
        
        resolved_tickets = df[df['status'].isin(['Resolved', 'Closed'])]
        
        if not resolved_tickets.empty:
            resolved_tickets['created_dt'] = pd.to_datetime(resolved_tickets['created_at'])
            resolved_tickets['updated_dt'] = pd.to_datetime(resolved_tickets['updated_at'])
            resolved_tickets['resolution_time'] = (resolved_tickets['updated_dt'] - resolved_tickets['created_dt']).dt.total_seconds() / 3600
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                avg_time = resolved_tickets['resolution_time'].mean()
                st.metric("Rata-rata Waktu Resolusi", f"{avg_time:.1f} jam")
            
            with col2:
                min_time = resolved_tickets['resolution_time'].min()
                st.metric("Tercepat", f"{min_time:.1f} jam")
            
            with col3:
                max_time = resolved_tickets['resolution_time'].max()
                st.metric("Terlama", f"{max_time:.1f} jam")
        
        # Export data
        st.markdown("---")
        st.subheader("📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv,
                file_name="tickets_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            json_str = json.dumps(tickets, indent=2, ensure_ascii=False)
            st.download_button(
                label="📋 Download JSON",
                data=json_str,
                file_name="tickets_export.json",
                mime="application/json",
                use_container_width=True
            )
    else:
        st.info("📭 Belum ada data untuk analisis. Buat tiket terlebih dahulu!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 20px;'>
    <p>🎫 Support Ticket System v1.0 | Dibuat dengan ❤️ menggunakan Streamlit</p>
    <p>© 2026 - Sistem Management Tiket Support @SendPain11</p>
</div>
""", unsafe_allow_html=True)