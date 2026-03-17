from config.paths import POLICIES_DATA_PATH, POLICIES_DIR
from striprtf.striprtf import rtf_to_text
from common.logger import logger
from PyPDF2 import PdfReader
from tqdm import tqdm
import pandas as pd
import win32com.client
import datetime
import django
import json
import re
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.environments.dev')
django.setup()


def transform_and_load_policies():
    """
    Fetches all the existing documents from the .csv file and stores them into the SQLITE database after
    cleaning and transforming the data.
    """
    #! Needs django initalized to work
    #! Only works on Windows since it uses win32com

    from apps.docs.models import Policy

    df = pd.read_csv(POLICIES_DATA_PATH)
    logger.info(f"Storing {df.shape[0]} policies into the database.")

    word = win32com.client.Dispatch("Word.Application")
    all_topics = set()

    for _, row in df.iterrows():
        data = {}
        code = str(row['Código']).strip()
        if Policy.objects.filter(code=code).exists():
            logger.warning(f"Policy {code} already exists in the database.")
            continue

        logger.debug(f"Processing policy {code}.")

        data["code"] = code
        data["title"] = str(row['Texto depositado']).upper().strip()
        data["type"] = data["code"][:3]

        fecha_deposito = str(row['Fecha Depósito']).strip()
        if fecha_deposito.startswith('Res.'):
            fecha_deposito = fecha_deposito.split('del')[1].strip()

        # Fecha deposito is in format dd/mm/yyyy
        data["deposit_date"] = datetime.date(
            year=int(fecha_deposito.split('/')[2]),
            month=int(fecha_deposito.split('/')[1]),
            day=int(fecha_deposito.split('/')[0])
        )

        linked_policies = str(row['Pólizas/Cláusulas']).strip()
        linked_policies = re.split(r'\n|\s', linked_policies)
        if linked_policies[0] == 'nan':
            linked_policies = []
        data["linked_policies"] = linked_policies

        data["insurance_company"] = str(
            row['Nombre entidad que deposita']).strip()
        data["prohibition_resolution"] = str(row['Res. Prohibición']).strip()
        data["authorization_resolution"] = str(row['Res. Autoriza']).strip()

        is_prohibited = False
        if data["prohibition_resolution"] != "-" and data["prohibition_resolution"] != "nan" and data["prohibition_resolution"] != "":
            is_prohibited = True
        data["is_prohibited"] = is_prohibited

        topics = str(row['Temas']).strip().split('-')
        topics = [topic.strip() for topic in topics if topic != '']
        all_topics.update(topics)
        data["topics"] = json.dumps(topics)

        file = None
        if os.path.exists(os.path.join(POLICIES_DIR, f"{code}.pdf")):
            file = os.path.join(POLICIES_DIR, f"{code}.pdf")
        elif os.path.exists(os.path.join(POLICIES_DIR, f"{code}.doc")):
            file = os.path.join(POLICIES_DIR, f"{code}.doc")
        elif os.path.exists(os.path.join(POLICIES_DIR, f"{code}.rtf")):
            file = os.path.join(POLICIES_DIR, f"{code}.rtf")

        if not file:
            logger.error(f"File {code} not found.")
        else:
            with open(file, 'rb') as f:
                if file.endswith('.pdf'):
                    reader = PdfReader(f)
                    content = ''.join(page.extract_text()
                                      for page in reader.pages)
                    page_count = len(reader.pages)
                elif file.endswith('.doc'):
                    try:
                        wb = word.Documents.Open(file, False, False, True)
                        doc = word.ActiveDocument
                        content = doc.Range().Text
                        page_count = doc.ComputeStatistics(2)
                        wb.Close(SaveChanges=False)
                    except Exception as e:
                        logger.error(f"An error occurred: {e}")
                        continue
                elif file.endswith('.rtf'):
                    content = rtf_to_text(f.read())
                    page_count = None

                data["content"] = content
                data["page_count"] = page_count
                data["word_count"] = len(content.split())
                data["char_count"] = len(content)

        logger.info(f"Storing policy {code} into the database.")
        policy = Policy.objects.create(**data)
        policy.save()

    logger.info("Policies stored successfully.")
    word.Quit()

    logger.info("Updating policy topics.")
    updated = 0
    policies = Policy.objects.all()

    for policy in policies:
        topics = json.loads(policy.topics)
        topics = [topic.lower() for topic in topics]
        policy.topics = json.dumps(topics)
        policy.save()
        updated += 1
        logger.info(f"Policy {updated}/{len(policies)} updated.")

    logger.info(
        f"Topics updated successfully. {len(all_topics)} topics found.")
    logger.info(f"Topics: {all_topics}")

    logger.info("Fixing last policy details.")
    for policy in tqdm(policies):
        policy.title = policy.title.upper()
        policy.save()

    logger.info("Last policy fixes applied successfully.")


def load_to_chroma():
    from apps.docs.models import Policy
    from apps.ai.core.chroma import ChromaManager

    chroma_manager = ChromaManager()
    chroma_manager.reset_all_collections()
    policies = Policy.objects.all()

    for policy in tqdm(policies, desc="Creating embeddings for policy titles..."):
        embedding_str = f"{policy.title}"
        metadata = {
            "title": policy.title,
            "type": policy.type,
            "deposit_date": policy.deposit_date.strftime("%Y-%m-%d"),
            "linked_policies": json.dumps(policy.linked_policies),
            "insurance_company": policy.insurance_company,
            "prohibition_resolution": policy.prohibition_resolution,
            "authorization_resolution": policy.authorization_resolution,
            "is_prohibited": policy.is_prohibited,
            "topics": policy.topics,
            "char_count": policy.char_count,
            "word_count": policy.word_count,
            "page_count": policy.page_count,
        }

        chroma_manager.add_entry(
            collection_name="documents",
            pol_id=policy.code,
            str_embedding=embedding_str,
            metadata=metadata
        )

    logger.info("All policies inserted into the collection.")
