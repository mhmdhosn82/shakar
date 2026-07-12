from app.models.warehouse import Stock, StockMovement, Warehouse
from app.utils.helpers import CRUDService

warehouse_service = CRUDService(Warehouse, search_fields=("name", "code", "address"))
stock_service = CRUDService(Stock)
stock_movement_service = CRUDService(StockMovement, search_fields=("reference_type", "notes"))
