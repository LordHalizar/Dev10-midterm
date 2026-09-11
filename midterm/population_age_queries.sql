set search_path to population_age;

select * from country order by country_name;

select * from population_range;

select * from population_data;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'US'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'MX'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'CA'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'FR'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'CN'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'JP'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
where c.country_code = 'IN'
order by pd.year asc;

select
	c.country_name,
	pr.pop_range_100,
	pd.*
from country c
join population_data pd on pd.country_id = c.country_id
join population_range pr on pd.pop_range_id = pr.pop_range_id
order by pr.pop_range_0_4 asc;