import pandas as pd
import sqlite3

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 256)

def list_types():

    conn = sqlite3.connect('monsters.db')
    cur = conn.execute("""
select Type, count(*) as Cnt
from monsters 
group by Type
order by Type
""")
    df = pd.DataFrame(cur, columns=[x[0] for x in cur.description])
    print(df)


def list_dragons():

    conn = sqlite3.connect('monsters.db')
    cur = conn.execute("""
select Name, Size, Type, Alignment, CR, Source 
from monsters 
where Type = 'Dragon'
order by CR desc
""")
    df = pd.DataFrame(cur, columns=[x[0] for x in cur.description])
    print(df)


if __name__ == "__main__":
    list_types()    
    list_dragons()