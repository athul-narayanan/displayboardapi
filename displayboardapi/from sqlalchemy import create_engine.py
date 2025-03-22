from sqlalchemy import create_engine

# Connection string format: postgresql://user:password@host:port/database
engine = create_engine('postgresql://127.0.0.1:Algoma@2024@127.0.0.1:5432/displayboarddatabase')

# Connect and execute queries
with engine.connect() as connection:
    result = connection.execute("SELECT * FROM userrole")
    for row in result:
        print(row)
