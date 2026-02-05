from fastapi import APIRouter
import gc

router = APIRouter()


@router.get("/")
def get_health():
    """
    Simple health check endpoint
    """
    gc.collect()
    return {"status": "ok"}
