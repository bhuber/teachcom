from django.db import models

# Create your models here.
class Student(models.Model):
    student_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    sms_notification_ind = models.BooleanField()
    call_notification_ind = models.BooleanField()
    email_notification_ind = models.BooleanField()
    phone_number = models.CharField(max_length=30)
    email= models.CharField(max_length=30)

class Message(models.Model):
    text = models.TextField()

class Event(models.Model):
    student = models.ForeignKey('Student')
    message = models.ForeignKey('Message')
    date_of_message = models.DateTimeField()
    time_of_message = models.DateTimeField()
    type_of_message = models.IntegerField() #Create a dict for this
    result_of_message = models.IntegerField() #and this