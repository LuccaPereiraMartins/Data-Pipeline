import pandas as pd
import numpy as np
import os
from processors import parse, upload
from mapping import mapping_dict
from logging_config import logger

'''
In this assignment, your objective is to design and implement a simplified version of
an application that ingests data from multiple sources and formats, harmonizes the
data and then allows other services to consume it with an API.
'''

def pipeline(
    source_folder: str,
    output_path: str,
    to_upload: bool = True
):

    # create empty dataframe to append each file to
    # initialise the column headers with target mapping for shape
    # TODO write this manually for now, although it should be retrieved from the mapping dict
    cols = ['date','nt_fund_code','ticker',
    	'nt_currency','nt_gti_code','exchange_name',
        'nt_country_name','nt_bloomberg_code','nt_bloomberg_id',
        'nt_quantity','price']
    df_all = pd.DataFrame(columns=cols)

    # iterate through all the files in the source folder
    ls_source_folder = [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]

    for file in ls_source_folder:
        # create the path name
        path = f'{source_folder}/{file}'
        # load cleaned file from a path
        data = parse(file_path=path,mapping_dict=mapping_dict)

        if not data.empty:
            logger.info('Modifying dataframe')
            # iterate through each row
            for index, row in data.iterrows():
                # check if ticker exists in df_all
                if row['ticker'] in df_all['ticker'].values:
                    # find the index of the existing row
                    existing_index = df_all[df_all['ticker'] == row['ticker']].index[0]
                    # update the existing row with new/updated values
                    df_all.loc[existing_index] = df_all.loc[existing_index].fillna(row)
                    # TODO function that compares existing to current, ie patching for data quality, updates entry if passes checks
                    # accounts for more than just the fillna
                else:
                    # add the row to df_all
                    df_all = pd.concat([df_all, pd.DataFrame([row])], ignore_index=True)

                # ideally, use a SQL style outer join, can't seem to get it to work
                # df_all.merge(right=data, left_index=True, right_index=True, how='outer')
                # otherwise this line showed promise but couldn't quite get it to work
                # df_all.join(other=data,how='outer',rsuffix='df2')


    # final processing steps like dropping duplicates or str.lower()
    # TODO not sure this works exactly as intended
    df_all.set_index(keys='ticker',inplace=True)

    # simple dataframe with company information that should stay consistent
    df_info = df_all[[
        'nt_currency','exchange_name',
        'nt_country_name','nt_bloomberg_code',
        'nt_bloomberg_id'
    ]].copy()

    # stacked dataframe with ticker > date > price to handle several dates worth of prices per ticker
    # TODO also not sure this works exactly as intended
    df_prices = df_all[[
        'date', 'price'
    ]].copy()
    df_prices.stack(future_stack=True)

    # check if data is present before upload
    # ideally, use more descriptive name (date, source, etc.)
    if not df_all.empty and to_upload:
        filename = 'test.csv'
        upload(
            data=df_all, 
            output_path=f'{output_path}/{filename}',
        )
        upload(
            data=df_info, 
            output_path=f'{output_path}/reference_info.csv',
        )
        upload(
            data=df_prices, 
            output_path=f'{output_path}/prices.csv',
        )

    # return the dataframes in case we want to use their df properties
    return df_all, df_info, df_prices 

# call the pipeline here for testing purposes
def main():

    # run pipeline
    logger.info('Started running pipeline')
    pipeline(
        source_folder='source',
        output_path='processed',
        to_upload=True)
    logger.info('Finished running pipeline')


if __name__ == '__main__':
    main()