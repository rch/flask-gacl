drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  author text not null,
  tags text not null,
  text text not null,
  private integer not null 
);
