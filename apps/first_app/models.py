from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def name_invalid(self, first_name):
        if not len(first_name) < 2 and re.search(r'^[a-zA-Z]+$', first_name):
            return False
        else:
            return True
    def email_invalid(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if email_regex.match(email):
            return False
        else:
            return True
    def password_invalid(self, password):
        if len(password) < 8:
            return True
        else:
            return False
    def password_not_match(self, password, confirm_password):
        if password == confirm_password:
            return False
        else:
            return True
    def reg_validator(self, username, name, email, password, confirm_password):
        errors = []
        if not username:
            errors.append("Alias field must not be empty")
        if self.name_invalid(first_name):
            errors.append("Name must be more than two characters and only letters")
        if self.email_invalid(email):
            errors.append("Invalid email")
        if self.password_invalid(password):
            errors.append("Password must be 8 characters or more")
        if self.password_not_match(password, confirm_password):
            errors.append("Passwords must match")
        return errors
## returns an object with either {errors: list of errors}, or {user: user object}
    def add_user(self, username, name, email, password, confirm_password):
        errors = self.reg_validator(username, name, email, password, confirm_password)
        if errors:
            return {'errors': errors}
        else:
            try:
                hash_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                user = User(username=username, name=name, email=email, hash_pw=hash_pw)
                user.save()
                return {"user": user}
            except:
                return {"errors": ["Email already registered"]}
## returns an object with either {errors: list of errors}, or {user: user object}
    def login(self, email, password):
        try:
            user = User.objects.get(email=email)
            if bcrypt.hashpw(password.encode(), user.hash_pw.encode()) == user.hash_pw:
                return {"user": user}
            else:
                return {"errors": ["Invalid email or password"]}
        except:
            return {"errors": ["Invalid email or password"]}



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    hash_pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField('self', through='Friend', symmetrical=False, related_name='related_to')
    objects = UserManager()

    def __unicode__(self):
        return self.name

    def add_friend(self, person, status):
        friend, created = Friend.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status)
        return friend

    def remove_friend(self, person, status):
        Friend.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        return

    def get_following(self):
        return self.get_following(FRIEND_FOLLOWING)

    def get_friends(self, status):
        return self.friends.filter(
            to_people__status=status,
            to_people__from_person=self)

    def get_related_to(self, status):
        return self.related_to.filter(
            from_people__status=status,
            from_people__to_person=self)


FRIEND_FOLLOWING = 1
FRIEND_BLOCKED = 2
FRIEND_STATUSES = (
    (FRIEND_FOLLOWING, 'Following'),
    (FRIEND_BLOCKED, 'Blocked'),
)

class Friend(models.Model):
    from_person = models.ForeignKey(User, related_name='from_people')
    to_person = models.ForeignKey(User, related_name='to_people')
    status = models.IntegerField(choices=FRIEND_STATUSES)
