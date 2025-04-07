drop table if exists stocks;

create table stocks (
	id SERIAL primary key,
	symbol VARCHAR(10) not null,
	name VARCHAR(100) not null,
	price DECIMAL(10,2),
	volume INT
);

drop table if exists users;

create table users (
	id SERIAL primary key,
	username VARCHAR(50) unique,
	password_hash VARCHAR(255),
	email VARCHAR(100)
);

drop table if exists watchlist;

create table watchlist (
	id SERIAL primary key,
	user_id INT not null references users(id) on delete cascade,
	stock_id INT not null references stocks(id) on delete cascade,
	alert_price DECIMAL(10,2), -- optional: set an alert price for notifications
	unique(user_id, stock_id) -- ensures a user cannott watch the same stock twice
);

drop table if exists notifications;

create table notifications (
    id SERIAL primary key,
    user_id INT not null references users(id) on delete cascade,
    stock_id INT references stocks(id),
    message TEXT not null,
    created_at TIMESTAMP default CURRENT_TIMESTAMP,
    is_read BOOLEAN default false
);