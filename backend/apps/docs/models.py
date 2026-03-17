from django.db import models

POLICY_TYPES = [
    ('POL', 'Póliza General'),
    ('CAL', 'Clausula Adicional'),
    ('CAD', 'Clausula Adicional'),
    ('COP', 'Clausula Opcional'),
    ('CUG', 'Clausula de Uso General')
]


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
