-- Database: "hazard-mobility"

-- DROP DATABASE "hazard-mobility";

CREATE DATABASE "hazard-mobility"
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;

drop table if exists distances_sjc_sp;

CREATE TABLE public.distances_sjc_sp
(
  id serial primary key,
  idx_origin character varying(1000),
  idx_destination character varying(1000),
  origin character varying(1000),
  destination character varying(1000),
  distance_meters character varying(1000),
  mode character varying(1000),
  path text,
  duration character varying(1000),
  intermediate_paths_ok character varying(1000)
);

delete from distances_sjc_sp;



DROP TABLE if exists intermiate_distances_sjc_sp;

CREATE TABLE public.intermiate_distances_sjc_sp
(
  id serial primary key,
  id_distances_sjc_sp character varying(1000),
  duration_seconds character varying(1000),
  start_point character varying(1000),
  end_point character varying(1000),
  mode character varying(1000),
  path text,
  distance_meters character varying(1000)
);

delete from intermiate_distances_sjc_sp;





CREATE TABLE public.excel
(
  id serial primary key,
  zonatrafego character varying(100),
  pop_ibge character varying(100),
  dom_ibge character varying(100),
  macrozona character varying(100),
  nome_zt character varying(100),
  pop_od character varying(100),
  dom_od character varying(100),
  perc_pop character varying(100),
  perc_dom character varying(100),
  area_km character varying(100),
  x_centroid character varying(100),
  y_centroid character varying(100),
  pop_area character varying(100)
);