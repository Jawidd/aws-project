## DB quick steps

- start shell: `bin/db/scale-db-shell-up` (or `bin/db/run-db-shell` to open psql and auto tear down)
- get into the task: `bin/db/connect-db-shell` → you land at a shell prompt
- open psql: `psql "$CONNECTION_URL"` (this drops you into the `cruddur` DB)
- load schema: `\i /opt/db-scripts/schema.sql` (runs all table/DDL commands)
- load seed: `\i /opt/db-scripts/seed.sql` (inserts sample data)
- also create likes Table/schema `\i /opt/db-scripts/migrations/003_create_likes_table.sql`
- check tables: `\dt` (lists tables)
- check a row: `SELECT uuid, handle FROM public.users;`
- exit psql: `\q`
- stop shell task: `bin/db/scale-db-shell-down` (not needed if you used run-db-shell)
