
 -- 1. bringing all of the relevant information together
SELECT DISTINCT
 q.search_query,
-- u.engine_name, 
u.title, 
-- u.snippet, 
u.url,
-- c.content_type, 
c.freq
FROM WildHummingbirds.urls u 
JOIN WildHummingbirds.content c ON c.url = u.url
LEFT JOIN WildHummingbirds.search_query q ON u.search_id = q.search_id
WHERE freq IS NOT NULL
ORDER BY search_query, freq DESC;

-- 2.1 total frequency by search engine
SELECT 
q.search_query,
u.engine_name, 
u.title, 
-- u.snippet, 
u.url,
c.content_type, 
c.freq,
ROUND(SUM(freq) OVER(PARTITION BY search_query, engine_name),2) AS total_freq
FROM WildHummingbirds.urls u 
JOIN WildHummingbirds.content c ON c.url = u.url
LEFT JOIN WildHummingbirds.search_query q ON u.search_id = q.search_id
WHERE freq IS NOT NULL
ORDER BY search_query, total_freq DESC;


WITH base as (
-- 2.2 search engine ranking
SELECT 
search_query,
engine_name,
total_freq,
search_engine_rank 
FROM (
	SELECT b.*, 
	COUNT(engine_name) OVER(PARTITION BY search_query) AS search_engine_count,
    DENSE_RANK() OVER(PARTITION BY search_query ORDER BY total_freq DESC) as search_engine_rank
	FROM (
		SELECT DISTINCT
		search_query,
		engine_name,
		total_freq FROM (
			SELECT 
			q.search_query,
			u.engine_name, 
			u.title, 
			-- u.snippet, 
			u.url,
			c.content_type, 
			c.freq,
			ROUND(SUM(freq) OVER(PARTITION BY search_query, engine_name),2) AS total_freq
			FROM WildHummingbirds.urls u 
			JOIN WildHummingbirds.content c ON c.url = u.url
			LEFT JOIN WildHummingbirds.search_query q ON u.search_id = q.search_id
			WHERE freq IS NOT NULL
		) a
	)b
)c 
WHERE search_engine_count >= 3
ORDER BY search_query, total_freq DESC
)
 SELECT 
 engine_name,
 -- ones as top_count,
 ROUND(ones / SUM(ones) OVER(),2)*100.0 as freq
 FROM
(
SELECT 
engine_name,
SUM(CASE WHEN search_engine_rank=1 THEN 1 ELSE NULL END) as ones
-- SUM(CASE WHEN search_engine_rank=2 THEN 1 ELSE NULL END) as twos,
-- SUM(CASE WHEN search_engine_rank=3 THEN 1 ELSE NULL END) as threes
FROM base
GROUP BY 1
ORDER BY 1 DESC
) a