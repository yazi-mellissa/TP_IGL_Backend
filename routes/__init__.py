from fastapi import APIRouter
from routes.Authentification import router as auth_router
from routes.Administrateur import router as admin_router
from routes.Utilisateur import router as user_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth", tags=["Authentification"])
router.include_router(router=admin_router, prefix="/admin", tags=["Administrateur"])
router.include_router(router=user_router, prefix="/user", tags=["Utilisateur"])