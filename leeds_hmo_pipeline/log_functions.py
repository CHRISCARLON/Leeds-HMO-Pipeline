from loguru import logger
import os 
import datetime


# Call and configure loguru at the start of main.py
def configure_logger():
    log_dir = "log_files"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, "warnings.txt")
    logger.add(log_file_path, format="{time} {level} {message}", level="WARNING", rotation="5 MB")


def check_rename(df, df2):
    df = df.columns.tolist()
    df2 =  df2.columns.tolist()
    
    # Verify if the renaming was successful
    # The columns should not be equal if renaming had worked (v basic check)
    if set(df2) != set(df):
        logger.success("Column renaming was successful.")
    else:
        logger.warning("Column renaming failed. Check the column names.")


def check_cols(df):
    # Does the source data have the expected columns? These may change in the future.
    # Might need a better way to capture this rather than hard coding them in!
    actual_columns = df.columns.tolist()
    expected_columns = ["Street name", "Address", "Renewal Date", "Licence Holder", "Maximum Permitted Number of Tenants"]

    missing_columns = set(expected_columns) - set(actual_columns)
    additional_columns = set(actual_columns) - set(expected_columns)

    # Log and raise an exception for discrepancies
    if missing_columns:
        message = f"Missing expected columns: {missing_columns}"
        logger.warning(message)
        raise ValueError(message)  

    if additional_columns:
        message = f"Additional columns not expected: {additional_columns}"
        logger.warning(message)
        raise ValueError(message)  
    
    if not missing_columns and not additional_columns:
        logger.success("DataFrame columns match the expected columns.")
        

def check_added_cols(df):
    # Have the 3 extra columns been added correctly?
    if "date_added" in df.columns:
        logger.success("date added")
    if "postcode" in df.columns:
        logger.success("postcode added")
    if "coordinates" in df.columns:
        logger.success("coordinates added")
    else: 
        df_logged = df.columns
        message = f"Missing either date_added, postcode, or coordinates column: {df_logged}"
        logger.warning(message)
        raise ValueError(message)  
            

def log_missing_postcodes(df, column_name):
    # Find rows with missing postcode values and log them
    missing_vals_df = df[df[column_name].isna()]

    if not missing_vals_df.empty:
        now = datetime.datetime.now()
        missing_vals_info = f"Missing values for '{column_name}' logged on {now.strftime('%Y-%m-%d %H:%M:%S')}:\n{missing_vals_df.to_string(index=False)}\n\n"
        logger.warning(missing_vals_info)
    else:
        logger.success(f"No missing values found for '{column_name}' on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")