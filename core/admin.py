from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, OrderItem
from .models import PCBDesign

# PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

# ORDER ADMIN
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]


@admin.register(PCBDesign)
class PCBAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50"/>'.format(obj.image.url))
        return "-"