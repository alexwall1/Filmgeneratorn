create table movie (
	id integer primary key autoincrement,
	title char(150) not null,
	plot text not null,
	genre char(50) not null,
	rating integer default(1)
);
