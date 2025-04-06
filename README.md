# NetworksProject
CS 381 Semester Project

# Server Setup
To connect to the PostgreSQL database used by this project, use the following credentials:

- **Host:** localhost
- **Port:** 5432
- **Database:** stockdb
- **Username:** admin
- **Password:** adminpass

# DBeaver Setup

1. Open DBeaver and select **New Database Connection**.
2. Choose **PostgreSQL** as the database type.
3. Enter the connection details:
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** stockdb
   - **Username:** admin
   - **Password:** adminpass
4. Test the connection and click **Finish**.

### Command Line (psql):
You can also connect using the `psql` command line tool:
```bash
psql -h localhost -U admin -d stockdb -p 5432