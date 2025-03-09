import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product, MaintenanceStock

class Command(BaseCommand):
    help = 'Import data from Excel file to database'

    def handle(self, *args, **kwargs):
        # Ler o arquivo Excel
        excel_file = 'caminho/para/seu_arquivo.xlsx'

        # Importar marcas
        brands_df = pd.read_excel(excel_file, sheet_name='Brand')
        for index, row in brands_df.iterrows():
            Brand.objects.create(
                name=row['nome'],
                is_active=row['ativo'],
                description=row['descrição'],
                created_at=row['criado em'],
                updated_at=row['atualizado em']
            )

        # Importar categorias
        categories_df = pd.read_excel(excel_file, sheet_name='Category')
        for index, row in categories_df.iterrows():
            Category.objects.create(
                name=row['nome'],
                is_active=row['ativo'],
                description=row['descrição'],
                created_at=row['criado em'],
                updated_at=row['atualizado em']
            )

        # Importar produtos
        products_df = pd.read_excel(excel_file, sheet_name='Product')
        for index, row in products_df.iterrows():
            brand = Brand.objects.get(name=row['marca'])
            category = Category.objects.get(name=row['categoria'])
            Product.objects.create(
                title=row['título'],
                brand=brand,
                category=category,
                price=row['preço'],
                is_active=row['ativo'],
                description=row['descrição'],
                created_at=row['criado em'],
                updated_at=row['atualizado em']
            )

        # Importar estoque de manutenção
        stock_df = pd.read_excel(excel_file, sheet_name='MaintenanceStock')
        for index, row in stock_df.iterrows():
            product = Product.objects.get(title=row['produto'])
            MaintenanceStock.objects.create(
                product=product,
                quantity=row['quantidade'],
                location=row['localização'],
                minimum_stock=row['estoque mínimo'],
                last_updated=row['última atualização']
            )

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))