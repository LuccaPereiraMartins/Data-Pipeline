import pandas as pd
import numpy as np
from logging_config import logger



'''
consider using the following data standardization:
MIC codes for nt_exchange_name
Tickers or LEIs for company description
3 letter currency code (as per source)
3 letter country code for nt_country_name
quantity in int
price in 2dp float
dates in YYYY-MM-DD format
'''




def parse(
    file_path: str,
    mapping_dict: dict
) -> pd.DataFrame:
    """_summary_

    Args:
        file_path (str): source path with raw data
        mapping_dict (dict): mapping keys for data

    Returns:
        dataframe with mapped keys and data types
    """

    # retrieve the column & datatype mappings
    column_mapping = {k: v['name'] for k, v in mapping_dict.items()}
    data_types = {v['name']: v['data_type'] for v in mapping_dict.values()}

    # read in the file
    df = pd.read_csv(filepath_or_buffer=file_path, index_col=None, header=0)
    # drop the duplicates
    # TODO likely a better way to verify data before dropping than just keeping last
    df.drop_duplicates(inplace=True,keep='last',ignore_index=True)
    # map column headers and datatypes
    df.rename(columns=column_mapping, inplace=True)
    df.astype(dtype=data_types)
    # columns can also be manually converted one by one, better for non-standard formats
    # format date
    df['date'] = pd.to_datetime(df['date'])
    # clean the description column to use as index
    df['ticker'].str.strip().str.lower()
    # TODO ideally a step to convert from names to tickers/LEIs, something more standardized

    return df


def upload(
    data: pd.DataFrame,
    output_path: str,
):

    # upload the final df to the appropriate database
    # for now, create a csv in a defined filepath

    # try except for uploading data, more useful when connecting to databases in case of failure
    try:
        data.to_csv(
            path_or_buf=output_path,
            index=True,
        )
        logger.info('Upload succeeded')
    except Exception as e:
        logger.warning('warn')
