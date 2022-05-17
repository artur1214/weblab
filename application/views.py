import requests
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings

from .models import Medicine, TypeChoices, User
from .serializers import MedicineSerializer, VkTokenObtainPairSerializer, \
    RefreshTokenSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated


class MedicineView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()


class AboutMeView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: WSGIRequest, format=None):
        if not request.user.is_authenticated:
            return Response(status=401)
        email = request.user.email
        username = request.user.username
        return Response({
            'id': request.user.id,
            'username': username,
            'email': email,
        })


class MedicineTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: WSGIRequest, format=None):
        #return Response([dict(zip(i[::2], i[1::2])) for i in TypeChoices.choices])
        return Response(TypeChoices.choices)


class VkTokenObtainPairView(TokenObtainPairView):
    serializer_class = VkTokenObtainPairSerializer


def get_vk_token(request):
    try:
        code = request.GET['code']
        token = requests.get(f'https://oauth.vk.com/access_token?client_id={settings.VK_APP_ID}&'
                     f'client_secret={settings.VK_KEY}&redirect_uri={settings.FRONTEND_VK_URL}&'
                             f'code={code}')
        res = token.json()
        print(res)
        user = None
        if (access_token := res.get('access_token')) and (user_id := res.get('user_id')):
            try:
                #ser.objects.get()
                user = User.vk_users().get(vk_id=str(user_id))
            except User.DoesNotExist:
                user_data = requests.get(f'https://api.vk.com/method/users.get?'
                             f'user_ids={user_id}&access_token={access_token}&v=5.131').json()['response'][0]
                print(user_data)
                user = User.objects.create_user(
                    username=f'vk_user_id{user_id}',
                    first_name=user_data.get('first_name'),
                    last_name=user_data.get('last_name'),
                    vk_id=str(user_id)
                )
            token = VkTokenObtainPairSerializer.get_token(user)
            data = {}
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            print(data)
            return JsonResponse(data, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'переданы неверные данные для входа'}, status=401)
    return HttpResponse()


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer