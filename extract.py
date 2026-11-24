from pathlib import Path
from constants import Paths
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Extractor:
    def __init__(self):
        self._df = None


    def extract(self):

        Paths.WORK_DIR.mkdir(exist_ok=True)
        input_file = Paths.INPUT_FILE
            
        if  not Path.exists(input_file):
            raise FileNotFoundError(input_file)

        self._df =  pd.read_csv(input_file)
        logger.info(f"extract file :{input_file.name} with {len(self._df)} rows")
         
        return  self._df  

