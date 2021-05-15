drop table if exists 'stock';
drop table if exists 'dayPrice';
drop table if exists 'holds';
drop table if exists 'testholds';
drop table if exists 'watchlist';
drop table if exists 'contain';
create table 'stock' (
  'id' integer primary key autoincrement,
  'ticker' text,
  'name' char(50),
  'industry' char(50)
);

INSERT INTO 'stock' ('id', 'ticker', 'name', 'industry') VALUES
(1, 3034, '聯詠','IC設計'),
(2, 2317, '鴻海精密','電子製造'),
(3, 3481, '群創光電','面板'),
(4, 3576, '聯合再生能源','能源'),
(5, 3711, '日月光控股','封測'),
(6, 2881, '富邦金','金融');

create table 'dayPrice' (
  'id' integer primary key autoincrement,
  'open' float,
  'high' float,
  'low' float,
  'close' float,
  'sid' integer,
  foreign key('sid') references stock('id')
);

create table 'holds' (
  'id' integer primary key autoincrement,
  'bprice' float,
  'sprice' float,
  'pprice' float,
  'sell' float,
  'bdate' Date,
  'sdate' Date,
  'sid' integer,
  'unit' integer,
  foreign key('sid') references stock('id')
);
INSERT INTO 'holds' ('id', 'bprice', 'sprice', 'pprice','sell','bdate','sdate','sid','unit') VALUES
(1, 12, 11,14, NULL, '2021-03-25',NULL,1,1),
(2, 15, 10,33, NULL, '2021-03-25',NULL,2,2);


create table 'testholds' (
  'id' integer primary key autoincrement,
  'bprice' float,
  'sprice' float,
  'pprice' float,
  'sell' float,
  'bdate' Date,
  'sdate' Date,
  'sid' integer,
  'unit' integer,
  foreign key('sid') references stock('id')
);

create table 'watchlist' (
  'id' integer primary key autoincrement,
  'name' char(50)
);
INSERT INTO 'watchlist' ('id','name') VALUES
(1, '電子'),
(2, '金融');

create table 'contain' (
  'wid' integer not null,
  'sid' integer not null,
  foreign key('wid') references watchlist('id'),
  foreign key('sid') references stock('id')
);
INSERT INTO 'contain' ('wid','sid') VALUES
(1, 1),
(1, 2),
(2, 6);