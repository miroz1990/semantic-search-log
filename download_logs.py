import os
import requests
from tqdm import tqdm
import tarfile

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Add multiple datasets here
DATASETS = {
    "HDFS": "https://zenodo.org/record/3227177/files/HDFS_1.tar.gz",
    "Apache": "https://zenodo.org/record/3227177/files/Apache.tar.gz",
    "Linux": "https://zenodo.org/record/3227177/files/Linux.tar.gz"
}

def download_and_extract(name, url):
    file_path = os.path.join(DATA_DIR, f"{name}.tar.gz")

    # Skip if already downloaded
    if os.path.exists(file_path):
        print(f"{name} already downloaded.")
    else:
        print(f"\nDownloading {name} dataset...")

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(file_path, 'wb') as f:
            for data in tqdm(response.iter_content(1024), total=total_size//1024):
                f.write(data)

        print(f"{name} download complete.")

    # Extract
    print(f"Extracting {name} logs...")

    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(DATA_DIR)

    print(f"{name} extraction complete.")


# Loop through datasets
for name, url in DATASETS.items():
    download_and_extract(name, url)

print("\nAll datasets ready ✅")