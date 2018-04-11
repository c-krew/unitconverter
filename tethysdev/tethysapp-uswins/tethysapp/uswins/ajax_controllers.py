from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render
import netCDF4 as nc
from netCDF4 import *
import pandas as pd
import datetime
import ast
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import *
from django.http import HttpResponse, JsonResponse
import requests



def forecastpercent(request):


    # Check if its an ajax post request
    if request.is_ajax() and request.method == 'GET':
        reach = int(request.GET.get('comid'))

        request_params = dict(watershed_name='Dominican Republic', subbasin_name='National', reach_id=reach)
        request_headers = dict(Authorization='Token fa7fa9f7d35eddb64011913ef8a27129c9740f3c')
        res = requests.get('http://tethys-staging.byu.edu/apps/streamflow-prediction-tool/api/GetReturnPeriods/',
                           params=request_params, headers=request_headers)

        resdict = ast.literal_eval(res.content)
        resdict.pop('max', None)

        rivers = {}
        riverpercent = {}
        rivpercorder = {}

        for key in resdict:
            filename = '/Users/student/Sandbox/DR/netcdf-dr/20180322/Qout_dominican_republic_national_1.nc'
            ncf = nc.Dataset(filename)

            rivid = ncf.variables['rivid'][:]

            rp = float(resdict[key])
            rivers[key] = {}
            netnum = 1

            times = ncf.variables['time'][:]
            timeall = []
            timeuniq = []
            for i in times:
                date = datetime.datetime.fromtimestamp(i).strftime('%Y-%m-%d')
                timeall.append(date)
                if date not in timeuniq:
                    timeuniq.append(date)

            for q in timeuniq:
                rivers[key][q] = []

            length = len(timeall)
            riv_index = rivid.tolist().index(reach)
            for b in range(0, length):
                flow = ncf.variables['Qout'][riv_index][b]
                time = timeall[b]
                if flow > rp:
                    if netnum not in rivers[key][time]:
                        rivers[key][time].append(netnum)

            for c in range(2, 52):
                filename = '/Users/student/Sandbox/DR/netcdf-dr/20180322/Qout_dominican_republic_national_' + str(c) + '.nc'

                ncf = nc.Dataset(filename)

                netnum = c

                # for y in rivid:
                riv_index = rivid.tolist().index(reach)
                for b in range(0, length):
                    flow = ncf.variables['Qout'][riv_index][b]
                    time = timeall[b]
                    if flow > rp:
                        if netnum not in rivers[key][time]:
                            rivers[key][time].append(netnum)

            riverpercent[key] = {}
            for e in rivers[key]:
                riverpercent[key][e] = float(len(rivers[key][e])) / 51.0 * 100

        for keyss in riverpercent:
            data = riverpercent[keyss]
            ordered_data = sorted(data.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'))
            rivpercorder[keyss] = ordered_data

        rivdates = []
        rivperctwo = []
        rivpercten = []
        rivperctwenty = []

        for a in rivpercorder['two']:
            rivdates.append(a[0])
            rivperctwo.append(a[1])

        for s in rivpercorder['ten']:
            rivpercten.append(s[1])

        for d in rivpercorder['twenty']:
            rivperctwenty.append(d[1])

        formatteddates = [str(elem)[-4:] for elem in rivdates]
        formattedtwo = ["%.2f" % elem for elem in rivperctwo]
        formattedten = ["%.2f" % elem for elem in rivpercten]
        formattedtwenty = ["%.2f" % elem for elem in rivperctwenty]

    try:


        table_view = TableView(column_names=formatteddates,
                               rows=[formattedtwo,
                                     formattedten,
                                     formattedtwenty],
                               hover=True,
                               striped=True,
                               bordered=True,
                               condensed=True,
                               row_ids=['two','ten','twenty'])

        context = {
            'gizmo_object': table_view,
        }

        return render(request,'uswins/gizmo_ajax.html', context)

    except Exception as e:
        print str(e)
        return JsonResponse({'error': 'No historic data found for calculating flow duration curve.'})