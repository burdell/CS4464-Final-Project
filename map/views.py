from map.models import RegistrationForm, MapPost, Friendship
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import re

import datetime

def youtube(string):
	if not string:
		return ''
		
	string = string.split('&')[0]
	vid_id = re.search(r'watch\?v=(.+)', string)

	if vid_id:
		return vid_id.group(1)

	return ''

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

	elif option == 'one_hour':                
                hour_ago = timedelta(hours=1)
                now = datetime.datetime.now()
                then = now-hour_ago
                map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'two_hours':                
            hour_ago = timedelta(hours=2)
            now = datetime.datetime.now()
            then = now-hour_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'three_hours':                
            hour_ago = timedelta(hours=3)
            now = datetime.datetime.now()
            then = now-hour_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)

	elif option == 'one_week':                
            week_ago = timedelta(weeks=1)
            now = datetime.datetime.now()
            then = now-week_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'two_weeks':                
            week_ago = timedelta(weeks=2)
            now = datetime.datetime.now()
            then = now-week_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'three_weeks':                
            week_ago = timedelta(weeks=3)
            now = datetime.datetime.now()
            then = now-week_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)

	elif option == 'one_month':                
            month_ago = timedelta(weeks=4)
            now = datetime.datetime.now()
            then = now-month_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'two_months':                
            month_ago = timedelta(weeks=8)
            now = datetime.datetime.now()
            then = now-month_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)
	elif option == 'three_months':                
            month_ago = timedelta(weeks=12)
            now = datetime.datetime.now()
            then = now-month_ago
            map_posts = MapPost.objects.filter(posted_on__gt=then)

    #filter by post type         
	elif option == 'accident':
		map_posts = MapPost.objects.filter(post_type="accident")
	elif option == 'advertisement':
		map_posts = MapPost.objects.filter(post_type="advertisement")
	elif option == 'crime':
		map_posts = MapPost.objects.filter(post_type="crime")
	elif option == 'fire':
		map_posts = MapPost.objects.filter(post_type="fire")
	elif option == 'landmark':
		map_posts = MapPost.objects.filter(post_type="landmark")
	elif option == 'news_story':
		map_posts = MapPost.objects.filter(post_type="news_story")
	elif option == 'party':
		map_posts = MapPost.objects.filter(post_type="party")
	elif option == 'status_update':
		map_posts = MapPost.objects.filter(post_type="status_update")
	elif option == 'steer_clear':
		map_posts = MapPost.objects.filter(post_type="steer_clear")              
	else:
		map_posts = MapPost.objects.all()
		
	
	js_array = "var map_posts = ["
	vid="None"
	for map_post in map_posts:
                if map_post.post_video:
                        vid = "http://www.youtube.com/embed/" + map_post.post_video
		js_array += "[" + str(map_post.lat) + ", " + str(map_post.lon) + ", \"" + map_post.text + "\", \"" + map_post.user.username + "\", \"" + map_post.post_type + "\", \"" + vid + "\"], " 
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
			post_video = request.POST['post_video']
                        video_ID = youtube(post_video)
            

			MapPost.objects.create(lat=lat, lon=lon, text=text, user=request.user, post_type=post_type, posted_on=timestamp, post_video=video_ID)
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

		

