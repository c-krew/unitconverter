from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from django.http import HttpResponse, JsonResponse
import requests

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    context = {
    }

    return render(request, 'uswins/home.html', context)

@login_required()
def scores(request):
    """
    Controller for the app home page.
    """

    context = {
    }

    return render(request, 'uswins/scores.html', context)

@login_required()
def about(request):
    """
    Controller for the app home page.
    """

    context = {
    }

    return render(request, 'uswins/about.html', context)

def get_station_data(request):
    """
    Get data from telemetric stations
    """
    get_data = request.GET
    print(request.GET)

    try:
        dates = get_data['dates']
        two = get_data['two']
        ten = get_data['ten']
        twenty = get_data['twenty']

        table_view = TableView(column_names=dates,
                               rows=[two,
                                     ten,
                                     twenty],
                               hover=True,
                               striped=False,
                               bordered=False,
                               condensed=False,
                               row_ids=['two','ten','twenty'])

        context = {
            'gizmo_object': table_view,
        }

        return render(request,'uswins/gizmo_ajax.html', context)

    except Exception as e:
        #print str(e)
        return JsonResponse({'error': 'No historic data found for calculating flow duration curve.'})