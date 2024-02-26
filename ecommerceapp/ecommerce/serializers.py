from .models import Product, User, Comment, Payments, Shop, InfoSP
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class InfoSPSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoSP
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # Băm mật khẩu
    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        # user = User(first_name=data.first_name)
        user.set_password(data['password'])
        user.save()

        return user


class UserInteractionSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar']


class CommentSerializer(serializers.ModelSerializer):
    user = UserInteractionSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    user = UserInteractionSerializer()

    class Meta:
        model = Payments
        fields = '__all__'

