from django.contrib import admin
from .models import Customer

# Define an admin class to customize admin interface
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'user') # Columns to display in the admin list view
    search_fields = ('first_name', 'last_name', 'email') # Fields to be searchable in the admin
    list_filter = ('user',) # Filters you can use on the side

# Register the Customer model with its admin class
admin.site.register(Customer, CustomerAdmin)