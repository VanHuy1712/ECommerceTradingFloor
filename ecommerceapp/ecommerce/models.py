from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


class User(AbstractUser):
    class Role(models.IntegerChoices):
        ADMIN = 1, "Admin"
        STAFF = 2, "Staff"
        USER = 3, "User"
    role = models.IntegerField(choices=Role.choices, default=Role.USER)
    avatar = CloudinaryField('avatar', null=True)


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    seller_id = models.CharField(max_length=10, unique=True, null=True)

    class Meta:
        unique_together = ('user', 'seller_id')

    def __str__(self):
        return f"{self.user}'s Profile"


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Shop(BaseModel):
    name = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255, null=True, unique=True)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class InfoSP(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        # Muc dich la khong tao table
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=True)


class Review(Interaction):
    class RatingStart(models.IntegerChoices):
        ONE = 1, "One Star"
        TWO = 2, "Two Star"
        THREE = 3, "Three Star"
        FOUR = 4, "Four Star"
        FIVE = 5, "Five Star"

    active = models.BooleanField(default=True)
    rate = models.IntegerField(choices=RatingStart, null=True)

    def __str__(self):
        return self.rate.name

    class Meta:
        unique_together = ('user', 'product')


class Payments(Interaction):
    class PayChoices(models.IntegerChoices):
        PAYPAL = 1, "Pay pal"
        STRIPE = 2, "Stripe"
        ZALO = 3, "Zalo"
        MOMO = 4, "Momo"
        PAYDIRECT = 5, "Pay when recive product"

    active = models.BooleanField(default=True)
    payments = models.IntegerField(choices=PayChoices, null=True)

