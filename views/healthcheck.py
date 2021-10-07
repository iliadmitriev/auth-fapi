from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import InterfaceError
from starlette import status
from starlette.requests import Request

router = APIRouter()


@router.get(
    "/health", name="health-check",
    summary="check application health status",
    description="checks connection with database performing simple query and responds if it's OK"
)
async def health_check(request: Request):
    db = request.app.state.db
    try:
        res = await db.execute("select 1")
        one = res.scalar()
        assert str(one) == '1'
    except InterfaceError:
        return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Fail")
    return {"message": "OK"}
