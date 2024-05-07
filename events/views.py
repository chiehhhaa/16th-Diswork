from django.shortcuts import render


def events(req):
    return render(req, "events/calendar.html")


# Create your views here.
