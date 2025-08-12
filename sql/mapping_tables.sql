/*
 To make the ETL realistic, we want lookup tables for:
 - Old accounts codes --> new account codes
 - Old customer/vendor IDs --> new party IDs
 These can live in PostgreSQL or in a CSV/YAML file that your ETL script reads.
/*