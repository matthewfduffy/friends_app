from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from models import *

def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.login(email, password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session["username"] = user["user"].username
            request.session["id"] = user["user"].id
            request.session["name"] = user["user"].name
            return redirect('main:index')
    else:
        return redirect(reverse('login/index'))

def register(request):
    if request.method == "POST":
        name = request.POST['first_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.add_user(name, username, email, password, confirm_password)
        if "errors" in user:
            for error in user["errors"]:
                messages.error(request, error)
            return redirect(reverse('login:index'))
        else:
            request.session["username"] = user["user"].username
            request.session["name"] = user["user"].name
            request.session["id"] = user["user"].id
            return redirect('main:index')
    else:
        return redirect(reverse('login:index'))

def logout(request):
    request.session['id'] = None
    return redirect(reverse('login:index'))

def user(request, user_id):
    if request.session['id'] == None:
		return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=user_id)
            }
        return render(request, 'user.html', context)

def main(request):
    if request.session['id'] == None:
		return redirect('/')
    user = User.objects.get(id = request.session['id'])
    friends = user.friends.all()
    friendlist = []
    for f in friends:
        friendlist.append(f)
    notfriends = User.objects.all().exclude(name=user.name)
    for x in friendlist:
        notfriends = notfriends.exclude(name=x.name)
    context = {
        'user':request.session['id'],
        'friends': friends,
        'notfriends': notfriends,
    }
    return render(request, 'home.html', context)

def newfriend(request, user_id):
    current_user = User.objects.get(id= request.session['id'])
    newfriend = User.objects.get(id=user_id)
    current_user.add_friend(newfriend, FRIEND_FOLLOWING)
    return redirect('/main')

def byefriend(request, user_id):
    current_user = User.objects.get(id= request.session['id'])
    oldfriend = User.objects.get(id=user_id)
    current_user.remove_friend(oldfriend, FRIEND_FOLLOWING)
    return redirect('/main')
