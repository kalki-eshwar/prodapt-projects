from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.rbac import CurrentUser, require_roles
from app.models.asset import Asset
from app.schemas.asset_schema import AssetCreate, AssetResponse

router = APIRouter(prefix='/superadmin', tags=['SuperAdmin'])


@router.post('/assets', response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN')),
):
    existing = db.query(Asset).filter(Asset.asset_tag == asset.asset_tag).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Asset tag already exists',
        )

    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


@router.get('/assets', response_model=List[AssetResponse])
def get_all_assets(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles('SUPERADMIN', 'IT_ADMIN')),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status_filter: str | None = Query(None, alias='status'),
    search: str | None = Query(None),
):
    query = db.query(Asset)

    if status_filter:
        query = query.filter(Asset.status == status_filter.upper())
    if search:
        query = query.filter(Asset.asset_tag.ilike(f'%{search}%'))

    return query.offset((page - 1) * size).limit(size).all()
