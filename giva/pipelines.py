# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
#
# from giva.customUtils import insert_into
# from giva.items import ProductRawItem, ProductDataItem
#
# class GivaPipeline:
#     def process_item(self, item, spider):
#         if isinstance(item, ProductRawItem):
#             copy_item = item.copy()
#             # copy_item.pop('id')
#
#             data_table_name = 'products_links'
#
#             cols = ', '.join(copy_item.keys())
#             values = tuple(copy_item.values())
#             placeholders = (', %s' * len(copy_item)).strip(', ')
#
#             insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)
#             try:
#                 print('Inserting Data into DB Table...')
#                 spider.cursor.execute(query=insert_query, args=values)
#                 print('Inserted Data...')
#             except Exception as e:
#                 print(e)
#         elif isinstance(item, ProductDataItem):
#             copy_item = item.copy()
#             # copy_item.pop('id')
#
#             data_table_name = 'products_data'
#
#             cols = ', '.join(copy_item.keys())
#             values = tuple(copy_item.values())
#             placeholders = (', %s' * len(copy_item)).strip(', ')
#
#             insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)
#             try:
#                 print('Inserting Data into DB Table...')
#                 spider.cursor.execute(query=insert_query, args=values)
#                 print('Inserted Data...')
#             except Exception as e:
#                 print(e)
#         return item

# Define your item pipelines here
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from giva.customUtils import insert_into
from giva.items import ProductRawItem, ProductDataItem


class GivaPipeline:
    def process_item(self, item, spider):
        # Determine the table based on item type
        if isinstance(item, ProductRawItem):
            data_table_name = 'products_links'
        elif isinstance(item, ProductDataItem):
            data_table_name = 'products_data'
        else:
            print('Skipped Processing...')
            # If the item type is unknown, skip processing
            return item

        copy_item = item.copy()

        cols = ', '.join(copy_item.keys())
        values = tuple(copy_item.values())
        placeholders = ', '.join(['%s'] * len(copy_item))

        insert_query = insert_into(table_name=data_table_name, cols=cols, placeholders=placeholders)

        try:
            print(f'Inserting {data_table_name} Data into DB Table...')
            spider.cursor.execute(query=insert_query, args=values)
            print('Inserted Data Successfully.')
        except Exception as e:
            print(f'Error inserting {data_table_name} data: {e}')
            # Optionally log the error or take other actions

        return item
