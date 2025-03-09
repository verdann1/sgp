import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Brand, Category, Product, MaintenanceStock

class Command(BaseCommand):
    help = 'Import data from Excel file to database'

    def handle(self, *args, **kwargs):
        # Caminho para o arquivo Excel
        excel_file = r"P:\sgp\import_data.xlsx"  # Use o caminho completo

        # Importar marcas
        try:
            brands_df = pd.read_excel(excel_file, sheet_name='Brand')
            for index, row in brands_df.iterrows():
                Brand.objects.create(
                    name=row['nome'],
                    is_active=row['ativo'],
                    description=row['descrição'],
                    created_at=row['criado em'],
                    updated_at=row['atualizado em']
                )
            self.stdout.write(self.style.SUCCESS('Marcas importadas com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao importar marcas: {e}"))

        # Importar categorias
        try:
            categories_df = pd.read_excel(excel_file, sheet_name='Category')
            for index, row in categories_df.iterrows():
                Category.objects.create(
                    name=row['nome'],
                    is_active=row['ativo'],
                    description=row['descrição'],
                    created_at=row['criado em'],
                    updated_at=row['atualizado em']
                )
            self.stdout.write(self.style.SUCCESS('Categorias importadas com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao importar categorias: {e}"))

        # Importar produtos
        try:
            products_df = pd.read_excel(excel_file, sheet_name='Product')
            for index, row in products_df.iterrows():
                try:
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
                except Brand.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Marca '{row['marca']}' não encontrada."))
                except Category.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Categoria '{row['categoria']}' não encontrada."))
            self.stdout.write(self.style.SUCCESS('Produtos importados com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao importar produtos: {e}"))

        # Importar estoque de manutenção
        try:
            stock_df = pd.read_excel(excel_file, sheet_name='MaintenanceStock')
            for index, row in stock_df.iterrows():
                try:
                    product = Product.objects.get(title=row['produto'])
                    MaintenanceStock.objects.create(
                        product=product,
                        quantity=row['quantidade'],
                        location=row['localização'],
                        minimum_stock=row['estoque mínimo'],
                        last_updated=row['última atualização']
                    )
                except Product.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Produto '{row['produto']}' não encontrado."))
            self.stdout.write(self.style.SUCCESS('Estoque de manutenção importado com sucesso!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao importar estoque de manutenção: {e}"))