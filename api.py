import logging
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import JTBDMultiAgentSystem
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize the JTBD Multi-Agent System
try:
    logger.info("Initializing JTBD Multi-Agent System")
    jtbd_system = JTBDMultiAgentSystem()
    logger.info("JTBD Multi-Agent System initialized successfully")
except Exception as e:
    logger.error(f"Error initializing JTBD Multi-Agent System: {str(e)}")
    logger.error(traceback.format_exc())
    raise

# Create FastAPI app
app = FastAPI(
    title="JTBD Multi-Agent System API",
    description="API for processing user queries using the Jobs To Be Done framework",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request model
class QueryRequest(BaseModel):
    query: str

# Define routes
@app.get("/")
async def root():
    return {"message": "JTBD Multi-Agent System API. Use /process endpoint to submit queries."}

@app.post("/process")
async def process_query(request: QueryRequest):
    """
    Process a user query through the JTBD Multi-Agent System.
    
    Args:
        request: QueryRequest containing the user's query
        
    Returns:
        dict: Response from the appropriate agent(s)
    """
    try:
        logger.info(f"Processing query: {request.query}")
        # Process the query using the JTBD Multi-Agent System
        result = jtbd_system.process_query(request.query)
        logger.info("Query processed successfully")
        return result
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    logger.info("Starting API server on port 8002")
    uvicorn.run(app, host="0.0.0.0", port=8002) 