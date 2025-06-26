from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    'Check if the user is in the Admins group'
    return user.groups.filter(name='Admins').exists()

def is_guest_or_admin(user):
    'Check if the user is in Guests or Admins group'
    return user.groups.filter(name__in=['Guests', 'Admins']).exists()

# Decorators for views
admin_required = user_passes_test(is_admin)
guest_or_admin_required = user_passes_test(is_guest_or_admin)