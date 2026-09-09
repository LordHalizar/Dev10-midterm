drop schema if exists population_age cascade;
create schema population_age;
set search_path to population_age;

create table country (
	country_id serial primary key,
    country_code varchar(128) not null
);

create table population_range (
	pop_range_id serial primary key,
    pop_range_0_4 int not null,
    pop_range_5_9 int not null,
    pop_range_10_14 int not null,
    pop_range_15_19 int not null,
    pop_range_20_24 int not null,
    pop_range_25_29 int not null,
    pop_range_30_34 int not null,
    pop_range_35_39 int not null,
    pop_range_40_44 int not null,
    pop_range_45_49 int not null,
    pop_range_50_54 int not null,
    pop_range_55_59 int not null,
    pop_range_60_64 int not null,
    pop_range_65_69 int not null,
    pop_range_70_74 int not null,
    pop_range_75_79 int not null,
    pop_range_80_84 int not null,
    pop_range_85_89 int not null,
    pop_range_90_94 int not null,
    pop_range_95_99 int not null,
    pop_range_100 int not null
);

create table population_rate (
	pop_rate_id serial primary key,
	life_expectancy numeric(5, 3) not null,
	infant_mortality numeric(5, 3) not null,
	natural_rate numeric(5, 3) not null
);

create table population_data (
	pop_data_id serial primary key,
	year int not null,
	median_age numeric(5,3) not null,
	country_id int not null,
	pop_range_id int not null,
	pop_rate_id int not null,
	foreign key (country_id)
		references country(country_id),
	foreign key (pop_range_id)
		references population_range(pop_range_id),
	foreign key (pop_rate_id)
		references population_rate(pop_rate_id),
	constraint up_country_year
		unique (country_id, year),
	constraint uq_range_rate
		unique (pop_range_id, pop_rate_id)		
);