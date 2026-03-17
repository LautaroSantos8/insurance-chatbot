import json
import os
import random
import time
import requests
import PyPDF2
from config.paths import POLICIES_DIR, DOWNLOAD_LINKS_PATH
from dotenv import dotenv_values
from common import logger

env = dotenv_values()


class PolicyExtractionPipeline:
    def __init__(self):
        """
        Initializes the PolicyExtractionPipeline with the given download directory and links JSON path.

        :param download_dir: Directory where files will be downloaded.
        :param links_json_path: Path to the JSON file containing the download links.
        """
        self.download_folder = POLICIES_DIR
        self.downloaded_files = set()
        self.links_dict = json.load(open(DOWNLOAD_LINKS_PATH, "r"))
        self.cookiesession1 = env["CMF_COOKIESESSION1"]
        self.phpsessid = env["CMF_PHPSESSID"]

    def download_files_from_json(self):
        """
        Downloads files from the links provided in the JSON file to the specified download directory.
        """
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        if os.path.exists("downloaded.json"):
            with open("downloaded.json", "r") as downloaded_file:
                self.downloaded_files = set(json.load(downloaded_file))

        consecutive_failures = 0

        for code, link in self.links_dict.items():
            try:
                sleep_time = random.uniform(5, 10)
                time.sleep(sleep_time)
                headers = {
                    'User-Agent': 'Mozilla/5.0',
                    'Cookie': f'cookiesession1={self.cookiesession1}; PHPSESSID={self.phpsessid}'
                }
                response = requests.get(link, headers=headers)
                if response.status_code == 200:
                    file_name = os.path.join(
                        self.download_folder, code + '.pdf')
                    with open(file_name, 'wb') as f:
                        f.write(response.content)
                    logger.debug(f"Downloaded file for code {code}")

                    self.downloaded_files.add(code)
                    consecutive_failures = 0
                else:
                    logger.error(
                        f"Failed to download file for code {code}: Status code {response.status_code}")
                    consecutive_failures += 1
                    if consecutive_failures >= 5:
                        logger.error(
                            "Too many consecutive failures. Cancelling process.")
                        break

            except Exception as e:
                logger.error(f"Failed to download file for code {code}: {e}")
                consecutive_failures += 1
                if consecutive_failures >= 5:
                    logger.error(
                        "Too many consecutive failures. Cancelling process.")
                    break

        with open("downloaded.json", "w") as downloaded_file:
            json.dump(list(self.downloaded_files), downloaded_file)

    def check_missing_files(self):
        """
        Checks for any missing files that were not downloaded.

        :return: Set of missing codes.
        """
        downloaded_files_json_list = json.load(open("downloaded.json", "r"))
        self.downloaded_files = set(downloaded_files_json_list)
        all_codes = set(self.links_dict.keys())
        missing_codes = all_codes - self.downloaded_files
        return missing_codes

    def convert_doc_files(self):
        """
        Converts downloaded files to .doc format if they cannot be read as PDFs.
        """
        renamed_files = []
        failed_files = []

        for file_name in os.listdir(self.download_folder):
            file_path = os.path.join(self.download_folder, file_name)
            try:
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
            except Exception as e:
                logger.debug(f"Failed to open file {file_name} as PDF: {e}")
                new_file_path = os.path.join(
                    self.download_folder, os.path.splitext(file_name)[0] + ".doc")
                try:
                    os.rename(file_path, new_file_path)
                    renamed_files.append(new_file_path)
                    logger.debug(
                        f"Renamed file {file_name} to {new_file_path}")
                except Exception as e:
                    logger.debug(f"Failed to rename file {file_name}: {e}")
                    failed_files.append(file_path)

        logger.debug(f"Renamed files: {renamed_files}")
        logger.debug(f"Failed files: {failed_files}")

    def convert_rtf_files(self):
        """
        Converts files identified as RTF to have the .rtf extension.

        :return: List of renamed files.
        """
        renamed_files = []

        for file_name in os.listdir(self.download_folder):
            file_path = os.path.join(self.download_folder, file_name)
            logger.debug(f"Checking file {file_name}")
            try:
                with open(file_path, 'r') as file:
                    start_chars = file.read(10)
                    logger.debug(f"Start chars for {file_name}: {start_chars}")

                if "\\rtf" in start_chars and not file_name.endswith(".rtf"):
                    logger.debug(f"{file_name} is an RTF file")
                    new_file_path = os.path.join(
                        self.download_folder, os.path.splitext(file_name)[0] + ".rtf")
                    os.rename(file_path, new_file_path)
                    renamed_files.append(new_file_path)
                    logger.debug(
                        f"Renamed file {file_name} to {new_file_path}")

            except Exception as e:
                logger.debug(f"Failed to open file {file_name}: {e}")

        return renamed_files
