
from constants import Paths
import logging
import pandas as pd
logger = logging.getLogger(__name__)

class Loader:

    def __init__(self, df :pd.DataFrame ):

        # final output_df
        self._df = df



    def save(self):

        out_dir = Paths.OUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        csv_path = out_dir / "orders_sample_clean.csv"
        self._df.to_csv(csv_path, index=False)
        logger.info(f"saved CSV   -> {csv_path} ({csv_path.stat().st_size:,} bytes)")  