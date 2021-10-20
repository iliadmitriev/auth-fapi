import uvicorn
from fastapi import FastAPI

from views import items, users, welcome, healthcheck, login
from db.database import app_init_db, app_dispose_db

description = """
**API with HTTP Bearer authorization using JWT token**
"""

openapi_tags = [
    {
        'name': 'login',
        'description': 'operations for users to register, login, logout or refresh token'
    },
    {
        'name': 'users',
        'description': 'admin operations with users accounts: find, create, update, delete',
        'externalDocs': {
            'description': 'Read more',
            'url': 'https://iliadmitriev.github.io/auth-fapi/'
        }
    },
    {
        'name': 'status',
        'description': 'application status check methods'
    }
]

app = FastAPI(
    title="Auth-fAPI",
    version='0.0.1',
    description=description,
    openapi_tags=openapi_tags,
    contact={
        'name': 'Ilia Dmitriev',
        'url': 'https://iliadmitriev.github.io/iliadmitriev/',
        'email': 'ilia.dmitriev@gmail.com'
    },
    license_info={
        'name': 'MIT License',
        'url': 'https://github.com/iliadmitriev/auth-fapi/blob/master/LICENSE'
    }
)


@app.on_event('startup')
async def startup_event():
    await app_init_db(app)


@app.on_event('shutdown')
async def shutdown_event():
    await app_dispose_db(app)


app.include_router(login.router, tags=['login'])
app.include_router(users.router, tags=['users'])
app.include_router(items.router, tags=['items'])
app.include_router(welcome.router)
app.include_router(healthcheck.router, tags=['status'])

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
