from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    data={'twenty': [('2018-03-21', 0.0), ('2018-03-22', 0.0), ('2018-03-23', 0.0), ('2018-03-24', 0.0), ('2018-03-25', 0.0), ('2018-03-26', 0.0), ('2018-03-27', 0.0), ('2018-03-28', 0.0), ('2018-03-29', 0.0), ('2018-03-30', 0.0), ('2018-03-31', 0.0), ('2018-04-01', 0.0), ('2018-04-02', 0.0), ('2018-04-03', 0.0), ('2018-04-04', 0.0), ('2018-04-05', 0.0)], 'two': [('2018-03-21', 0.0), ('2018-03-22', 0.0), ('2018-03-23', 9.803921568627452), ('2018-03-24', 17.647058823529413), ('2018-03-25', 3.9215686274509802), ('2018-03-26', 3.9215686274509802), ('2018-03-27', 0.0), ('2018-03-28', 0.0), ('2018-03-29', 0.0), ('2018-03-30', 0.0), ('2018-03-31', 0.0), ('2018-04-01', 0.0), ('2018-04-02', 0.0), ('2018-04-03', 0.0), ('2018-04-04', 0.0), ('2018-04-05', 0.0)], 'ten': [('2018-03-21', 0.0), ('2018-03-22', 0.0), ('2018-03-23', 0.0), ('2018-03-24', 0.0), ('2018-03-25', 1.9607843137254901), ('2018-03-26', 0.0), ('2018-03-27', 0.0), ('2018-03-28', 0.0), ('2018-03-29', 0.0), ('2018-03-30', 0.0), ('2018-03-31', 0.0), ('2018-04-01', 0.0), ('2018-04-02', 0.0), ('2018-04-03', 0.0), ('2018-04-04', 0.0), ('2018-04-05', 0.0)]}



    table_view = TableView(column_names=(),
                           rows=[],
                           hover=True,
                           striped=True,
                           bordered=True,
                           condensed=False,
                           classes='perctable',)

    context = {'table_view':table_view
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