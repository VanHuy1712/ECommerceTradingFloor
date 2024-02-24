from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Product, Shop, InfoSP
from django.urls import path
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Product
        fields = '__all__'


class ShopForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Shop
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    search_fields = ['name', 'price']
    list_filter = ['id', 'name', 'price']
    form = ProductForm


class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    form = ShopForm


class EcommerceAppAdminSite(admin.AdminSite):
    site_header = 'Sàn giao dịch thương mại điện tử'


admin_site = EcommerceAppAdminSite(name='myapp')


admin.site.register(Product, ProductAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(InfoSP)
