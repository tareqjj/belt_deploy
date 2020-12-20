from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

# Create your views here.
def display_login_reg(request):
    return render(request, 'login_reg_page.html')

def add_user(request):
    errors = models.User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = models.reg_user(request.POST)
        request.session['logged_user_info'] = logged_user
        return redirect('/display_quotes')

def login(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = models.login_user(request.POST)
        if logged_user:
            request.session['logged_user_info'] = logged_user
            return redirect('/display_quotes')
        return redirect("/")

def logout(request):
    del request.session['logged_user_info']
    return redirect('/')

def add_Quote(request):
    errors = models.Qoute.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/display_quotes')
    else:
        models.add_quote_DB(request.POST, request.session['logged_user_info']['user_id'])
        return redirect('/display_quotes')

def add_toLikes(request, quote_id):
    models.add_like_toQuote(quote_id, request.session['logged_user_info']['user_id'])
    return redirect('/display_quotes')


def display_quoteInfo(request, quote_id):
    context = models.view_quoteInfo(quote_id, request.session['logged_user_info']['user_id'])
    return render(request, 'book_info.html', context)

def display_quotes(request):
    if 'logged_user_info' in request.session:
        context = models.view_quotes(request.session['logged_user_info']['user_id'])
        return render(request, 'display_and_add_books.html', context)
    else:
        return redirect("/")

def display_userPage(request, user_id):
    context = models.view_userPage(user_id)
    return render(request, 'user_page.html', context)

def delete_quote(request, user_id, quote_id):
    if user_id == request.session['logged_user_info']['user_id']:
        models.remove_quote(quote_id)
    return redirect('/display_quotes')

def edit_account(request, user_id):
    errors = models.User.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/display_edit/' + str(user_id))
    else:
        models.edit_user(user_id, request.POST)
        return redirect('/display_quotes')

def display_edit(request, user_id):
    context = models.display_edited_user(user_id)
    return render(request, 'edit_account.html', context)

