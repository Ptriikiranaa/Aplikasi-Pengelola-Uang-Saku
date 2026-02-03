import json
import os
from datetime import datetime

# ANSI Color Codes
class Warna:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    END = '\033[0m'

# File untuk menyimpan data
FILE_SALDO = 'saldo.json'

# Fungsi utility
def divider(char="─", length=60):
    """Buat divider line."""
    return f"{Warna.YELLOW}{char * length}{Warna.END}"

def pause():
    """Pause dan tunggu user tekan Enter."""
    input(f"\n{Warna.DIM}[ Tekan Enter untuk lanjut... ]{Warna.END}")

def print_header(teks):
    """Menampilkan header dengan styling."""
    print(f"\n{divider('═', 60)}")
    print(f"{Warna.BOLD}{Warna.YELLOW}{teks.center(60)}{Warna.END}")
    print(f"{divider('═', 60)}\n")

# Inisialisasi struktur data
def init_data():
    """Inisialisasi struktur data jika belum ada."""
    if not os.path.exists(FILE_SALDO):
        data = {
            'saldo': 0,
            'riwayat': []
        }
        simpan_saldo(data)

def muat_saldo():
    """Membaca file saldo.json. Jika tidak ada, kembalikan 0."""
    try:
        if os.path.exists(FILE_SALDO):
            with open(FILE_SALDO, 'r') as file:
                data = json.load(file)
                return data
        else:
            return {'saldo': 0, 'riwayat': []}
    except (json.JSONDecodeError, ValueError):
        print("⚠️ File JSON korup! Menggunakan data default.")
        return {'saldo': 0, 'riwayat': []}

def simpan_saldo(data):
    """Menyimpan data saldo ke file 'saldo.json' secara terformat."""
    try:
        with open(FILE_SALDO, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"❌ Error saat menyimpan file: {e}")

def tambah_pemasukan():
    """Meminta input pemasukan, menambah saldo, dan menampilkan pesan berhasil."""
    print_header("💵 TAMBAH PEMASUKAN")
    try:
        jumlah = float(input(f"{Warna.YELLOW}  Masukkan jumlah (Rp): {Warna.END}"))
        if jumlah <= 0:
            print(f"\n{Warna.RED}  ❌ Jumlah harus lebih dari 0!{Warna.END}\n")
            pause()
            return
        
        deskripsi = input(f"{Warna.YELLOW}  Deskripsi (cth: Gaji, Bonus): {Warna.END}").strip()
        if not deskripsi:
            deskripsi = "Pemasukan"
        
        # Muat data saat ini
        data = muat_saldo()
        data['saldo'] += jumlah
        
        # Catat ke riwayat
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['riwayat'].append({
            'tanggal': waktu,
            'tipe': 'Pemasukan',
            'jumlah': jumlah,
            'deskripsi': deskripsi
        })
        
        # Simpan data
        simpan_saldo(data)
        print(f"\n{Warna.GREEN}{divider('═', 60)}{Warna.END}")
        print(f"{Warna.GREEN}{Warna.BOLD}  ✅ PEMASUKAN BERHASIL DITAMBAHKAN!{Warna.END}")
        print(f"{Warna.GREEN}{divider('═', 60)}{Warna.END}")
        print(f"\n  {Warna.BOLD}Deskripsi :{Warna.END} {deskripsi}")
        print(f"  {Warna.BOLD}Jumlah    :{Warna.END} Rp {jumlah:>17,.0f}")
        print(f"  {Warna.BOLD}{Warna.BLUE}Saldo Baru:{Warna.END} Rp {data['saldo']:>17,.0f}\n")
        pause()
    except ValueError:
        print(f"\n{Warna.RED}  ❌ Input tidak valid! Masukkan angka.{Warna.END}\n")
        pause()

def tambah_pengeluaran():
    """Meminta input pengeluaran, mengurangi saldo, tampilkan peringatan jika tidak cukup."""
    print_header("💸 TAMBAH PENGELUARAN")
    try:
        jumlah = float(input(f"{Warna.YELLOW}  Masukkan jumlah (Rp): {Warna.END}"))
        if jumlah <= 0:
            print(f"\n{Warna.RED}  ❌ Jumlah harus lebih dari 0!{Warna.END}\n")
            pause()
            return
        
        deskripsi = input(f"{Warna.YELLOW}  Deskripsi (cth: Makan, Beli buku): {Warna.END}").strip()
        if not deskripsi:
            deskripsi = "Pengeluaran"
        
        # Muat data saat ini
        data = muat_saldo()
        
        # Cek apakah saldo cukup
        if data['saldo'] < jumlah:
            kurang = jumlah - data['saldo']
            print(f"\n{Warna.RED}{divider('═', 60)}{Warna.END}")
            print(f"{Warna.RED}{Warna.BOLD}  ⚠️  SALDO TIDAK CUKUP!{Warna.END}")
            print(f"{Warna.RED}{divider('═', 60)}{Warna.END}")
            print(f"\n  {Warna.BOLD}Saldo Anda    :{Warna.END} Rp {data['saldo']:>17,.0f}")
            print(f"  {Warna.BOLD}Pengeluaran   :{Warna.END} Rp {jumlah:>17,.0f}")
            print(f"  {Warna.RED}{Warna.BOLD}Kurang        :{Warna.END} Rp {kurang:>17,.0f}\n")
            pause()
            return
        
        # Kurangi saldo
        data['saldo'] -= jumlah
        
        # Catat ke riwayat
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['riwayat'].append({
            'tanggal': waktu,
            'tipe': 'Pengeluaran',
            'jumlah': jumlah,
            'deskripsi': deskripsi
        })
        
        # Simpan data
        simpan_saldo(data)
        print(f"\n{Warna.GREEN}{divider('═', 60)}{Warna.END}")
        print(f"{Warna.GREEN}{Warna.BOLD}  ✅ PENGELUARAN BERHASIL DICATAT!{Warna.END}")
        print(f"{Warna.GREEN}{divider('═', 60)}{Warna.END}")
        print(f"\n  {Warna.BOLD}Deskripsi :{Warna.END} {deskripsi}")
        print(f"  {Warna.BOLD}Jumlah    :{Warna.END} Rp {jumlah:>17,.0f}")
        print(f"  {Warna.BOLD}{Warna.BLUE}Saldo Baru:{Warna.END} Rp {data['saldo']:>17,.0f}\n")
        pause()
    except ValueError:
        print(f"\n{Warna.RED}  ❌ Input tidak valid! Masukkan angka.{Warna.END}\n")
        pause()

def lihat_saldo():
    """Menampilkan saldo saat ini dengan rapi."""
    print_header("💰 SALDO ANDA")
    data = muat_saldo()
    
    # Styling saldo dengan warna
    if data['saldo'] > 0:
        warna = Warna.GREEN
        status = "✅ SALDO POSITIF"
    elif data['saldo'] == 0:
        warna = Warna.YELLOW
        status = "⚠️ SALDO NOLOL"
    else:
        warna = Warna.RED
        status = "❌ SALDO NEGATIF"
    
    print(f"{warna}{divider('═', 60)}{Warna.END}")
    print(f"{Warna.BOLD}{warna}{status.center(60)}{Warna.END}")
    print(f"{warna}{divider('═', 60)}{Warna.END}\n")
    
    # Display saldo dengan ukuran besar
    print(f"\n  {Warna.BOLD}{warna}Rp {data['saldo']:>20,.0f}{Warna.END}\n")
    
    print(f"{warna}{divider('═', 60)}{Warna.END}\n")
    pause()

def lihat_laporan():
    """Menampilkan rekap pemasukan dan pengeluaran."""
    print_header("📊 LAPORAN KEUANGAN LENGKAP")
    data = muat_saldo()
    
    if not data['riwayat']:
        print(f"{Warna.YELLOW}  📭 Belum ada riwayat transaksi.{Warna.END}\n")
        pause()
        return
    
    total_pemasukan = 0
    total_pengeluaran = 0
    
    # Header tabel dengan border rapi
    print(f"{Warna.YELLOW}╔════════╦════════════════════╦═════════════════════╦══════════════════╗{Warna.END}")
    print(f"{Warna.YELLOW}║{Warna.BOLD}{Warna.YELLOW}  No  {Warna.END}{Warna.YELLOW}║{Warna.BOLD}{Warna.YELLOW}    Tanggal    {Warna.END}{Warna.YELLOW}║{Warna.BOLD}{Warna.YELLOW}   Deskripsi       {Warna.END}{Warna.YELLOW}║{Warna.BOLD}{Warna.YELLOW}  Jumlah (Rp) {Warna.END}{Warna.YELLOW}║{Warna.END}")
    print(f"{Warna.YELLOW}╠════════╬════════════════════╬═════════════════════╬══════════════════╣{Warna.END}")
    
    for i, transaksi in enumerate(data['riwayat'], 1):
        tipe = transaksi['tipe']
        jumlah = transaksi['jumlah']
        tanggal = transaksi['tanggal'][:10]  # Format YYYY-MM-DD
        deskripsi = transaksi.get('deskripsi', tipe)
        
        if tipe == 'Pemasukan':
            total_pemasukan += jumlah
            symbol = f"{Warna.GREEN}+{Warna.END}"
            warna_jumlah = Warna.GREEN
        else:
            total_pengeluaran += jumlah
            symbol = f"{Warna.RED}−{Warna.END}"
            warna_jumlah = Warna.RED
        
        jumlah_str = f"{symbol} {warna_jumlah}Rp {jumlah:>10,.0f}{Warna.END}"
        deskripsi_trunc = (deskripsi[:18] + '..') if len(deskripsi) > 20 else deskripsi
        print(f"{Warna.YELLOW}║{Warna.END}  {i:>2}  {Warna.YELLOW}║{Warna.END} {tanggal} {Warna.YELLOW}║{Warna.END} {deskripsi_trunc:<19} {Warna.YELLOW}║{Warna.END}  {jumlah_str}  {Warna.YELLOW}║{Warna.END}")
    
    print(f"{Warna.YELLOW}╠════════╬════════════════════╬═════════════════════╬══════════════════╣{Warna.END}")
    
    # Ringkasan
    selisih = total_pemasukan - total_pengeluaran
    
    print(f"{Warna.YELLOW}║{Warna.END}        {Warna.YELLOW}║{Warna.END}  {Warna.GREEN}{Warna.BOLD}✓ TOTAL PEMASUKAN{Warna.END}    {Warna.YELLOW}║{Warna.END} {Warna.GREEN}Rp {total_pemasukan:>11,.0f}{Warna.END}     {Warna.YELLOW}║{Warna.END}")
    print(f"{Warna.YELLOW}║{Warna.END}        {Warna.YELLOW}║{Warna.END}  {Warna.RED}{Warna.BOLD}✗ TOTAL PENGELUARAN{Warna.END}  {Warna.YELLOW}║{Warna.END} {Warna.RED}Rp {total_pengeluaran:>11,.0f}{Warna.END}     {Warna.YELLOW}║{Warna.END}")
    
    if selisih >= 0:
        warna_selisih = Warna.GREEN
        symbol_selisih = "="
    else:
        warna_selisih = Warna.RED
        symbol_selisih = "−"
    
    print(f"{Warna.YELLOW}║{Warna.END}        {Warna.YELLOW}║{Warna.END}  {warna_selisih}{Warna.BOLD}{symbol_selisih} SELISIH{Warna.END}           {Warna.YELLOW}║{Warna.END} {warna_selisih}Rp {selisih:>11,.0f}{Warna.END}     {Warna.YELLOW}║{Warna.END}")
    print(f"{Warna.YELLOW}║{Warna.END}        {Warna.YELLOW}║{Warna.END}  {Warna.BLUE}{Warna.BOLD}💰 SALDO AKHIR{Warna.END}        {Warna.YELLOW}║{Warna.END} {Warna.BLUE}Rp {data['saldo']:>11,.0f}{Warna.END}     {Warna.YELLOW}║{Warna.END}")
    
    print(f"{Warna.YELLOW}╚════════╩════════════════════╩═════════════════════╩══════════════════╝{Warna.END}\n")
    pause()

def menu():
    """Menampilkan menu utama."""
    print(f"\n{Warna.BOLD}{Warna.HEADER}")
    print("  ╔════════════════════════════════════════════════╗")
    print("  ║                                                ║")
    print("  ║    🏦  APLIKASI PENGELOLA UANG SAKU 🏦    ║")
    print("  ║                                                ║")
    print("  ║          💰 Money Management App 💰            ║")
    print("  ║                                                ║")
    print("  ╚════════════════════════════════════════════════╝")
    print(f"{Warna.END}")
    
    print(f"\n  {Warna.YELLOW}┌──────────────────────────────────────────────┐{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}                                              {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}  {Warna.BOLD}{Warna.GREEN}1{Warna.END}  💵 Tambah Pemasukan                  {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}  {Warna.BOLD}{Warna.RED}2{Warna.END}  💸 Tambah Pengeluaran                {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}  {Warna.BOLD}{Warna.YELLOW}3{Warna.END}  💰 Lihat Saldo                      {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}  {Warna.BOLD}{Warna.YELLOW}4{Warna.END}  📊 Lihat Laporan                    {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}  {Warna.BOLD}{Warna.RED}5{Warna.END}  🚪 Keluar                           {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}│{Warna.END}                                              {Warna.YELLOW}│{Warna.END}")
    print(f"  {Warna.YELLOW}└──────────────────────────────────────────────┘{Warna.END}")

# Inisialisasi data
init_data()

# Loop utama
while True:
    menu()
    pilihan = input(f"\n  {Warna.YELLOW}{Warna.BOLD}→ Pilih menu (1-5): {Warna.END}")

    if pilihan == "1":
        tambah_pemasukan()
    elif pilihan == "2":
        tambah_pengeluaran()
    elif pilihan == "3":
        lihat_saldo()
    elif pilihan == "4":
        lihat_laporan()
    elif pilihan == "5":
        print(f"\n{Warna.BOLD}{Warna.HEADER}")
        print("  ╔════════════════════════════════════════════════╗")
        print("  ║                                                ║")
        print("  ║  ✨ Terima kasih telah menggunakan aplikasi! ║")
        print("  ║                                                ║")
        print("  ║           Sampai jumpa lagi! 👋               ║")
        print("  ║                                                ║")
        print("  ╚════════════════════════════════════════════════╝")
        print(f"{Warna.END}\n")
        break
    else:
        print(f"\n  {Warna.RED}{Warna.BOLD}❌ Pilihan tidak valid! Silakan pilih 1-5.{Warna.END}\n")