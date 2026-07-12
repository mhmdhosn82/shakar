from fastapi import APIRouter

from app.api.v1.endpoints import accounting, audit, auth, backup, brands, branches, categories, customers, inventory, products, purchases, sales, suppliers, users, warehouses

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(branches.router, prefix="/branches", tags=["Branches"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(brands.router, prefix="/brands", tags=["Brands"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(warehouses.router, prefix="/warehouses", tags=["Warehouses"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(customers.router, prefix="/customers", tags=["Customers"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(sales.router, prefix="/sales", tags=["Sales"])
api_router.include_router(purchases.router, prefix="/purchases", tags=["Purchases"])
api_router.include_router(accounting.router, prefix="/accounting", tags=["Accounting"])
api_router.include_router(backup.router, prefix="/backup", tags=["Backup"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
