import pandas as pd
import re

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 256)

def example_1(df: pd.DataFrame):
    print("Dragons:")
    print(df[ df.Name.str.contains("Dragon")])

def example_2(df: pd.DataFrame):
    print("Void Dragons:")
    print(df[ df.Name.str.contains("Dragon") & df.Name.str.contains("Void") ])

def example_3(df: pd.DataFrame):
    print("Void Dragons:")
    print(df[ df.Name.str.contains(re.compile("Void.*Dragon")) ])

def main():
    df = pd.read_csv("Monsters.csv", sep=",")
    #print(df.columns)

    df = df[["Name", "Size", "Type", "Alignment", "CR", "Source"]]
    #print(df)
    
    #example_1(df)
    #example_2(df)
    example_3(df)
    pass

if __name__ == "__main__":
    main()