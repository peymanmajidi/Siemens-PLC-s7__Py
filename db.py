import pyodbc 

print("Connecting ...")


cnxn = pyodbc.connect(driver="{FreeTDS}",
                      server="192.168.2.41\EHSANSQL",
                      database="CrossBeltDB", 
                      user="sa",password="server@1314")
cnxn.timeout=4



print("Connectted")

cursor = cnxn.cursor()
cursor.execute("""INSERT INTO [dbo].[UsersTBL]
		 ([name]
           ,[family]
           ,[age])

     VALUES
           ('ALI','BANDARI22',20)
""")
cnxn.commit();


cursor.execute("SELECT * FROM UsersTBL")

for row in cursor:
    print('row = %r' % (row,))