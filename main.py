import uvicorn
from fastapi import FastAPI

from views import items
from views import users
from views import welcome


app = FastAPI()

app.include_router(items.router, tags=['items'])
app.include_router(users.router, tags=['users'])
app.include_router(welcome.router)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
