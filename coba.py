
import requests
import concurrent.futures
import time
import os

def clear_screen():
    # untuk Windows
    if os.name == 'nt':
        os.system('cls')
    # untuk Linux/Mac
    else:
        os.system('clear')

# panggil fungsi clear
clear_screen()
# Konfigurasi
RPC_URL = "TOKEN SUI MU"
INPUT_FILE = "wallet.txt"
OUTPUT_FILE = "wallet_ada_balance.txt"

HEADERS = {"Content-Type": "application/json"}
DELAY_PER_CHECK = 3  # Detik
MAX_RETRIES = 2      # Ulang hingga 2 kali jika gagal

def get_sui_balance(address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "suix_getBalance",
        "params": [address]
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(RPC_URL, json=payload, headers=HEADERS, timeout=15)

            if response.status_code == 200:
                result = response.json()
                if "result" in result:
                    balance_mist = int(result["result"]["totalBalance"])
                    return address, balance_mist
                else:
                    error = result.get("error", {}).get("message", "Unknown error")
                    print(f"[ERROR] RPC error untuk {address} (coba {attempt}): {error}")
            else:
                print(f"[ERROR] HTTP {response.status_code} untuk {address} (coba {attempt})")

        except Exception as e:
            print(f"[ERROR] Eksepsi pada {address} (coba {attempt}): {str(e)}")

        if attempt < MAX_RETRIES:
            print(f"[RETRY] Mencoba ulang {address}...")
            time.sleep(2)

    return address, 0  # Asumsi saldo 0 jika gagal semua percobaan

def read_wallets(filename):
    try:
        with open(filename, "r") as f:
            wallets = [line.strip() for line in f if line.strip()]
        return wallets
    except FileNotFoundError:
        print(f"[ERROR] File {filename} tidak ditemukan.")
        return []

def check_with_delay(address):
    time.sleep(DELAY_PER_CHECK)  # Delay sebelum cek
    return get_sui_balance(address)

def main():
    wallets = read_wallets(INPUT_FILE)

    if not wallets:
        print("Tidak ada alamat wallet ditemukan atau file kosong.")
        return

    found_wallets = []

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(check_with_delay, wallets)

            for result in results:
                if result:
                    address, balance = result
                    print(f"DEBUG: {address} balance = {balance}")
                    if balance > 0:
                        print(f"[ADA SALDO] {address} -> {balance / 1_000_000_000:.9f} SUI")
                        found_wallets.append(address)
                    else:
                        print(f"[TIDAK ADA SALDO] {address}")

    except KeyboardInterrupt:
        print("\n[INFO] Program dihentikan oleh user. Menyimpan hasil sementara...")

    # Simpan hasil apapun kondisinya
    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write("\n".join(found_wallets))
        print(f"[INFO] File berhasil disimpan: {OUTPUT_FILE}")
        if found_wallets:
            print(f"Total wallet dengan saldo: {len(found_wallets)}")
        else:
            print("Semua wallet tidak memiliki saldo.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file: {str(e)}")

    # Tulis file output hanya 1x
    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write("\n".join(found_wallets))  # Jika kosong, file tetap dibuat tapi kosong
        print(f"\n[INFO] File berhasil disimpan: {OUTPUT_FILE}")
        if found_wallets:
            print(f"Total wallet dengan saldo: {len(found_wallets)}")
        else:
            print("Semua wallet tidak memiliki saldo.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file: {str(e)}")


    # Selalu buat file output, meskipun kosong
    try:
        with open(OUTPUT_FILE, "w") as f:
            if found_wallets:
                f.write("\n".join(found_wallets))
        print(f"\n[INFO] File berhasil disimpan: {OUTPUT_FILE}")
        if found_wallets:
            print(f"Total wallet dengan saldo: {len(found_wallets)}")
        else:
            print("Semua wallet tidak memiliki saldo.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file: {str(e)}")
    # Selalu simpan hasil ke file
    try:
        with open(OUTPUT_FILE, "w") as f:
            if found_wallets:
                f.write("\n".join(found_wallets))
        print(f"\nHasil pengecekan selesai.")
        print(f"File output tersimpan di: {OUTPUT_FILE}")
        if found_wallets:
            print(f"Total wallet dengan saldo: {len(found_wallets)}")
        else:
            print("Tidak ada wallet yang memiliki saldo.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan file {OUTPUT_FILE}: {str(e)}")

if __name__ == "__main__":
    main()