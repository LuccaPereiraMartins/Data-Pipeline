import logging

# Configure the logger
logging.basicConfig(
    filename='test_filename.log',           
    level=logging.INFO,           
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('test_loggername')