from django.contrib import admin

from extra.models import SI_EmptyPay, SI_Pay, SI_Contract, SI_Invoice

# Register your models here.
admin.site.register([SI_EmptyPay, SI_Pay, SI_Contract, SI_Invoice])
