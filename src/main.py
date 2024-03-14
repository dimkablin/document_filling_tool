"""Main function for running the API service."""
# mypy: ignore-errors
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8001,
        reload=False
    )  # nosec
