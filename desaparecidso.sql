CREATE DATABASE desaparecidosgt;

USE desaparecidosgt;

CREATE TABLE KEYWORDS(words VARCHAR(100), wtype VARCHAR(20));
insert into KEYWORDS values("#AlertaIsabelClaudina", "key"), ("#AlertaAlbaKeneth", "key"), ("#AlbaKeneth", "key"), ("#desaparecidosgt", "key"), ("#botaparecegt", "key");
insert into KEYWORDS values("localizada", "jump"), ("localizado", "jump"), ("localización", "jump");

insert into KEYWORDS values ("love", "jump"),("kiss", "jump"),("ass", "jump"),("night", "jump"),("talented", "jump"),("mouth", "jump"),("calendar", "jump"),("sex", "jump"),("crazy", "jump"),("body", "jump"),("taste", "jump"),("masturbate", "jump"),("smell", "jump"),("fuck", "jump"),("doll", "jump"),("sexy", "jump"),("want", "jump"),("surprise", "jump");


CREATE TABLE ReTweets(
    id varchar(500),
    created_at date
);

 
update KEYWORDS set wtype = "located"
where words = "localizada"
OR words = "localizado"
OR words = "localización";

CREATE TABLE LocatedTweets(id VARCHAR(500), tweet_text VARCHAR(500) , created_at date);


update KEYWORDS set wtype = "albakeneth"
where words = "#AlbaKeneth" OR words = "#AlertaAlbaKeneth";

update KEYWORDS set wtype = "isabelclaudina"
where words = "#AlertaIsabelClaudina";

