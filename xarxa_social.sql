
CREATE TABLE if not exists usuaris(
	email varchar(20),
	nom varchar(20),
	cognom varchar(20),
	poblacio varchar(20),
	dataNaixament date,
	pwd varchar(20)
);


create DOMAIN estatsAmistat as varchar(10)
constraint estatsValids
check (value in("Aprovada","Rebutjada","Pendent")
);

create table if not exists amistats (
email1 varchar(20),
email2 varchar(20) ,
estat estatsAmistat,
primary key(email1,email2),
foreign key(email1) references usuaris,
foreign key(email2) references usuaris);


