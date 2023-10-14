from rest_framework.viewsets import mixins, GenericViewSet


class FavoriteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    pass
