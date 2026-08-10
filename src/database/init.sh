#!/bin/sh

# Créer la base et l'utilisateur

psql -U postgres << EOF
CREATE DATABASE ${DB_API_NAME};
CREATE USER ${DB_API_USER} WITH PASSWORD '${DB_API_PWD}';
ALTER DATABASE ${DB_API_NAME} OWNER TO ${DB_API_USER};
EOF
# GRANT ALL PRIVILEGES ON DATABASE ${DB_API_NAME} TO ${DB_API_USER};

# Donner les droits sur le schema public
psql -U postgres -d ${DB_API_NAME} << EOF
GRANT ALL ON SCHEMA public TO ${DB_API_USER};
EOF

echo "Base de données et table initialisées avec succès !"