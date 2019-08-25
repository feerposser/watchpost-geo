from rest_framework.viewsets import ModelViewSet


from .serializers import SerializerCidade


class ViewSetCidade(ModelViewSet):
    serializer_class = SerializerCidade

    def get_queryset(self):
        pass
