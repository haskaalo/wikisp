.PHONY: createdb
createdb:
    docker run -p 3306:3306 -name test-db-mysql -e MYSQL_ROOT_PASSWORD=totalrandompassword -d mysql