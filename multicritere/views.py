from os import read
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile, DataDecideur
# Create your views here.
from django.contrib.auth.decorators import login_required
import pandas as pd
import csv
from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from sys import argv
import os
class AgenteHello(Agent):
    def __init__(self, aid, name):
        super(AgenteHello, self).__init__(aid=aid)
        display_message(self.aid.localname, 'Hello {}!'.format(name))

def home(request):
	agents_per_process = 4
	c = 0
	agents = list()
	for i in range(agents_per_process):
		print(i)
		print(argv[2])
		port = argv[2]
		agent_name = 'agent_{}_{}'.format(i, port)
		agente = AgenteHello(AID(name=agent_name), agent_name)
		agents.append(agente)
		c += 1000

	# start_loop(agents)
	return render(request, 'home.html', )

import pandas as pd
import json
@login_required
def dashboard(request):
	user_profile = Profile.objects.get(user = request.user)
	if user_profile.role == 'Coordinateur':
		print("cordinateur")
		decideurs = Profile.objects.filter(role = "Decideur")
		print(user_profile.datasCord.last().mp.url)
		performancematrix = pd.read_csv(user_profile.datasCord.last().mp)
		geeks_object = performancematrix
		
		for rows  in geeks_object.values:
			for row in rows:
				print(row)
		
		context = {
			'user_profile': user_profile,
			'geeks_object' : geeks_object.to_html(),
			'columns': geeks_object,
			'data': geeks_object.values,
			'decideurs' : decideurs
		}
		return render(request, 'registration/dashboard.html', context)
	else:
		print("Decideuuuuuuuuuuuuuur")
		if user_profile.datasDecid.last():
			performancematrix = pd.read_csv(user_profile.datasDecid.last().mp)
			weights = pd.read_csv(user_profile.datasDecid.last().weights)
			geeks_object = performancematrix
			geeks_weights = weights
			print(geeks_weights.columns)

			context = {
				'user_profile': user_profile,
				'columns': geeks_object,
				'data': geeks_object.values,
				'weights_column' : geeks_weights,
				'weights_data' : geeks_weights.columns
			}
		else:

			context = {
				'user_profile': user_profile,
			}
		return render(request, 'registration/dashboard.html', context)

def send_matrix_to_all_dec(request):
	user_profile = Profile.objects.get(user = request.user)
	decideurs = Profile.objects.filter(role = "Decideur")
	for decideur in decideurs:
		data_decideur = DataDecideur.objects.create(user = decideur, mp = user_profile.datasCord.last().mp)
		data_decideur.save()
	return redirect('home')
import subprocess

def classification(request):
	user_profile = Profile.objects.get(user = request.user)
	# subprocess.Popen('python ',user_profile.datasDecid.last().mp , user_profile.datasDecid.last().weights)
	output = subprocess.Popen(['media/promethe2.py', user_profile.datasDecid.last().mp.url, user_profile.datasDecid.last().weights.url])
	print(output)
	context = {'output': output}
	return render(request, 'registration/classification.html', context)

def send_matrix(request, decideur):
	user_profile = Profile.objects.get(user = request.user)
	decideur = Profile.objects.get(user = decideur)
