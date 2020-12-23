CREATE TABLE category (
	category_id serial PRIMARY KEY,
	category_name VARCHAR ( 50 ) UNIQUE NOT NULL
);

CREATE TABLE brand (
	brand_id serial PRIMARY KEY,
	brand_name VARCHAR (50) UNIQUE NOT NULL
);

CREATE TABLE item(
	item_id serial PRIMARY KEY,
	item_name VARCHAR (50) NOT NULL,
	item_price MONEY,
	category_id int NOT NULL,
	brand_id int NOT NULL,
	FOREIGN KEY (category_id) REFERENCES category(category_id) ON UPDATE CASCADE,
	FOREIGN KEY (brand_id) REFERENCES brand(brand_id) ON UPDATE CASCADE
);

CREATE TABLE orders(
	order_id serial PRIMARY KEY,
	order_time TIMESTAMPTZ,
	item_id int NOT NULL,
	FOREIGN KEY (item_id) REFERENCES item(item_id) ON UPDATE CASCADE
);
