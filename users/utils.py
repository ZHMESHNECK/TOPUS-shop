from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, renderers
from users.models import Profile


class PesnolaData(APIView):
    """ Зберігає персональну інформацію користувача

    Returns:
        Response: data=dict
    """

    authentication_classes = [SessionAuthentication]
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user_id=request.user.id)
        try:
            profile.first_name = request.data.get('first_name')
            profile.last_name = request.data.get('last_name')
            profile.surname = request.data.get('surname')
            profile.phone_number = request.data.get('phone_number')
            profile.save()
            return Response(data={'ans': 'Данні успішно збережено'}, status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={'ans': 'Сталася помилка'}, status=status.HTTP_400_BAD_REQUEST)
