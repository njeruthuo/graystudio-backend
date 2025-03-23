from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import Client, ClientSerializer


class ClientAPIView(APIView):

    def get(self, request, *args, **kwargs):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        client = ClientSerializer(data=request.data)
        if client.is_valid(raise_exception=True):
            client.save()
            return Response(client.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


client_api_view = ClientAPIView.as_view()
