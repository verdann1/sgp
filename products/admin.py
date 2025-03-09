import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Brand, Category, Product, MaintenanceStock


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="brands.csv"'
        writer = csv.writer(response)
        writer.writerow(['nome', 'ativo', 'descrição', 'criado em', 'atualizado em'])
        for brand in queryset:
            writer.writerow([brand.name, brand.is_active, brand.description,
                             brand.created_at, brand.updated_at])
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'
        writer = csv.writer(response)
        writer.writerow(['nome', 'ativo', 'descrição', 'criado em', 'atualizado em'])
        for category in queryset:
            writer.writerow([category.name, category.is_active, category.description,
                             category.created_at, category.updated_at])
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'price', 'is_active', 'maintenance_stock_info', 'created_at', 'updated_at')
    search_fields = ('title', 'brand__name', 'category__name')
    list_filter = ('is_active', 'brand', 'category')

    def maintenance_stock_info(self, obj):
        if hasattr(obj, 'maintenance_stock'):
            return f"{obj.maintenance_stock.quantity} em estoque (Mín: {obj.maintenance_stock.minimum_stock})"
        return "Sem estoque"
    maintenance_stock_info.short_description = 'Estoque de Manutenção'

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['título', 'marca', 'categoria', 'preço', 'ativo', 'descrição', 'estoque', 'criado em', 'atualizado em'])
        for product in queryset:
            stock_info = "Sem estoque"
            if hasattr(product, 'maintenance_stock'):
                stock_info = f"{product.maintenance_stock.quantity} (Mín: {product.maintenance_stock.minimum_stock})"
            writer.writerow([
                product.title,
                product.brand.name,
                product.category.name,
                product.price,
                product.is_active,
                product.description,
                stock_info,
                product.created_at,
                product.updated_at
            ])
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]


@admin.register(MaintenanceStock)
class MaintenanceStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'location', 'minimum_stock', 'last_updated')
    search_fields = ('product__title', 'location')
    list_filter = ('product__brand', 'product__category')

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="maintenance_stock.csv"'
        writer = csv.writer(response)
        writer.writerow(['produto', 'quantidade', 'localização', 'estoque mínimo', 'última atualização'])
        for stock in queryset:
            writer.writerow([
                stock.product.title,
                stock.quantity,
                stock.location,
                stock.minimum_stock,
                stock.last_updated
            ])
        return response

    export_to_csv.short_description = 'Exportar para CSV'
    actions = [export_to_csv]