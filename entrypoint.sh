#! /bin/bash

mongoimport --host mongodb --authenticationDatabase admin -u root -p root --db tpb --collection articles --type json --file app/articles.json --jsonArray -vvvvv