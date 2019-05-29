import pyodbc 

print("Connecting ...")


cnxn = pyodbc.connect(driver="{ODBC Driver 17 for SQL Server}",
                      server=".",
                      database="MyDB", 
                      user="sa",password="server@1314")
cnxn.timeout=4



print("Connectted")

cursor = cnxn.cursor()
# cursor.execute("""INSERT INTO [dbo].[UsersTBL]
# 		 ([name]
#            ,[family]
#            ,[age])

#      VALUES
#            ('ALI','BANDARI',20)
# """)
# cnxn.commit();


cursor.execute("SELECT * FROM TestTBL")

for row in cursor:
    print('row = %r' % (row,))