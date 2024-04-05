from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def create_custom_permissions(sender,instance,created,**kwargs):
    permissions_to_assign = Permission.objects.filter(codename__in=employee_permissions + owner_permissions + customer_permissions)
    # Get ContentType model
    if created:  # If a new user is created
        if instance.is_super:  # Assign "owner" group if the user is staff
            group, _ = Group.objects.get_or_create(name='Owner')
            group.permissions.add(*permissions_to_assign.filter(codename__in=owner_permissions))
        elif instance.is_staff:  # Assign "owner" group if the user is staff
            group, _ = Group.objects.get_or_create(name='Employee')
            group.permissions.add(*permissions_to_assign.filter(codename__in=employee_permissions))
        else:  # Otherwise, assign "employee" group
            group, _ = Group.objects.get_or_create(name='Customer')
            group.permissions.add(*permissions_to_assign.filter(codename__in=customer_permissions))
        instance.groups.add(group)  # Add the group to the user
  
    # Retrieve or create employee and owner group

    # Define a list of permission codenames for each group
    employee_permissions = [
        'can_view_employee_group',
        'can_change_employee_group',
        'can_delete_employee_group',
    ]
    owner_permissions = [
        'can_view_owner_group',
        'can_change_owner_group',
        'can_delete_owner_group',
        'can_view_employee_group',
        'can_change_employee_group',
        'can_delete_employee_group',
        'can_view_customer_group',
        'can_change_customer_group',
        'can_delete_customer_group'
    ]
    customer_permissions = [
        'can_view_customer_group'
    ]

    # Get the actual permission instances
    

