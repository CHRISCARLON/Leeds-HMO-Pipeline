import pandas as pd
import os
from dotenv import load_dotenv
from loguru import logger
from download_functions import data_url, load_excel_into_memory
from json_functions import current_local_date, update_json
from log_functions import configure_logger, check_cols, log_missing_postcodes, check_rename, check_added_cols
from website_date import find_the_date
from data_transformation_functions import date_from_url, remove_dots_from_date, new_date_added_column, add_postcode_column ,extract_unique_postcodes, get_coords, rename_cols
from database_push import connect_to_motherduck, load_into_duckdb

load_dotenv()

def main():
    
    configure_logger()
    
    base_url = os.getenv('base_url')
    website_date = find_the_date(base_url)
    
    local_date = current_local_date('date_holder.json')
    
    if local_date != website_date:
        logger.info("Strings are different. Updating Current Json date file and fetching download link.")
        update_json('date_holder.json', website_date)
    else:
        logger.info("Dates are the same. No update or download needed.")
        return

    download_data_url = data_url(base_url)
    
    df = load_excel_into_memory(download_data_url)
    check_cols(df)
    
    df2 = rename_cols(df)
    check_rename(df, df2)
    
    date = date_from_url(download_data_url)
    date2 = remove_dots_from_date(date)
    df2 = new_date_added_column(df2, date2)

    df2 = add_postcode_column(df2)
    log_missing_postcodes(df2, 'postcode')
    
    post_code_list = extract_unique_postcodes(df2)
    coords = get_coords(post_code_list)
    
    df2 = pd.merge(df2, coords, on='postcode', how='left')
    check_added_cols(df2)
    
    db_name = os.getenv("db_name")
    con = connect_to_motherduck(db_name)
    load_into_duckdb(con, date2, df2)
    print("Success")
    
if __name__ == "__main__":
    main()