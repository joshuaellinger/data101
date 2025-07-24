import pandas as pd
import sqlite3

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 256)

def list_types():

    conn = sqlite3.connect('monsters.db')
    #conn.execute("update monsters set cr='0.5' where cr='1/2'")
    #conn.execute("update monsters set cr='0.125' where cr='1/8'")
    # conn.execute("update monsters set cr='0.25' where cr='1/4'")
    #conn.commit()
    cur = conn.execute("""
select Type,cr, count(*) as Cnt
from monsters 
where type='Plant'
group by Type,cr
order by Type,cast(cr as number)
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
    #list_dragons()