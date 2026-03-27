import os
base_dir = r"c:\Users\Administrator\Documents\Assignments\prodapt-projects\fullstack\assignment_3\question_3\enterprise_asset_mgmt"

files = {
    "app/schemas/asset_schema.py": "from pydantic import BaseModel\nclass AssetCreate(BaseModel):\n    asset_tag: str\n    asset_type: str\n    brand: str\n    model: str\n    department_id: int",
    "app/schemas/request_schema.py": "from pydantic import BaseModel\nclass RequestCreate(BaseModel):\n    asset_type: str\n    reason: str",
    "app/schemas/assignment_schema.py": "from pydantic import BaseModel\nclass AssignmentCreate(BaseModel):\n    asset_id: int\n    user_id: int",

    "app/routers/superadmin_router.py": "from fastapi import APIRouter\nfrom app.schemas.asset_schema import AssetCreate\nrouter = APIRouter(prefix='/superadmin', tags=['SuperAdmin'])\n@router.post('/assets')\ndef create_asset(asset: AssetCreate):\n    return {'message': 'Asset created', 'asset': asset.model_dump()}\n@router.get('/assets')\ndef get_all_assets():\n    return {'message': 'All assets'}",

    "app/routers/itadmin_router.py": "from fastapi import APIRouter\nfrom app.schemas.assignment_schema import AssignmentCreate\nrouter = APIRouter(prefix='/itadmin', tags=['ITAdmin'])\n@router.post('/assignments')\ndef assign_asset(assignment: AssignmentCreate):\n    return {'message': 'Asset assigned', 'assignment': assignment.model_dump()}\n@router.post('/requests/{request_id}/approve')\ndef approve_request(request_id: int):\n    return {'message': f'Request {request_id} approved'}\n@router.post('/assignments/{assignment_id}/return')\ndef return_asset(assignment_id: int):\n    return {'message': f'Asset returned for assignment {assignment_id}'}",

    "app/routers/manager_router.py": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/manager', tags=['Manager'])\n@router.get('/department/assets')\ndef view_department_assets():\n    return {'message': 'List of department assets'}\n@router.get('/assets')\ndef view_own_assets():\n    return {'message': 'List of own assets'}",

    "app/routers/employee_router.py": "from fastapi import APIRouter\nfrom app.schemas.request_schema import RequestCreate\nrouter = APIRouter(prefix='/employee', tags=['Employee'])\n@router.post('/requests')\ndef create_request(req: RequestCreate):\n    return {'message': 'Request created', 'request': req.model_dump()}\n@router.get('/assets')\ndef view_own_assets():\n    return {'message': 'List of own assets'}",

    "app/main.py": "from fastapi import FastAPI\nfrom app.database.base import Base\nfrom app.database.session import engine\nimport app.models\nfrom app.routers import superadmin_router, itadmin_router, manager_router, employee_router\n\nBase.metadata.create_all(bind=engine)\n\napp = FastAPI(title='EAMS')\n\napp.include_router(superadmin_router.router)\napp.include_router(itadmin_router.router)\napp.include_router(manager_router.router)\napp.include_router(employee_router.router)\n\n@app.get('/')\ndef root(): return {'message': 'EAMS API Root'}"
}

for path, content in files.items():
    with open(os.path.join(base_dir, path), "w", encoding="utf-8") as f:
        f.write(content)
print("Files created.")
