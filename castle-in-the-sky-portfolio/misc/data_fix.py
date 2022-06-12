import time
import pandas as pd
from db_config import engine


connection = engine.connect()
#Check all 7 tables

def fix_data_to_excel(db_name):
    db_name = db_name
    # Retrive Data
    df = pd.read_sql(f'{db_name}', connection) # Only Take Columns Needed
    df = df.drop_duplicates(subset=['Date'])
    df.to_excel(f'Misc/{db_name}.xlsx', index=False)
    

def upload_fixed_data(db_name):
    db_name = db_name
    # Do after wiping database
    df = pd.read_excel(f'Misc/{db_name}.xlsx')
    df.to_sql(f'{db_name}', con=engine, if_exists='append', index=False)

# fix_data_to_excel(db_name='eps')
# fix_data_to_excel(db_name='sentiment')
# fix_data_to_excel(db_name='prices')
# fix_data_to_excel(db_name='allocations')
# fix_data_to_excel(db_name='shares')
# fix_data_to_excel(db_name='portfolio')
# fix_data_to_excel(db_name='totalPortfolioValue')

# upload_fixed_data(db_name='eps')
# upload_fixed_data(db_name='sentiment')
# upload_fixed_data(db_name='prices')
# upload_fixed_data(db_name='allocations')
# upload_fixed_data(db_name='shares')
# upload_fixed_data(db_name='portfolio')
# upload_fixed_data(db_name='totalPortfolioValue')