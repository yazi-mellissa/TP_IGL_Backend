from fastapi import HTTPException, status

class HTTPResponse(HTTPException):
    def __init__(self, status_code : status, detail : str | dict):
        if ( detail is str):
            super().__init__(
                status_code=status_code,
                detail={
                    "message":detail
                }
            )
        else:
            super().__init__(
                status_code=status_code,
                detail=detail
            )