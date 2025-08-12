#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}==> Stopping and removing old containers & volumes...${NC}"
docker-compose down -v

echo -e "${GREEN}==> Starting MySQL and PostgreSQL containers...${NC}"
docker-compose up -d

# Function to wait for MySQL
wait_for_mysql() {
    echo -e "${GREEN}==> Waiting for MySQL to be ready...${NC}"
    until docker exec legacy_mysql mysqladmin ping -uroot -prootpass --silent &> /dev/null; do
        sleep 2
    done
    echo -e "${GREEN}==> MySQL is ready!${NC}"

}

# Function to wait for PostgreSQL
wait_for_postgres() {
    echo -e "${GREEN}==> Waiting for PostgreSQL to be ready...${NC}"
    until docker exec modern_postgres pg_isready -U postgres &> /dev/null ; do
        sleep 2
    done
    echo -e "${GREEN}PostgreSQL is ready!${NC}"
}

wait_for_mysql
wait_for_postgres

echo -e "${GREEN}==> Verifying schema load...${NC}"
docker exec legacy_mysql mysql -uroot -prootpass -e "SHOW TABLES IN legacy_financials;"
docker exec modern_postgres psql -U postgres -d modern_financials -c "\dt"

echo -e "${GREEN}==> Data load complete! Ready for ETL.${NC}"