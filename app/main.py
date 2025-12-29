"""
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import webhook

app = FastAPI (
	title="CI Pipeline scanner",
	description="Automated security scanner for code repo",
	version="0.1.0"
	)

app.add_middleware(
	CORSMiddleware, 
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
	)

app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])

@app.get("/")
async def root():
	return {
		"status": "ok",
		"message":"CI Pipeline Scanner",
		"version": "0.1.0"
	}

@app.get("/health")
async def health():
	return {"status":"healthy"}

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=3000)
