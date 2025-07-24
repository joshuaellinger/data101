import pandas as pd
import sqlite3

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 256)

def list_types():

    conn = sqlite3.connect('monsters.db')
    #conn.execute("update monsters set CR = '0.5' where CR = '1/2'")
    #conn.execute("update monsters set CR = '0.25' where CR = '1/4'")
    #conn.execute("update monsters set CR = '0.125' where CR = '1/8'")
    #conn.commit()
    cur = conn.execute("""
select Type, CR, count(*) as Cnt
from monsters 
where type in ('Monstrosity','Plant')                   
group by Type, CR
order by Type, cast(CR as number)                      

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