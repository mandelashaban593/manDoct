from django.contrib import admin
from Doct.models import  Page, UserProfile, Topup, Register, Diognosis,Enterpay,\
Illness, Patientr, Conddrugs,converse,convMembers


admin.site.register(Page)
admin.site.register(UserProfile)

admin.site.register(Topup)

admin.site.register(Register)
admin.site.register(Diognosis)
admin.site.register(Enterpay)
admin.site.register(Illness)
admin.site.register(Conddrugs)
admin.site.register(converse)
admin.site.register(convMembers)