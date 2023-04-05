from django.db import models

# Create your models here.

class MyModel(models.Model):
    id = models.AutoField(db_column='post_id', primary_key=True, )
    pdf_file = models.FileField(upload_to='pdf_files/')
