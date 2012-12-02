# Create your views here.
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from teachercomapp.models import Student, Message, Event
import datetime
import csv
import StringIO

@cache_page(1)
def index(request):
    return render_to_response('index.html')

def send(request):
    if request.method == 'GET':
        data = {
            'students': Student.objects.order_by('first_name'),
            'messages': Message.objects.order_by('label')
        }

        data.update(csrf(request))
        return render_to_response('send.html', data)
    else:
        message = Message.objects.get(pk=request.POST['message'])
        for student_id in request.POST.getlist('students'):
            student = Student.objects.get(pk=student_id)
            if student.sms_notification_ind:
                send_message(student, message, 1)
            if student.call_notification_ind:
                send_message(student, message, 2)
            if student.email_notification_ind:
                send_message(student, message, 3)
        return render_to_response('sent.html')

def handle_csv(request):
    if request.method == 'GET':
        data = {}
        data.update(csrf(request))
        return render_to_response('csv.html', data)
    else:
        f = request.FILES['csv']
        contents = f.read()

        fp = StringIO.StringIO(contents)
        reader = csv.reader(fp)
        for row in reader:
            student = Student(
                student_id = row[0].strip(),
                first_name = row[1].strip(),
                last_name = row[2].strip(),
                phone_number = row[3].strip(),
                email = row[4].strip(),
                sms_notification_ind = (row[5].strip() == 'True'),
                call_notification_ind = (row[6].strip() == 'True'),
                email_notification_ind = (row[7].strip() == 'True')
            )
            student.save()
        return render_to_response('csv-saved.html')

        


def send_message(student, message, message_type):
    print 'sending message for %s' % (student.first_name)
    event = Event(student=student, message=message,
        date_of_message=datetime.datetime.now(),
        type_of_message=message_type,
        result_of_message=4)
    event.save()

def phone_call_config(request, event_id):
    twilio_call_id = request.POST.CallSid

    event = Event(pk=event_id)

    t = template.Template(event.message.text)
    c = template.Context({'student': event.student})
    call_text = t.render(c)

    # TODO if student not found ?
    # TODO if student.objects.call_notification_ind if false?

    r = twiml.Response()
    r.say(call_text)

    return HttpResponse(str(r))


def phone_call_completed_handler(request, event_id):
    twilio_call_id = request.POST.CallSid
    call_status = request.POST.CallStatus
    answered_by = request.POST.AnsweredBy

    event = Event(pk=event_id)
    student = event.Student

    if request.POST.Status == 'completed':
        result = 0
    elif request.POST.Status == 'busy':
        result = 1
    elif request.POST.Status == 'no-answer':
        result = 2
    elif request.POST.Status == 'failed':
        result = 3
    else:
        result = -1

    if result != -1:
        event.result_of_message = result
        event.Save()

    return render_to_response("success")
