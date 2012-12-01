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
    label = models.CharField(max_length=64)
    text = models.TextField()

class Event(models.Model):
    MESSAGE_TYPES =  (
        (1, 'sms'),
        (2, 'voice'),
        (3, 'email'),
        )
    RESULT_TYPES = (
        (0, 'success'),
        (1, 'busy'),
        (2, 'nopickup'),
        (3, 'failed'),
        (4, 'pending'),
        )
    student = models.ForeignKey('Student')
    message = models.ForeignKey('Message')
    date_of_message = models.DateTimeField()
    type_of_message = models.IntegerField(choices=MESSAGE_TYPES) 
    result_of_message = models.IntegerField(choices = RESULT_TYPES)
