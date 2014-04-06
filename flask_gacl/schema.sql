drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  text text not null,
  author text not null,
  tags text not null,
  pending text not null,
  private integer not null 
);

drop table if exists requests;
create table requests (
  id integer primary key autoincrement,
  tag text not null,
  author text not null,
  status text not null
);
