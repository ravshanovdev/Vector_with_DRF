from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class RegistrationApiView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']

        user = User(username=username, email=email,)
        user.set_password(password)

        try:
            user.save()

            refresh = RefreshToken.for_user(user)

        except Exception as e:
            return Response({"error": str(e)})

        return Response(
            {
                'status': 'success',
                'user_id': user.id,
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }
        )



