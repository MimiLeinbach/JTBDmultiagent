import logging
import sys
from utils.data_generator import generate_sample_datasets

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Generating test data for the JTBD Multi-Agent System")
    generate_sample_datasets()
    logger.info("Test data generation complete") 