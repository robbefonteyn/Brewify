USE Brewify;

Select * from styles;

select * from styles;
Update styles set style_name = "Non-Alcoholic Beer" where style_id = 479; 

select * from beers;
select * from styles;
select brewery_id, brewery_name from breweries;
select max(rating_id) from ratings;

SELECT beers.beer_id, beers.beer_name, breweries.brewery_name, ratings.rating, beers.abv, beers.ibu
FROM beers
INNER JOIN breweries ON beers.brewery_id = breweries.brewery_id
INNER JOIN styles ON beers.style_id = styles.style_id
LEFT JOIN ratings ON beers.rating_id = ratings.rating_id
WHERE styles.style_name = 'Low Alcoholic Beer';

