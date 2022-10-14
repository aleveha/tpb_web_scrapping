#! /bin/bash

mongoimport --host mongodb --authenticationDatabase admin -u root -p root --db tpb --collection links --type json --file app/links.json --jsonArray -vvvvv
mongoimport --host mongodb --authenticationDatabase admin -u root -p root --db tpb --collection articles --type json --file app/articles.json --jsonArray -vvvvv