import pandas as pd
import logging

logger =logging.getLogger(__name__)

class Transformer:

    def __init__(self, df: pd.DataFrame):
        self._df = df
        
    
    def run(self):    

        self._drop_duplicate()
        self._clean_amount()
        self._clean_dates()
        self._clean_keys()

        return self._df

    def _drop_duplicate(self):

        before =len(self._df)
        self._df =self._df.drop_duplicates(subset="order_id", keep='first')
        after = len(self._df)

        logger.info(f"Duplicate removal: before: {before} rows → after: {after} rows ")

    
    def _clean_amount(self):

        before = len(self._df)
        self._df["amount"] = self._df['amount'].replace(r"[a-zA-Z, ]", "",regex=True)\
                                                .replace(r"\.(?=.*\.)","",regex=True)
        # converts text into number.
        self._df["amount"] = pd.to_numeric(self._df["amount"],errors='coerce')

        # removes rows where the amount column contains missing values
        self._df = self._df.dropna(subset='amount')
        after = len(self._df)

        logger.info(f"Amount cleaning: before: {before} rows → after: {after} rows")


    def _clean_dates(self):

        col  = self._df['order_date'].astype("string").str.strip()
        # converting the text into number will catch Excel date form "45661 only and will make other dates be null
        numeric = pd.to_numeric(col,errors='coerce')
        # get the numbers between 20000 and 60000 which are the Excel dates
        mask  = numeric.between(20000,60000)
        
        col.loc[mask] = (
            pd.to_datetime(numeric.loc[mask],unit='D',origin="1899-12-30").dt.strftime("%Y-%m-%d")
        )

        mask_compact = col.str.fullmatch(r"\d{8}",na=False)
        col.loc[mask_compact] = (
            col.loc[mask_compact].str[:4]
            + "-"
            +col.loc[mask_compact].str[4:6]
            + "-"
            +col.loc[mask_compact].str[6:8]
        )

        self._df['order_date'] = pd.to_datetime(
            col,
            format='mixed',
            dayfirst=True,
            errors='coerce'
        )

        logger.info("dates: %d unreadable kept as NaT ",
                       self._df['order_date'].isna().sum())
        


    def _clean_keys(self):
    
        self._df['city'] = self._df['city'].str.strip().str.lower().str.title()

        self._df['customer_id'] = self._df['customer_id'].fillna("Guest")

                




