COPY brand(brand_name) FROM '/data/brand.csv' DELIMITER ',' CSV HEADER;
COPY category(category_name) FROM '/data/category.csv' DELIMITER ',' CSV HEADER;
COPY item(item_name,item_price,category_id,brand_id) FROM '/data/item.csv' DELIMITER ',' CSV HEADER;
