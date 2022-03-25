from fastapi import APIRouter


from app.api.routes.election import router as elections_router


router = APIRouter()




router.include_router(elections_router, prefix="/elections", tags=["elections"])

