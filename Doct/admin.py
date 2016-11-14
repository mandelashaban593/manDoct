from django.contrib import admin
from Doct.models import Category, Page, UserProfile, Topup, Register, Diognosis,Enterpay,\
Illness, Patientr, Conddrugs


admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)

admin.site.register(Topup)

admin.site.register(Register)
admin.site.register(Diognosis)
admin.site.register(Enterpay)
admin.site.register(Illness)
admin.site.register(Conddrugs)