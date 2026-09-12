from typing import Annotated

from clerk_backend_api import (
    AuthenticateRequestOptions,
    authenticate_request,
)
from fastapi import Depends, HTTPException, Request

from app.config import settings


# --------------------------------------------------
# Clerk Authentication
# --------------------------------------------------

def require_user(request: Request) -> str:
    """
    Verify the Clerk session token from the request.

    Returns the authenticated Clerk user ID when
    authentication is successful.
    """

    authorized_parties = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.clerk_secret_key,
            jwt_key=settings.clerk_jwt_key or None,
            authorized_parties=authorized_parties,
            accepts_token=["session_token"],
        ),
    )

    if not state.is_signed_in:
        raise HTTPException(
            status_code=401,
            detail=(
                state.reason.name
                if state.reason
                else "User is not authenticated."
            ),
        )

    user_id = state.payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user ID was not found.",
        )

    return user_id


# --------------------------------------------------
# Current User Dependency
# --------------------------------------------------

CurrentUser = Annotated[
    str,
    Depends(require_user),
]