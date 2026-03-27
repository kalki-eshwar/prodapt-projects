from fastapi import APIRouter, Depends

from app.dependencies.rbac import CurrentUser, get_current_user

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.get('/me')
def me(current_user: CurrentUser = Depends(get_current_user)):
	return current_user
