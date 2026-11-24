from constants import Paths
from extract import Extractor
from transform import Transformer
import logging
from load import Loader
from logging_setup import setup_logging,log_step


setup_logging()
logger = logging.getLogger(__name__)

def main():
    
    logger.info("========== ETL PIPELINE STARTED ==========")

    try: 
        
        # Extract
        with log_step(logger, "extract"):
            extractor = Extractor()
            main_df = extractor.extract()


        # take a look on csv files after extract to know what should you clean
        with log_step(logger, " analysis"):
            df =get_table_after_analyze(main_df, Paths.INPUT_FILE)


        # Transform
        with log_step(logger,"Transform"):
            transformer = Transformer(df)
            clean_df = transformer.run()


        # Load
        with log_step(logger, "Load"):
            loader = Loader(clean_df)
            loader.save()   
                
                
                
        logger.info("========== ETL PIPELINE COMPLETED ==========")
    except Exception:
        logger.exception("ETL pipeline failed") 



def get_table_after_analyze( main_df, input_file):
    
    df = main_df.copy()
    input_file.name
    
    logger.info(f"table {input_file.name} : {df.head(3)}")
    logger.info(f"read {input_file.name}: {df.shape[0]} rows x {df.shape[1]} columns")
    logger.info(f"dtypes {input_file.name}: {df.dtypes}")
    logger.info(f"duplicates {input_file.name}: {df.duplicated().sum()}")
    logger.info(f"Missing values {input_file.name}: {df.isna().sum()}")
    
    return df



if __name__ == "__main__":
    main()        

    
