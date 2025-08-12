# Overview, setup, execution steps

## Project Setup

1. Ensure Docker and Docker Compose are installed.
2. Run `./scripts/load_data.sh` to spin up MySQL and PostgreSQL containers with schemas loaded.
3. Run the ETL scripts in `etl/` to migrate data between databases