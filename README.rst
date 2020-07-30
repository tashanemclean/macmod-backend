e-commerce platform backend, can serve as a base for projects which consumes mongodb documents and advanced filters.

Initial Setup Backend
=====================

1. Install miniconda latest version(This will install conda, a package and environment manager)
    * https://docs.conda.io/en/latest/miniconda.html

2. Update conda just in case,
    * conda update conda

3. Create the environment using the file macmod-environment.yml file using the following command,
    * conda env create -f macmod-environment.yml

4. Activate the environment,
    * conda activate "env name"

Installing new Packages
=======================

1. Install the new package in your environment using
    * conda install "packagename"
    * pip install "packagename"

2. Add the package name and the version in the macmod-environment.yml file
    (put the package under respective package manager)

3. Push the updated environment file to git.


Updating packages
=================

1. git pull the environment file.

2. update your current environment using
    * conda env update -f macmod-environment.yml

    This will automatically check the differences in your current file and install the new ones.


Database Setup
==================

1. install mongodb from the following source:
    * sudo apt update
    * sudo apt install mongodb-org

2. Check the installation:
    * mongod --version

3. Connect to the db with the command:
    * mongo mongodb://localhost:27017

4. Use the admin database:
    * use admin

5. create a new user for use in the backend with the following command:
    * db.createUser(
        {
            user:"useradmin", 
            pwd:"<password>", 
            roles: [{
                    role:"userAdminAnyDatabase", 
                    db:"admin"
            }]
        }
    )

6. Enable database security in the file mongod.conf:
    * security: 
        authorization: "enabled"

7. Create database replace the [] values with the names for database and collection:
    * use [new-database-name]
    * and insert a value in a custom collection: db.[collection-name].insert({ Name : "TecAdmin.net" })

8. List the existing databases:
    * show dbs;

9. for finish set the database environment variables with this structure:
    export DATABASE_HOST="localhost"
    export DATABASE_PORT=27017
    export DATABASE_NAME=[database-name]
    export DATABASE_USERNAME=[database-username]
    export DATABASE_PASSWORD=[database-password]


10. command to import json array to database from command line: 
    mongoimport --host --ssl --username <username> --password <password> --authentication <clustername-uri> admin --db <DATABASE> --collection <COLLECTION> --jsonArray <PATH TO FILE>


NOTES: 
applications pdfs are stored in fs.files and contain 'brand' metadata key:
    example: { _id: asdf, filename: "somefile", metadata: {filename: "somefile", brand: "ace"}}

all other content is stored in fs.files and will contain 'content' metadata key:
    example1: { _id: asdf, filename: "someotherfile", metadata: {filename: "someotherfile", content: "Whitepaper"}}, 
    example2: { _id: asdf, filename: "randomfile", metadata: {filename: "randomfile", content: "Lab notes"}}
