from map.models import RegistrationForm, MapPost, Friendship
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import datetime

def prof_redirect(request):
	return redirect('/map_page/', permanent=True)

def register(request):
	form = RegistrationForm()
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			#Create a new user, if the email hasn't already been used.
			username = form.cleaned_data['username']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			password = form.cleaned_data['password2']
			email = username + '@gmail.com'		

			user = User.objects.create_user(username, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.save()

			return render_to_response('registration/registration_complete.html', {})

	return render_to_response('registration/register.html',
					   {'form': form, 'title_info': 'Register. Synergize. Repeat.'},
					   context_instance=RequestContext(request))
@login_required
def map_page(request, option):
	if option == 'friends':
		map_posts = []
		friend_rows = Friendship.objects.filter(user=request.user.pk)
		friend_list = []
		for friend in friend_rows:
			friend_list.append(friend.friend)

		for friend in friend_list:
			friend_posts = MapPost.objects.filter(user=User.objects.get(pk=friend))
			for post in friend_posts:
				map_posts.append(post)
	elif option == 'me':
		map_posts = MapPost.objects.filter(user=request.user)
	else:
		map_posts = MapPost.objects.all()
		
	
	js_array = "var map_posts = ["
	for map_post in map_posts:
		js_array += "[" + str(map_post.lat) + ", " + str(map_post.lon) + ", \"" + map_post.text + "\", \"" + map_post.user.username + "\", \"" + map_post.post_type + "\"], " 
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
			post_type = request.POST['post_type']
			timestamp = datetime.datetime.now()
            

			MapPost.objects.create(lat=lat, lon=lon, text=text, user=request.user, post_type=post_type, posted_on=timestamp)
			success = "SUCCESS"
					
	return HttpResponse(success)

def friend_list(request):
	friends = Friendship.objects.filter(user=request.user.pk)

	friend_list = []
	for friend in friends:
		friend_list.append(User.objects.get(pk=friend.friend))

	all_users = User.objects.all()
	others = []
	for a_user in all_users:
		if a_user not in friend_list:
			others.append(a_user)

	return render_to_response('friends.html', {'user':request.user, 'friend_list':friend_list, 'others':others}, context_instance=RequestContext(request))


def add_friend(request):
	success = "False"
	if request.is_ajax():
		if request.method == 'POST':
			user = request.user
			friend = request.POST['user_id']
			Friendship.objects.create(user=user.pk, friend=friend)
			success = "True"
	
	return HttpResponse(success)

		

