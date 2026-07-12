from app.models.branch import Branch
from app.utils.helpers import CRUDService

branch_service = CRUDService(Branch, search_fields=("name", "code", "city"))
