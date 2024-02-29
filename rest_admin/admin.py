from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Table)
admin.site.register(MenuTable)
admin.site.register(Categories)
admin.site.register(Expenses)
admin.site.register(PerMonthExpenses)

