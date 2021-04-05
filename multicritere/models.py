from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model, ModelBase
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

class Profile(models.Model):
	COORDINATEUR = 'Coordinateur'
	DECIDEUR = 'Decideur'
    
	ROLE_CHOICES = (
		(COORDINATEUR, 'Coordinateur'),
        (DECIDEUR, 'Decideur'),
	)

	SEX_CHOICES = (
		('MALE', 'Homme'),
		('FEMALE', 'Femme')
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=30, blank=True)
	birthdate = models.DateField(null=True, blank=True)
	role = models.CharField(choices=ROLE_CHOICES, null=True, blank=True, max_length=20)
	gender = models.CharField(choices=SEX_CHOICES, default=1, max_length=20, blank=True, null=True)
	def __str__(self):  
		return self.user.username

	
def content_file_name(instance, filename):
	return '/'.join(['content', instance.user.user.username, filename])

class DataCordinateur(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='datasCord')
	mp = models.FileField(upload_to=content_file_name, default='default.csv')

	def __str__(self):
		return '{}'.format(self.user)

class DataDecideur(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='datasDecid')
	mp = models.FileField(upload_to=content_file_name, default='default.csv')
	weights = models.FileField(upload_to=content_file_name, default='default.csv')

	def __str__(self):
		return '{}'.format(self.user)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.create(user=instance)
		profile.save()
		print(profile)
		if profile.role == 'Coordinateur':
			data = DataCordinateur.objects.create(user = profile).save()
		else:
			data = DataDecideur.objects.create(user = profile).save()
