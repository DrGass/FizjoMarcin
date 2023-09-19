from fastapi import HTTPException, status


class UserExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project with given name already exists. Try again.",
        )
