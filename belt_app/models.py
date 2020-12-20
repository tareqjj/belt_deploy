from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 8:
            errors["pw_length"] = "Password should be at least 8 characters"

        if postData['password'] != postData['confirm_pw']:
            errors['pw_match'] = "Passwords must match"

        if User.objects.all().filter(email=postData['email']):
            errors['not_unique'] = 'email address already registered'
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if len(postData['password']) < 8:
            errors["pw_length"] = "Password should be at least 8 characters"
        return errors

    def edit_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First Name should be at least 1 characters"

        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last Name should be at least 1 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        if User.objects.all().filter(email=postData['email']):
            errors['not_unique'] = 'email address already registered'
        return errors

class QouteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors["author"] = "Author should be at least 1 character"

        if len(postData['quote']) < 10:
            errors["quote"] = "Quote should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # liked_books = a list of books a given user likes
    # books_uploaded = a list of books uploaded by a given user


class Qoute(models.Model):
    author = models.CharField(max_length=255)
    quote = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="quotes_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QouteManager()

def reg_user(user_info):
    password = user_info['password']
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=user_info['first_name'], last_name=user_info['last_name'], email=user_info['email'], password=hashed)
    user_info = {
        'user_id': new_user.id,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email,
    }
    return user_info

def login_user(user_info):
    user = User.objects.filter(email=user_info['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(user_info['password'].encode(), logged_user.password.encode()):
            user_info = {
                'user_id': logged_user.id,
                'first_name': logged_user.first_name,
                'last_name': logged_user.last_name,
                'email': logged_user.email,
            }
            return user_info
    return False

def add_quote_DB(quote_info, user_id):
    new_quote = Qoute.objects.create(author=quote_info['author'], quote=quote_info['quote'], uploaded_by=User.objects.get(id=user_id))


def add_like_toQuote(quote_id, user_id):
    Qoute.objects.get(id=quote_id).users_who_like.add(User.objects.get(id=user_id))


def view_quotes(user_id):
    liked_quotes = User.objects.get(id=user_id).liked_quotes.all()
    likedQuotes_list=[]
    for quote in liked_quotes:
        likedQuotes_list.append(quote.id)

    context = {
        'user_info':  User.objects.get(id=user_id),
        'all_quotes': Qoute.objects.all(),
        'liked_quotes': likedQuotes_list
    }
    return context

def view_userPage(user_id):
    context = {
        'all_quotes_uploaded': User.objects.get(id=user_id).quotes_uploaded.all(),
        'user_info':  User.objects.get(id=user_id)
    }
    return context

def remove_quote(message_id):
    Qoute.objects.get(id=message_id).delete()

def edit_user(user_id, user_info):
    User.objects.filter(id=user_id).update(first_name=user_info['first_name'], last_name=user_info['last_name'], email=user_info['email'])

def display_edited_user(user_id):
    context = {
        'user_info': User.objects.get(id=user_id)
    }
    return context
