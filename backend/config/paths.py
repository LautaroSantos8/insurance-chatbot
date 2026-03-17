import os
from pathlib import Path

# Root directoties
BASE_DIR = Path(__file__).resolve().parent.parent
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
STORAGE_DIR = os.path.join(BASE_DIR, 'storage')

# Subdirectories
CHROMA_SQLITE_DB_DIR = os.path.join(STORAGE_DIR, 'chroma')
DATASETS_DIR = os.path.join(STORAGE_DIR, 'datasets')
POLICIES_DIR = os.path.join(DATASETS_DIR, 'policies')

# File paths
DJANGO_SQLITE_DB_PATH = os.path.join(STORAGE_DIR, 'django_db.sqlite3')
CHROMA_SQLITE_PATH = os.path.join(CHROMA_SQLITE_DB_DIR, 'chroma.sqlite3')
LOG_FILE_PATH = os.path.join(TMP_DIR, 'api.log')
POLICIES_DATA_PATH = os.path.join(DATASETS_DIR, 'cleaned_dataset.csv') 
DOWNLOAD_LINKS_PATH = os.path.join(DATASETS_DIR, 'download_links.json')