from django.contrib.auth import authenticate
from django.contrib.sites import requests
from rest_framework import viewsets, generics, parsers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView

from .models import Product, Shop, User, Comment, Review, Payments, InfoSP
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

    @action(methods=['get'], url_path='current-user', url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(self.get_serializer(request.user).data, status=status.HTTP_200_OK)

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

    @action(methods=['get'], detail=True)
    def infosps(self, request, pk):
        infosps = self.get_object().infosp_set.filter(active=True).all()

        return Response(serializers.InfoSPSerializer(infosps, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

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


class ShopViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Shop.objects.filter(active=True).all()
    serializer_class = serializers.ShopSerializer
    pagination_class = paginators.ProductPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(name__icontains=q)

        return queries

    @action(methods=['get'], detail=True)
    def infosps(self, request, pk):
        infosps = self.get_object().infosp_set.filter(active=True).all()

        return Response(serializers.InfoSPSerializer(infosps, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class InfoShopProductViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = InfoSP.objects.filter(active=True).all()
    serializer_class = serializers.InfoSPSerializer
    pagination_class = paginators.ProductPaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(id__icontains=q)

        return queries


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializers_class = serializers.CommentSerializer
    permission_classes = [perms.IsOwner]


class PaymentsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Payments.objects.all()
    serializers_class = serializers.PaymentsSerializer
    permission_classes = [perms.IsOwner]


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        authenticate_url = 'http://192.168.1.91:3000/o/token/'
        username = request.data.get('username')
        password = request.data.get('password')
        role = int(request.data.get('role'))
        user = authenticate(username=username, password=password)
        # import pdb
        # pdb.set_trace()
        if user and user.role == role:
            data = {
                'username': username,
                'password': password,
                'client_id': request.data.get('client_id'),
                'client_secret': request.data.get('client_secret'),
                'grant_type': request.data.get('grant_type')
            }
            # pdb.set_trace()

            response = requests.post(authenticate_url, data=data)

            if response.status_code == 200:
                access_token = response.json().get('access_token')
                refresh_token = response.json().get('refresh_token')
                return Response(response.json(), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

