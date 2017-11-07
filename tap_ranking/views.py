# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from . import search_data
from django import forms
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

def index(request):
    if request.session.get('username'):
        return HttpResponseRedirect('/Installs')
    else:
        return HttpResponseRedirect('/login')

def login(request):
    message = ''
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            is_ok = search_data.check_name_pass(username, password)
            if is_ok:
                request.session['username'] = username
                return HttpResponseRedirect('/index')
            else:
                message = "账号密码不正确!"
    else:
        uf = UserForm()
    return render_to_response('login.html', {'message': message})

def Logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login')

def Installs(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context = {}
        context['tap_lists'] = search_data.get_Installs(times, search)
        context['type'] = 'Installs'
        context['time'] = times
        context['search'] = search
        context['username'] = request.session['username']
        return render(request, 'taptap_rank.html', context)
    else:
        return HttpResponseRedirect('/login')

def reserved(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context  = {}
        context['tap_lists'] = search_data.get_reserved(times, search)
        context['type'] = 'reserved'
        context['time'] = times
        context['search'] = search
        context['username'] = request.session['username']
        return render(request, 'taptap_rank.html', context)
    else:
        return HttpResponseRedirect('/login')

def attention(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context  = {}
        context['tap_lists'] = search_data.get_attention(times, search)
        context['type'] = 'attention'
        context['time'] = times
        context['search'] = search
        context['username'] = request.session['username']
        return render(request, 'taptap_rank.html', context)
    else:
        return HttpResponseRedirect('/login')

def tap_ad(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        context  = {}
        context['tap_ad_lists'] = search_data.tap_ad_lists(times)
        context['tap_top_game'] = search_data.tap_top_game(times)
        context['time'] = times
        context['username'] = request.session['username']
        return render(request, 'taptap_ads.html', context)
    else:
        return HttpResponseRedirect('/login')

def add_everyday(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context  = {}
        context['tap_add_everyday'] = search_data.tap_add_everyday(times, search)
        context['time'] = times
        context['search'] = search
        context['username'] = request.session['username']
        return render(request, 'add_everyday.html', context)
    else:
        return HttpResponseRedirect('/login')


def gonggao(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context = {}
        context['tap_lists'] = search_data.get_gongao_list(times, search)
        context['type'] = 'Installs'
        context['time'] = times
        context['search'] = search
        context['username'] = request.session['username']
        return render(request, 'gonggao.html', context)
    else:
        return HttpResponseRedirect('/login')


