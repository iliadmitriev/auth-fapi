import uvicorn
from fastapi import FastAPI

from views import items, users, welcome, healthcheck
from db.database import app_init_db, app_dispose_db

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    await app_init_db(app)


@app.on_event('shutdown')
async def shutdown_event():
    await app_dispose_db(app)


app.include_router(items.router, tags=['items'])
app.include_router(users.router, tags=['users'])
app.include_router(healthcheck.router, tags=['status'])
app.include_router(welcome.router)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
