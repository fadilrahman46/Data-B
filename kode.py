import pandas as pd
import requests

def extract_data_to_dataframe(url):
    """
    Mengambil data dari URL API BPS dan mengubahnya menjadi pandas DataFrame.

    Args:
        url (str): URL API yang akan diakses.

    Returns:
        pd.DataFrame: DataFrame yang berisi data domain, atau None jika gagal.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # Periksa apakah data adalah dictionary atau list
        if isinstance(data, dict):
            # Jika data adalah dictionary, coba ambil "domain" dari kunci "data"
            domain_data = data.get("data", {}).get("domain", [])
        elif isinstance(data, list):
            # Jika data adalah list, anggap list tersebut berisi data domain
            domain_data = data
        else:
            print("Format data JSON tidak dikenal.")
            return None

        if not domain_data:
            print("Tidak ada data 'domain' yang ditemukan.")
            return None

        # Membuat DataFrame dari list of dictionaries
        df = pd.DataFrame(domain_data)

        # Mengatur ulang nama kolom sesuai format yang diminta
        df.rename(columns={
            "domain_id": "domain_id",
            "domain_name": "domain_nama",
            "domain_url": "domain_url"
        }, inplace=True)

        return df

    except requests.exceptions.RequestException as e:
        print(f"Error saat mengakses API: {e}")
        return None
    except KeyError:
        print("Format JSON tidak sesuai dengan yang diharapkan.")
        return None

# --- Bagian Utama Program ---
if __name__ == "__main__":
    # URL API yang akan diakses
    url = "https://webapi.bps.go.id/v1/api/domain/type/kab/prov/00000/key/79452e4c302f8921ad36cd2bf55f0630/"
    
    # Mengambil data dan membuatnya menjadi DataFrame
    df_result = extract_data_to_dataframe(url)

    if df_result is not None:
        print("DataFrame berhasil dibuat:")
        print(df_result.head())
    
    # Tambahkan fungsi ekspor ke Excel jika diperlukan
    def export_to_excel(dataframe, filename="data_domain_bps.xlsx"):
        if dataframe is not None:
            try:
                dataframe.to_excel(filename, index=False)
                print(f"Data berhasil diekspor ke file '{filename}'.")
            except Exception as e:
                print(f"Gagal mengekspor data ke Excel: {e}")

    # Panggil fungsi untuk mengekspor data
    export_to_excel(df_result)