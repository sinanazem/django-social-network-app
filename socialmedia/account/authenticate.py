from django.contrib.auth.models import User


class EmailBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user and user.check_password(password):
                return user
            
        except user.DoesNotExist:
            return None
            


    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        
        except user.DoesNotExist:
            return None
