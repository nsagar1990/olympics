# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpRequest
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.core import serializers
from models import *

def data(request):
	rows = Olympics.objects.all()
	medals_tally = []
	for row in rows:
		json_data = json.loads(serializers.serialize('json', [row]))
		json_data = json_data[0]
		medals_tally.append(json_data['fields'])

	chart = {'title': {'text': 'Winter Olympics Medals', 'x': -20},
			'subtitle': {'text': 'Source: wikipedia.org', 'x': -20},
			'xAxis': {'categories': [ row.country for row in rows ]},
			'yAxis': {'title': {'text': 'Medals'},
			'plotLines': [{'value': 0, 'width': 1, 'color': '#808080'}]},
			'legend': {'layout': 'vertical','align': 'right',
				'verticalAlign': 'middle', 'borderWidth': 0	},
			'series': [{'name': 'Gold',	'data': [ row.gold for row in rows ]},
			{'name': 'Silver', 'data' : [ row.silver for row in rows ]},
			{'name': 'Bronze', 'data': [ row.bronze for row in rows ]}]}
	output_data = {'chart' : chart, 'medals' : medals_tally}
	return JsonResponse(output_data)

def index(request):
	return render(request, 'index.html', context={})
