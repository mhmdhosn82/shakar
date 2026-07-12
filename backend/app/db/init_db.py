from __future__ import annotations

from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import AsyncSessionLocal, engine
from app.core.logging import get_logger
from app.core.security import get_password_hash
from app.models import Account, AccountType, Base, Branch, Permission, Role, RolePermission, User, Warehouse

logger = get_logger(__name__)

DEFAULT_ROLE_MAP = {
    "admin": "Full administrative access",
    "manager": "Operational management access",
    "salesperson": "Sales and customer operations",
    "cashier": "Payment handling access",
    "warehouse_keeper": "Inventory and purchasing operations",
    "accountant": "Accounting and financial operations",
}

DEFAULT_ACCOUNTS = [
    ("1000", "Cash", AccountType.asset),
    ("1100", "Bank", AccountType.asset),
    ("1200", "Accounts Receivable", AccountType.asset),
    ("2000", "Accounts Payable", AccountType.liability),
    ("3000", "Owner Equity", AccountType.equity),
    ("4000", "Sales Revenue", AccountType.income),
    ("5000", "Cost of Goods Sold", AccountType.expense),
]

DEFAULT_PERMISSIONS = {
    "users": ["read", "create", "update", "delete"],
    "roles": ["read", "create", "update", "delete"],
    "permissions": ["read", "create", "update", "delete"],
    "branches": ["read", "create", "update", "delete"],
    "categories": ["read", "create", "update", "delete"],
    "brands": ["read", "create", "update", "delete"],
    "products": ["read", "create", "update", "delete"],
    "warehouses": ["read", "create", "update", "delete"],
    "inventory": ["read", "create", "update", "delete"],
    "customers": ["read", "create", "update", "delete"],
    "suppliers": ["read", "create", "update", "delete"],
    "sales": ["read", "create", "update", "delete"],
    "purchases": ["read", "create", "update", "delete"],
    "accounting": ["read", "create", "update", "delete"],
    "backup": ["read", "create"],
    "audit": ["read", "create", "update", "delete"],
}

ROLE_GRANTS = {
    "admin": list(DEFAULT_PERMISSIONS.keys()),
    "manager": ["branches", "categories", "brands", "products", "warehouses", "inventory", "customers", "suppliers", "sales", "purchases", "accounting", "audit"],
    "salesperson": ["products", "categories", "brands", "customers", "sales", "branches"],
    "cashier": ["sales", "customers", "branches"],
    "warehouse_keeper": ["products", "categories", "brands", "inventory", "warehouses", "purchases", "suppliers", "branches"],
    "accountant": ["accounting", "sales", "purchases", "customers", "suppliers", "audit"],
}


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    settings = get_settings()
    async with AsyncSessionLocal() as session:
        branch = await session.scalar(select(Branch).where(Branch.code == "MAIN"))
        if branch is None:
            branch = Branch(name="Main Branch", code="MAIN", city="Tehran", address="Headquarters")
            session.add(branch)
            await session.flush()

        permission_map: dict[tuple[str, str], Permission] = {}
        for resource, actions in DEFAULT_PERMISSIONS.items():
            for action in actions:
                permission = await session.scalar(
                    select(Permission).where(Permission.resource == resource, Permission.action == action)
                )
                if permission is None:
                    permission = Permission(
                        resource=resource,
                        action=action,
                        description=f"Allows {action} access on {resource}",
                    )
                    session.add(permission)
                    await session.flush()
                permission_map[(resource, action)] = permission

        role_map: dict[str, Role] = {}
        for code, description in DEFAULT_ROLE_MAP.items():
            role = await session.scalar(select(Role).where(Role.code == code))
            if role is None:
                role = Role(name=code.replace("_", " ").title(), code=code, description=description)
                session.add(role)
                await session.flush()
            role_map[code] = role
            existing_permissions = {
                rp.permission_id
                for rp in (await session.scalars(select(RolePermission).where(RolePermission.role_id == role.id))).all()
            }
            granted_permission_ids = {
                permission_map[(resource, action)].id
                for resource in ROLE_GRANTS[code]
                for action in DEFAULT_PERMISSIONS[resource]
            }
            for permission_id in granted_permission_ids - existing_permissions:
                session.add(RolePermission(role_id=role.id, permission_id=permission_id))

        admin_role = role_map["admin"]
        superuser = await session.scalar(select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL))
        if superuser is None:
            superuser = User(
                email=settings.FIRST_SUPERUSER_EMAIL,
                username="admin",
                hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
                full_name="System Administrator",
                role_id=admin_role.id,
                branch_id=branch.id,
                is_active=True,
                is_superuser=True,
            )
            session.add(superuser)

        cash_account_exists = await session.scalar(select(Account).where(Account.code == DEFAULT_ACCOUNTS[0][0]))
        if cash_account_exists is None:
            for code, name, account_type in DEFAULT_ACCOUNTS:
                session.add(Account(code=code, name=name, account_type=account_type, description=f"Default {name} account"))

        warehouse = await session.scalar(select(Warehouse).where(Warehouse.code == "MAIN-WH"))
        if warehouse is None:
            session.add(
                Warehouse(
                    name="Main Warehouse",
                    code="MAIN-WH",
                    branch_id=branch.id,
                    address="Main branch warehouse",
                    is_active=True,
                )
            )

        await session.commit()
        logger.info("database-initialized", project=settings.PROJECT_NAME)
