CREATE DATABASE WildHummingbirds;
commit;

USE WildHummingbirds;

CREATE TABLE search_query (
id varchar(16) NOT NULL COMMENT 'The unique ID of this analysis',
search_query varchar(100) NOT NULL COMMENT 'search text', 
PRIMARY KEY (id)
);


CREATE TABLE search_meta (
search_engine varchar(20) NOT NULL COMMENT 'name of the search engine',
url varchar(500) DEFAULT NULL COMMENT 'full URL',
title varchar(250) DEFAULT NULL COMMENT 'title of the url ',
snippet text DEFAULT NULL COMMENT 'Description of the url ',
url_id varchar(16) NOT NULL COMMENT 'url_id',
search_id varchar(16) DEFAULT NULL COMMENT 'FK to as earch_idx table id',
PRIMARY KEY (url_id),
FOREIGN KEY (search_id) REFERENCES search_query(id)
);

commit;
