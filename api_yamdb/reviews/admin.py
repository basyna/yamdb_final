from django.contrib import admin

from reviews.models import Comment, Genre, Category, Title, User

admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(User)
