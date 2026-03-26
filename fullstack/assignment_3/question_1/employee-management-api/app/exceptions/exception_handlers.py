from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import AppException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        has_json_decode_error = any(error.get("type") == "json_invalid" for error in errors)

        if has_json_decode_error:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Invalid JSON body. Use double quotes for keys/values and no trailing commas.",
                    "example": {
                        "email": "admin@example.com",
                        "password": "admin123",
                        "role": "admin",
                    },
                },
            )

        return JSONResponse(status_code=422, content={"detail": errors})
