
import pandas as pd
import pymysql

# # Creating a connection to SQL Database
connection = pymysql.connect(host='localhost', user='root', database='giva_db', password='actowiz', charset='utf8mb4', autocommit=True)

fetch_query = '''SELECT * FROM products_data;'''  # Query that will retrieve all data from Database table

project_name = 'giva_Project_Files'
excel_path = rf'C:\Project Files (using Scrapy)\{project_name}\Output_Files'
# Create Excel file form SQL data
dataframe = pd.read_sql(sql=fetch_query, con=connection)
writer = pd.ExcelWriter(
    path=excel_path + r'\giva_products_data_old.xlsx',
    engine='xlsxwriter',
    engine_kwargs={'options': {'strings_to_urls': False}}
)
dataframe.to_excel(excel_writer=writer)

dataframe.to_excel(writer)
writer.close()
