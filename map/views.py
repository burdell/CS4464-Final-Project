from map.models import RegistrationForm, MapPost
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse


def register(request):
	form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			#Create a new user, if the email hasn't already been used.
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			password = form.cleaned_data['password1']
			

			user = User.objects.create_user(username, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()

			return render_to_response('registration/registration_complete.html', {'user': user})

	return render_to_response('registration/register.html',
					   {'form': form, 'title_info': 'Register. Synergize. Repeat.'},
					   context_instance=RequestContext(request))

def map_page(request):
	map_posts = MapPost.objects.all()
	js_array = "var map_posts = ["
	for map_post in map_posts:
		js_array += "[" + str(map_post.lat) + ", " + str(map_post.lon) + ", \"" + map_post.text + "\"], " 
	js_array += "]"
	js_array = js_array.replace("], ]", "]]")

	return render_to_response('map.html', {'user': request.user, 'map_posts': js_array},
					   context_instance=RequestContext(request))

def map_post(request):
	success = "FIAL"
	if request.is_ajax():
		if request.method == 'POST':
			lat = request.POST['lat']
			lon = request.POST['lon']
			text = request.POST['text']

			MapPost.objects.create(lat=lat, lon=lon, text=text)
			success = "SUCCESS"
					
	return HttpResponse(success)