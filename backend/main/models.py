
from django.db import models

class Corona(models.Model):
	# patient_id=models.IntegerField()
	region=models.CharField(blank=True, max_length=100)
	num=models.IntegerField()
	# confirmed_date=models.DateField()

