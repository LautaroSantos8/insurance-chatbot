from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from common.logger import logger
from utils.validators import validate_post_request_with_fields, validate_request_has_files, user_with_id_exists
from apps.docs.models import Policy
from apps.users.models import User
import json


""" # @validate_post_request_with_fields(["user_id"])
@validate_request_has_files()
@csrf_exempt
def upload_document(request: HttpRequest):
    # body_params = json.loads(request.body.decode('utf-8'))
    user_id = 123  # body_params["user_id"]
    if user_with_id_exists(user_id):
        return JsonResponse({'status': 400, 'message': 'Invalid user.'})

    files = request.FILES.items()
    error_messages = []

    logger.debug(f"Received files: {files}")

    for file_entry in files:
        file = file_entry[1]  # is a InMemoryUploadedFile object
        extension = file.name.split('.')[-1]

        if extension == 'txt':
            content = file.read()

        elif extension == 'pdf':
            from PyPDF2 import PdfReader
            reader = PdfReader(file)
            content = ''.join(page.extract_text() for page in reader.pages)

        elif extension == 'docx':
            from docx import Document as DocxDocument
            docx = DocxDocument(file)
            content = '\n'.join(
                [paragraph.text for paragraph in docx.paragraphs])
        else:
            error_messages.append(f"Invalid file format: {extension}")
            continue

        document = Policy.objects.create(
            owner=user_id,
            title=file.name,
            content=content
        )
        document.save()

        logger.debnug(f"Document {document.id} created successfully")

    if error_messages:
        return JsonResponse({'status': 400, 'message': error_messages})

    return JsonResponse({'status': 200, 'message': 'File uploaded successfully'}) """

# Policy data:
"""
class Policy(models.Model):
    code = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=50, choices=POLICY_TYPES)
    title = models.CharField(max_length=100)
    insurance_company = models.CharField(max_length=100)
    deposit_date = models.DateField()
    linked_policies = models.JSONField(default=list, null=True, blank=True)
    prohibition_resolution = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    authorization_resolution = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    topics = models.TextField()
    is_prohibited = models.BooleanField(default=False)

    content = models.TextField(default="", null=True, blank=True)
    page_count = models.IntegerField(default=0, null=True, blank=True)
    word_count = models.IntegerField(default=0, null=True, blank=True)
    char_count = models.IntegerField(default=0, null=True, blank=True)

"""


@csrf_exempt
@validate_post_request_with_fields(["code"])
def get_policy(request: HttpRequest):
    body_params = json.loads(request.body.decode('utf-8'))
    code = body_params["code"]

    try:
        policy = Policy.objects.get(code=code)
        policy_info = {
            'code': policy.code,
            'title': policy.title,
            'content': policy.content,
            'topics': policy.topics,
            'insurance_company': policy.insurance_company,
            'linked_policies': policy.linked_policies,
            'is_prohibited': policy.is_prohibited,
            'prohibition_resolution': policy.prohibition_resolution,
            'authorization_resolution': policy.authorization_resolution
        }
        return JsonResponse({'status': 200, 'message': policy_info})
    except Policy.DoesNotExist:
        return JsonResponse({'status': 400, 'message': 'Document not found'})
    except Exception as e:
        logger.error(f"Error while fetching document: {e}")
        return JsonResponse({'status': 500, 'message': 'Internal server error'})
