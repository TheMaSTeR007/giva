# Dynamic Insert query
def insert_into(table_name, cols, placeholders):
    insert_query = f'''INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders});'''
    return insert_query


products_links_table_query = '''CREATE TABLE products_links (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                product_name VARCHAR(255),
                                product_url VARCHAR(255) UNIQUE,
                                url_status VARCHAR(255) DEFAULT 'pending'
                                );'''

products_data_table_query = '''CREATE TABLE product_data (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                product_name VARCHAR(255),
                                product_url VARCHAR(255),
                                product_image_url VARCHAR(255),
                                product_description TEXT,
                                product_sku VARCHAR(255),
                                product_brand VARCHAR(255),
                                product_offer_price VARCHAR(255),
                                product_currency VARCHAR(255),
                                product_variant_url VARCHAR(255),
                                product_rating_value VARCHAR(255),
                                product_review_count VARCHAR(255),
                                shipping_data TEXT,
                                pincode VARCHAR(255),
                                delivery_time_message VARCHAR(255)
                                );'''
