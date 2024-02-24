from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from .models import Product, Shop, User, Comment, Review, Payments
from . import serializers, paginators, dao, perms


class UserViewSet(viewsets.ViewSet,
                  generics.ListAPIView,
                  generics.UpdateAPIView,
                  generics.DestroyAPIView,
                  generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    #    def get_permissions(self):
    #       if self.action.__eq__('current_user'):
    #           return [permissions.IsAuthenticated()]
    #
    #     return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        request.user
        return Response(serializers.UserSerializer(request.user).data)

    @action(methods=['post'], detail=False, url_path='products')
    def add_product(self, request):
        product = Product.objects.create(user=request.user, data=request.data)

        return Response(serializers.ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request):
        users = dao.sreach_product(params=request.GET)

        return Response(serializers.UserInteractionSerializer(users, many=True).data,
                        status=status.HTTP_200_OK)


# Create your views here.
class ProductViewSet(viewsets.ViewSet,
                     generics.ListAPIView,
                     generics.UpdateAPIView,
                     generics.DestroyAPIView,
                     generics.RetrieveAPIView):
    queryset = Product.objects.filter(active=True).all()
    serializer_class = serializers.ProductSerializer
    pagination_class = paginators.ProductPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    @action(methods=['post'], detail=True, url_path='comments')
    def add_comments(self, request, pk):
        c = Comment.objects.create(user=request.user, post=self.get_object(), content=request.data.get('content'))

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='ratings')
    def rating_product(self, request, pk):
        type = int(request.data.get('type'))
        rating, created = Review.objects.get_or_create(user=request.user, post=self.get_object(),
                                                       type=type)
        if not created:
            rating.active = not rating.active
            rating.save()
        post_detail_serializer = self.get_serializer(self.get_object(), context={'request': request})
        return Response(post_detail_serializer.data, status=status.HTTP_204_NO_CONTENT)


class ShopViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Shop.objects.filter(active=True).all()
    serializer_class = serializers.ShopSerializer
    pagination_class = paginators.ProductPaginator


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializers_class = serializers.CommentSerializer
    permission_classes = [perms.IsOwner]


class PaymentsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Payments.objects.all()
    serializers_class = serializers.PaymentsSerializer
    permission_classes = [perms.IsOwner]

