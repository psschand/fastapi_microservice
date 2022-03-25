from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, tasks

from app.api.routes import router as api_router
from fastapi.responses import HTMLResponse

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix="/api")

    @app.get("/")
    async def main():
        content = """
    <body>
    <h3> Welcome to election results </h3>
    <p> go to http://localhost:8000/docs to test the backend api </p>
    </body>
        """
        return HTMLResponse(content=content)

    return app


app = get_application()
