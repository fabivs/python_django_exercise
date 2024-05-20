from django.http import HttpResponse

def get_reports(request):
    return HttpResponse(status=200)
