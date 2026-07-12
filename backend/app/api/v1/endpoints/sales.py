from fastapi import APIRouter

from app.schemas.sales import (
    InstallmentPlanCreate,
    InstallmentPlanRead,
    InstallmentPlanUpdate,
    InstallmentScheduleCreate,
    InstallmentScheduleRead,
    InstallmentScheduleUpdate,
    PaymentCreate,
    PaymentRead,
    PaymentUpdate,
    SalesInvoiceCreate,
    SalesInvoiceItemCreate,
    SalesInvoiceItemRead,
    SalesInvoiceItemUpdate,
    SalesInvoiceRead,
    SalesInvoiceUpdate,
)
from app.services.sales import (
    installment_plan_service,
    installment_schedule_service,
    payment_service,
    sales_invoice_item_service,
    sales_invoice_service,
)
from app.utils.helpers import build_crud_router

router = APIRouter()
router.include_router(build_crud_router(service=sales_invoice_service, create_schema=SalesInvoiceCreate, update_schema=SalesInvoiceUpdate, read_schema=SalesInvoiceRead, resource="sales"))
router.include_router(
    build_crud_router(service=sales_invoice_item_service, create_schema=SalesInvoiceItemCreate, update_schema=SalesInvoiceItemUpdate, read_schema=SalesInvoiceItemRead, resource="sales"),
    prefix="/items",
)
router.include_router(
    build_crud_router(service=payment_service, create_schema=PaymentCreate, update_schema=PaymentUpdate, read_schema=PaymentRead, resource="sales"),
    prefix="/payments",
)
router.include_router(
    build_crud_router(service=installment_plan_service, create_schema=InstallmentPlanCreate, update_schema=InstallmentPlanUpdate, read_schema=InstallmentPlanRead, resource="sales"),
    prefix="/installment-plans",
)
router.include_router(
    build_crud_router(
        service=installment_schedule_service,
        create_schema=InstallmentScheduleCreate,
        update_schema=InstallmentScheduleUpdate,
        read_schema=InstallmentScheduleRead,
        resource="sales",
    ),
    prefix="/installment-schedules",
)
