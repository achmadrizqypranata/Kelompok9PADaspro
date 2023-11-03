from prettytable import PrettyTable
import json
import os
import pwinput

# Inisialisasi data produk dan keranjang belanja
products = []
shopping_cart = []

# Inisialisasi saldo E-Money
user_balance = 0

# Fungsi untuk menyimpan data produk ke dalam file JSON
def save_products_to_file():
    with open("products.json", "w") as file:
        json.dump(products, file)

# Fungsi untuk membaca data produk dari file JSON
def load_products_from_file():
    if os.path.exists("products.json"):
        with open("products.json", "r") as file:
            data = json.load(file)
            products.extend(data)

# Fungsi untuk menampilkan produk
def display_products(products_to_display=None):
    if not products_to_display:
        print("Tidak ada produk yang tersedia.")
        return

    table = PrettyTable()
    table.field_names = ["No.", "Nama Produk", "Harga"]
    for i, product in enumerate(products_to_display, start=1):
        table.add_row([i, product['name'], product['price']])
    
    print(table)

# Fungsi untuk menampilkan saldo E-Money
def display_balance():
    print(f"Saldo E-Money Anda:  Rp. {user_balance:.2f}")

# Fungsi untuk menambahkan saldo E-Money
def top_up_balance():
    global user_balance
    display_balance()
    choice = input("Apakah Anda ingin top up saldo E-Money? (ya/tidak): ")
    if choice.lower() == "ya":
        amount = int(input("Masukkan jumlah yang ingin Anda top up: Rp. "))
        if amount > 0:
            user_balance += amount
            print(f"Saldo E-Money Anda sekarang: Rp. {user_balance:.2f}")
        else:
            print("Saldo harus lebih dari 0")
    elif choice.lower() == "tidak":
        return
    else:
        print("Pilihan Anda tidak valid")

# Fungsi untuk menambahkan produk ke keranjang belanja
def add_to_cart(product):
    shopping_cart.append(product)
    print(f"{product['name']} ditambahkan ke keranjang belanja.")

# Fungsi untuk melihat isi keranjang belanja
def view_shopping_cart():
    if not shopping_cart:
        print("Keranjang belanja kosong.")
    else:
        print("Isi Keranjang Belanja:")
        table = PrettyTable()
        table.field_names = ["No.", "Nama Produk", "Harga"]
        for i, product in enumerate(shopping_cart, start=1):
            table.add_row([i, product['name'], product['price']])
        print(table)

# Fungsi untuk melakukan pembelian
def checkout():
    global user_balance
    if not shopping_cart:
        print("Keranjang belanja kosong. Belanja dulu sebelum checkout.")
        return

    receiver_name = input("Nama Penerima: ")
    delivery_address = input("Alamat Pengiriman: ")
    phone_number = input("Nomor Telepon: ")

    # Pilihan jasa pengiriman
    print("Pilih Jasa Pengiriman:")
    print("1. JNE")
    print("2. J&T")
    print("3. TIKI")
    delivery_option = input("Pilih jasa pengiriman (1/2/3): ")

    if delivery_option == "1":
        delivery_service = "JNE"
    elif delivery_option == "2":
        delivery_service = "J&T"
    elif delivery_option == "3":
        delivery_service = "TIKI"
    else:
        print("Pilihan jasa pengiriman tidak valid.")
        return

    # Membuat PrettyTable untuk invoice
    invoice_table = PrettyTable()
    invoice_table.field_names = ["Deskripsi", "Data"]
    invoice_table.add_row(["Nama Penerima", receiver_name])
    invoice_table.add_row(["Alamat Pengiriman", delivery_address])
    invoice_table.add_row(["Nomor Telepon", phone_number])
    invoice_table.add_row(["Jasa Pengiriman", delivery_service])

    total_price = sum(product['price'] for product in shopping_cart)

    # Membuat PrettyTable untuk invoice produk
    product_table = PrettyTable()
    product_table.field_names = ["Nama Produk", "Harga"]
    for product in shopping_cart:
        product_table.add_row([product['name'], product['price']])

    # Menampilkan informasi pengguna dan invoice belanja dalam satu tabel
    user_invoice_table = PrettyTable()
    user_invoice_table.field_names = ["Deskripsi", "Data"]
    user_invoice_table.add_row(["Nama Penerima", receiver_name])
    user_invoice_table.add_row(["Alamat Pengiriman", delivery_address])
    user_invoice_table.add_row(["Nomor Telepon", phone_number])
    user_invoice_table.add_row(["Jasa Pengiriman", delivery_service])
    user_invoice_table.add_row(["Invoice Belanja", product_table])
    user_invoice_table.add_row(["Total Harga", f"Rp {total_price:.2f}"])

    # Menampilkan invoice pengguna dan belanja dalam satu tabel
    print("Invoice Belanja dan Informasi Pengguna:")
    print(user_invoice_table)

    if user_balance >= total_price:
        user_balance -= total_price
        print("Checkout berhasil. Produk telah dibeli.")
        shopping_cart.clear()
    else:
        print("Saldo E-Money Anda tidak mencukupi untuk melakukan checkout.")

# Fungsi utama untuk pembeli
def buyer_main():
    global user_balance
    display_products(products)  # Memanggil fungsi ini untuk menampilkan daftar produk
    while True:
        print("\nMenu Pembeli:")
        print("1. Lihat / Top Up E-Money")
        print("2. Beli Buku")
        print("3. Lihat Keranjang")
        print("4. Checkout")
        print("5. Keluar")
        
        choice = input("Pilih operasi (1/2/3/4/5): ")
        
        if choice == "1":
            top_up_balance()
        elif choice == "2":
            # Memanggil fungsi ini untuk menampilkan daftar produk
            choice = input("Pilih nomor produk yang ingin Anda beli: ")
            if choice.isdigit() and 0 < int(choice) <= len(products):
                selected_product = products[int(choice) - 1]
                add_to_cart(selected_product)
            else:
                print("Pilihan produk tidak valid.")
        elif choice == "3":
            view_shopping_cart()
        elif choice == "4":
            checkout()
        elif choice == "5":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

# Fungsi untuk login Customer
def sign_in_Customer(data_Customer):
    username_input = input("Masukkan username: ")
    password_input = pwinput.pwinput("Masukkan password: ", mask='*')

    if username_input in data_Customer and data_Customer[username_input] == password_input:
        print("Login berhasil!")
        return True
    else:
        print("Login gagal. Coba lagi.")
        return False

def sign_up_Customer(data_Customer):
    username = input("Masukkan username baru: ")
    if username in data_Customer:
        print("Username sudah ada. Coba lagi.")
        return

    password = pwinput.pwinput("Masukkan password: ", mask='*')

    data_Customer[username] = password
    save_data_Customer(data_Customer)
    print("Akun berhasil ditambahkan!")
    return True

def load_data_Customer():
    try:
        with open("data_Customer.json", "r") as file:
            user_data = json.loads(file.read())
        return user_data
    except FileNotFoundError:
        return {}

def save_data_Customer(data_Customer):
    with open("data_Customer.json", "w") as file:
        json.dump(data_Customer, file)


# Fungsi untuk login admin
def login_admin():
    while True:
        admin = {
            "raisky": "6086",
            "luqman": "6068",
            "julia": "6069",
        }

        # Minta pengguna untuk memasukkan nama pengguna dan kata sandi
        username = input("Masukkan nama : ")
        password = pwinput.pwinput("Masukkan password: ", mask='*')
        # Cek apakah nama pengguna dan kata sandi ada di database
        if username in admin and password == admin[username]:
            # Jika ya, maka pengguna berhasil login
            print("="*100)
            print("selamat datang",username) 
            print("="*100)
            return True
        else:
            # Jika tidak, maka pengguna gagal login
            print("Nama pengguna atau kata sandi salah.")
            return False

# Fungsi untuk menampilkan produk menggunakan PrettyTable
def table_products():
    table = PrettyTable()
    table.field_names = ["Nama Produk", "Harga"]
    
    for product in products:
        table.add_row([product['name'], product['price']])
    
    print(table)

# Fungsi untuk menambahkan produk baru
def tambah_product():
    table_products()
    nama_products = input("Nama Produk: ")
    harga_products = int(input("Harga Produk: "))
    
    product = {
        "name": nama_products,
        "price": harga_products
    }
    
    products.append(product)
    save_products_to_file()

# Fungsi untuk membaca dan menampilkan semua produk
def melihat_products():
    table_products()
    if not products:
        print("Tidak ada produk yang tersedia.")
        return

# Fungsi untuk memperbarui produk berdasarkan nama
def perbarui_product():
    table_products()
    product_name = input("Nama Produk yang akan diperbarui: ")
    
    for product in products:
        if product['name'] == product_name:
            nama_baru = input("Nama Produk Baru: ")
            harga_baru = int(input("Harga Produk Baru: "))
            product['name'] = nama_baru
            product['price'] = harga_baru
            save_products_to_file()
            print("Produk diperbarui.")
            return
    
    print("Produk tidak ditemukan.")

# Fungsi untuk menghapus produk berdasarkan nama
def hapus_product():
    table_products()
    product_name = input("Nama Produk yang akan dihapus: ")
    
    for product in products:
        if product['name'] == product_name:
            products.remove(product)
            save_products_to_file()
            print("Produk dihapus.")
            return
    
    print("Produk tidak ditemukan.")

if __name__ == "__main__":
    load_products_from_file()  # Memuat produk saat memasuki program
    data_Customer = load_data_Customer()

while True:
    try:
        print("="*100)
        print("Selamat datang di Toko Buku ")
        print("="*100)
        print("1. Admin")
        print("2. Customer")
        print("3. Keluar")
        peran = input("Pilih peran Anda (Admin/Customer): ")
        print("="*100)

        if peran == "1":
            if login_admin():
                while True:
                    print("\nMenu Admin:")
                    print("1. Tambah Produk")
                    print("2. Lihat Produk")
                    print("3. Perbarui Produk")
                    print("4. Hapus Produk")
                    print("5. Keluar")
                    choice = input("Pilih operasi (1/2/3/4/5): ")

                    if choice == "1":
                        tambah_product()
                    elif choice == "2":
                        melihat_products()
                    elif choice == "3":
                        perbarui_product()
                    elif choice == "4":
                        hapus_product()
                    elif choice == "5":
                        print("Terima kasih! Sampai jumpa.")
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")

        elif peran == "2":
                while True:
                    print("\nLogin Customer:")
                    print("1. Sign In")
                    print("2. Sign Up")
                    print("3. Keluar")
                    pilihan = input("Pilih operasi (1/2/3): ")

                    if pilihan == "1":
                        if sign_in_Customer(data_Customer):
                            buyer_main()
                            break
                    elif pilihan == "2":
                        if sign_up_Customer(data_Customer):
                            buyer_main()
                            break
                    elif pilihan == "3":
                        break
                    else:
                        print("Pilihan tidak valid. Silakan coba lagi.")
        elif peran == "3":
            print("Terima kasih! Sampai jumpa.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")
    except KeyboardInterrupt:
        print("cieee")
