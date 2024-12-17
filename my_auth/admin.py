from django.contrib import admin
from .models import User, UserMobile, TokenRecoverPassword, CodeRecoverPassword, City

admin.site.register(User)
admin.site.register(UserMobile)
admin.site.register(TokenRecoverPassword)
admin.site.register(CodeRecoverPassword)






