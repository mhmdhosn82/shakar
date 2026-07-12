from app.models.product import Brand, Category, IMEIItem, Product, ProductVariant
from app.utils.helpers import CRUDService

category_service = CRUDService(Category, search_fields=("name", "code"))
brand_service = CRUDService(Brand, search_fields=("name", "code", "country_of_origin"))
product_service = CRUDService(Product, search_fields=("name", "sku", "barcode"))
product_variant_service = CRUDService(ProductVariant, search_fields=("color", "storage_capacity", "ram", "sku_suffix"))
imei_item_service = CRUDService(IMEIItem, search_fields=("imei",))
