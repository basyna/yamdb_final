from django.contrib import admin
from reviews.models import Category, Comment, Genre, Title, User

admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(User)
