from django.utils.translation import gettext_lazy
from django.contrib.auth.models import BaseUserManager

# Custom user manager for managing both superuser and normal user accounts detail storing.
class CustomUserManager(BaseUserManager):
    # for making django migrate this custom user manager not its default one. 
    use_in_migrations = True

    # creating new normal user and normal user are not active until they were verified.
    def create_user(self , phone_number , email , username ,password=None, **other_fields):
        if not phone_number :
            raise ValueError(gettext_lazy('You must provide phone number'))
        
        if email :
            email = self.normalize_email(email)
        else:
            email = None
        user = self.model(phone_number=phone_number,
            email=email,
            username=username,
            **other_fields
            )
        user.set_password(password)
        user.save()
        
        return user 
    
    # creating new super user and super user will always be active
    def create_superuser(self , phone_number , email , username , password , **other_fields):
        other_fields.setdefault('is_staff' , True)
        other_fields.setdefault('is_superuser' , True)
        other_fields.setdefault('is_active' , True)
        
        if other_fields.get('is_staff') is not True :
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True :
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(phone_number , email , username , password , **other_fields)