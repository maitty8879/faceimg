from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io
import uvicorn

app = FastAPI()

# Initialize session with u2netp (lightweight model) globally to save memory/time
# This is crucial for cloud deployments with limited resources (like Zeabur free tier)
model_name = "u2netp"
session = new_session(model_name)

# Allow CORS for Next.js frontend (usually localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, be more specific.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rembg Service is running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image content
        contents = await file.read()
        
        # Process with rembg
        # rembg expects bytes and returns bytes
        # Use the global session (u2netp)
        output_data = remove(contents, session=session)
        
        # Verify it's a valid image (optional but good for debugging)
        # image = Image.open(io.BytesIO(output_data))
        
        # Return as a response
        from fastapi.responses import Response
        return Response(content=output_data, media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
