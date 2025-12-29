import uvicorn

if __name__ == "__main__":
	print("Starting server: localhost:3333")
	uvicorn.run("app:app", host="0.0.0.0", port=3333, reload=True)
