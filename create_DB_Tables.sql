CREATE DATABASE WildHummingbirds;
commit;

USE WildHummingbirds;

CREATE TABLE search_query (
search_id varchar(16) NOT NULL COMMENT 'The unique ID for search query',
search_query varchar(100) NOT NULL COMMENT 'search text', 
PRIMARY KEY (search_id)
);


CREATE TABLE urls (
engine_name varchar(20) NOT NULL COMMENT 'name of the search engine',
title varchar(250) DEFAULT NULL COMMENT 'title of the url ',
url varchar(500) NOT NULL COMMENT 'full URL',
snippet text DEFAULT NULL COMMENT 'Description of the url ',
url_id varchar(16) NOT NULL COMMENT 'url_id',
search_id varchar(16) NOT NULL COMMENT 'FK to as earch_idx table id',
PRIMARY KEY (url_id),
FOREIGN KEY (search_id) REFERENCES search_query(search_id)
);

CREATE TABLE content (
url_id varchar(16) NOT NULL COMMENT 'url_id',
url varchar(500) NOT NULL COMMENT 'full URL',
page_content mediumtext NOT NULL COMMENT 'page content', 
content_type varchar (50) Default 'bf' comment 'by default we will inset bf for beautiful soup', 
freq int DEFAULT NULL,
PRIMARY KEY (url),
FOREIGN KEY (url_id) REFERENCES urls(url_id)
);
commit;