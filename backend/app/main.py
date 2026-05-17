from fastapi import FastAPI
from backend.app.api import(
    auth_routes,
    chat_routes,
    lead_routes,
    dashboard_routes,
    upload_routes, 
    workflow_routes
)
from backend.app.api.automation_routes import router as automation_router

app = FastAPI(
    title="Smart AI Buisness Assistant",
    version="1.0.0"
)

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(lead_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(upload_routes.router)
app.include_router(workflow_routes.router)
app.include_router(automation_router, prefix="/automation",tags=["Automation"])

@app.get("/")
async def root():
    return{
        "message":"AI Business Assistant Running"
    }