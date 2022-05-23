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

-- 2.2 search engine ranking
SELECT 
search_query,
engine_name,
total_freq 
FROM (
	SELECT b.*, 
	COUNT(engine_name) OVER(PARTITION BY search_query) AS search_engine_count
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
ORDER BY search_query, total_freq DESC;