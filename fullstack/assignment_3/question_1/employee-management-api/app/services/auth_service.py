from app.core.security import create_access_token, get_password_hash, verify_password
from app.exceptions.custom_exceptions import AuthException, ConflictException, ValidationException
from app.repositories.user_repository import UserRepository
from app.repositories.employee_repository import EmployeeRepository

class AuthService:
    def __init__(self, user_repository: UserRepository, employee_repository: EmployeeRepository = None):
        self.user_repository = user_repository
        self.employee_repository = employee_repository

    async def register(self, email: str, password: str, role: str) -> dict:
        if role not in {"employee", "manager", "admin"}:
            raise ValidationException("Invalid role")

        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise ConflictException("Email already registered")

        hashed = get_password_hash(password)
        user = await self.user_repository.create({"email": email, "password": hashed, "role": role})
        
        if self.employee_repository:
            await self.employee_repository.create({
                "user_id": user["id"],
                "name": email.split("@")[0],
                "department": "Unassigned",
                "manager_id": None
            })

        token = create_access_token(user["id"], user["role"])
        return {"access_token": token, "token_type": "bearer", "role": user["role"]}

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user["password"]):
            raise AuthException("Invalid email or password")
        token = create_access_token(user["id"], user["role"])
        return {"access_token": token, "token_type": "bearer", "role": user["role"]}
