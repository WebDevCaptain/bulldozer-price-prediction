
import os
import zipfile
from pathlib import Path

import requests


def download_and_extract_zip(
    source: str, destination: str, remove_source: bool = True
) -> Path:
    """Downloads a zipped dataset from source and extracts it to destination.

    Args:
        source (str): A link to a zipped file containing data.
        destination (str): A target directory to unzip data to.
        remove_source (bool): Whether to remove the source after downloading and extracting.

    Returns:
        pathlib.Path to downloaded data.
    """
    # Setup path to data folder
    data_path = Path("data/")
    dataset_path = data_path / destination

    # If the dataset folder doesn't exist, download it and prepare it...
    if dataset_path.is_dir():
        print(f"[INFO] {dataset_path} directory exists, skipping download.")
    else:
        print(f"[INFO] Did not find {dataset_path} directory, creating one...")
        dataset_path.mkdir(parents=True, exist_ok=True)

        target_file = Path(source).name
        target_file_path = dataset_path / target_file

        with open(target_file_path, "wb") as f:
            response = requests.get(source)
            print(f"[INFO] Downloading {target_file} from {source}...")
            f.write(response.content)

        with zipfile.ZipFile(target_file_path, "r") as zip_ref:
            print(f"[INFO] Unzipping {target_file} data...")
            zip_ref.extractall(dataset_path)

        # Remove .zip file
        if remove_source:
            os.remove(target_file_path)

    return dataset_path
