import uvicorn
from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=router)

@app.get("/")
def read_root():
    return {
        "Status": "Success",
        "Message": "Guerrout"
    }

if __name__ == '__main__':
    uvicorn.run(f"main:app", host="127.0.0.1", port=8888, reload=True)
