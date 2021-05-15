import sqlite3

script = {
    'allstock':"SELECT * FROM stock",
    'allhold':"SELECT s.ticker as ticker, s.name as name, s.industry as industry, h.unit as unit, h.bprice FROM holds h, stock s WHERE h.sid = s.id",
    'allwatchlist':"SELECT w.id as wid, w.name as wname,s.ticker as ticker, s.name as name, s.industry as industry FROM watchlist w, contain c, stock s WHERE s.id = c.sid AND c.wid = w.id"
}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_sqlite(db, action):
    conn = sqlite3.connect(db)

    #Display all blogs from the 'blogs' table
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(script[action])
    stocks = c.fetchall()
    return stocks