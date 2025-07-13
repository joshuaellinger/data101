
# Setup for example:

# 1. cleanup the header in the monsters files
# 2. import into a Sql Lite DB

def cleanup():

    print("generate Monsters.csv")
# The rows 2-4 contains header and filter information but it's split on to mutiple lines.
# So grab the parts we need and make a clean header.
#  
#0	1	2	3	4	5	6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	21	22	23	24	25	26	27	28	29	30	31	32	33	34	35	36	37	38	39	40	41	42	43	44	45	46	47	48	49	50	51	52	53	54	55	56	57	58	59	60	61	62	63	64	65	66
#					CR		Spellcaster	Legendary	Lair	Unique	Familiar	Template	Arctic	Coastal	Desert	Forest	Grassland	Hill	Mountain	Swamp	Underdark	Underwater	Urban	Other Plane																																										
#Name	Size	Type	Tag	Alignment	low | high		FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	Source	Page	Other Printings		Name	Size	Type	Tag	Alignment	CR	[PH]	Spellcaster	Legendary	Lair	Unique	Familiar	Template	Arctic	Coastal	Desert	Forest	Grassland	Hill	Mountain	Swamp	Underdark	Underwater	Urban	Other Plane	Source	Page	Reprint	Size	Type	Alignment	CR	Source	Owned	Core	Official	Charity	Third Party
#	Any	Any		Any	-	-	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	FALSE	All																																						Core	Official	Charity	Third Party

    with open("5e Complete Index v3.6 - Monsters.csv", "r") as f:
        with open("Monsters.csv", "w") as f_out:

            row_num = 0
            header_rows = []
            while (True):
                s = f.readline()
                if s == "": break
                row_num += 1

                if row_num == 1:
                    # first line contains a split files because of a comma -> ignore
                    continue
                elif row_num == 2:
                    # second line contains the CR column and the filter flag names

                    header_rows.append(s[:-1].split(","))
                    # get the filter flag names
                    idx = s.index("CR")                
                    s = s[idx:]
                    idx = s.rindex("Plane")
                    s = s[:idx+5]

                    s_flags = s
                    continue                
                elif row_num == 3:
                    # third line contains some column names, then the low|high label associated with 
                    # the CR column, then TRUE/FALSE for the filters, the rest of the columns
                    header_rows.append(s[:-1].split(","))
                    idx = s.index(",low | high,")
                    s_name = s[:idx]
                    idx = s.index("Source,")
                    s_source = s[idx:-1]

                    # combine the first and last part of the rows with the filter names
                    # to get the real column names
                    column_names = ",".join([s_name, s_flags, s_source])
                    s = column_names

                    n_cols = len(column_names.split(","))
                    print(f"   found {n_cols} columns")

                    header_rows.append(column_names[:-1].split(","))
                    for i in range(n_cols):
                        a = header_rows[0][i] if i < len(header_rows[0]) else ""
                        b = header_rows[1][i] if i < len(header_rows[1]) else ""
                        c = header_rows[2][i]
                        #print(f"  {i+1:03d}: <{a}> , <{b}> => <{c}>")

                    f_out.write(column_names)
                    f_out.write("\n")
                    continue                
                elif row_num == 4:
                    # just a bunch of flags -> ignore
                    continue

                f_out.write(s)

    print("generate Monsters.csv ... done")

def init_db():
    import sqlalchemy
    import pandas as pd

    print("load to monsters.db")
    engine = sqlalchemy.create_engine('sqlite:///monsters.db', echo=False)
    df = pd.read_csv("Monsters.csv", sep=",")
    df.to_sql('monsters', con=engine, if_exists='replace')
    print("load to monsters.db ... done")


if __name__ == "__main__":
    cleanup()
    init_db()