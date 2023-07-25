Project Milestone 5: SQL Design (15 pts)

## Tables

### Tags Table
Name: tags
Description: A table that stores the list of user created tags, with an automatically generated unique id, a title that the user creates, and a description of the tag. 
Fields:
id: primary key, declared serial so auto increments each time a tag is added. 
title: title of the tag, user generated - limit of 150 characters - VARCHAR(150)
descr: description of the tag - TEXT
Tests:
Access Methods:

### Resources Table
Name: resources
Description: A table that stores the list of user created resources, with an automatically generated unique id, the date when the resource is created (this has a default value of the current system date of when the row is added), a title, a link, and a description.
Fields:
id: primary key for the table, automatically increments every time a resource is added
create_date: when the resource is initially created - automatically captures system date as the default value DATE DEFAULT (CURRENT_DATE)
title: a short title for the resource - limit of 150 characters - VARCHAR(150)
link:link to the resource that the user provides - TEXT
descr: description that the user provides - TEXT
Tests:
Access Methods:
add_to_resources

### Projects Table
Name: projects
Description: A table that stores the list of user created projects, with an automatically generated unique id, the title that the user adds, and a description of the project. 
Fields:
id: primary key for the table, automatically increments every time a project is added to the table
title: the user created title for the project -  limit of 150 characters VARCHAR(150)
descr: the description of the project created by the user - TEXT
Tests:
Access Methods:

### ResourcesTags Table
Name: resource_tags
Description: Given the many-to-many relationship between our resources and our tags objects, we need an additional table to store the relationship between them. Each row represents the distinct combination between each tag and each resource that are mapped together. The table leverages the primary keys of the tags and resources tables, and has a foreign key requirement to ensure that the relationship between a resource and a tag is referring to tags and resources that actually exist. 
Fields:
id: the primary key for teh table, automatically increments every time a new relationship between a tag and a resource is stored.
resource_id: the primary key of the resources table, the key that points to the resource being mapped to a tag. the table requires that this is a foreign key that references the resources table. 
tag_id: the primary key of the tags table, the key that points to the tag being mapped to a resource. The table requires that this is a foreign key that references the tags table. 
Tests:
Access Methods:

### ProjectsResources Table
Name: project_resources
Description: Given the many-to-many relationship between our projects and our resources, we need an additional table to store the relationship between them. Each row represents the distinct combination between each project and each resource that are mapped together. The table leverages the primary keys of each project and each resource that are mapped together, and has a foreign key requirement to ensure that the relationship between a project and a resource is referring to a project and a resource that actually exist. 
Fields:
id: primary key for the table, automatically increments every time a new relationship between a project and a resource is added
project_id: the primary key of the projects table, points to the project being mapped to a resource. the table requires that this is a foreign key that references the projects table. 
resource_id: the primary key of the resources table, points to the resource being mapped to a project. the table requires that this is a foreign key that references the resources table. 
Tests:
Access Methods:


### ProjectsTags Table
Name: project_tags
Description: Given the many-to-many relationship between our projects and our tags, we need an additional table to store the relationship between them. Each row represents the distinct combination between each project and each tag that are mapped together. The table leverages the primary keys of each project and each tag that are mapped together, and has a foreign key requirement to ensure that the relationship between a project and a tag is referring to a project and a tag that actually exist. 
Fields:
id: primary key for the table, automatically increments every time a new relationship between a project and a resource is added. 
project_id: primary key of the projects table, points to the project being mapped to a tag. the table requires that this is a foreign key that references the projects table. 
tag_id: primary key of the tags table, points to the tag being mapped to a project. the table requires that this is a foreign key that references the tags table. 
Tests:
Access Methods:




You will create a list of descriptions for tables and functions being created for the project.
You must add a file SQL_TESTING.md to your repository and provide the following for each table (at least 3 tables):

Table Name
Table Description
For each field of the table, provide name and short description.
List of tests for verifying each table
You must also provide the following (in SQL_TESTING.md)for each data access method (at least one access method for each table or query required to get the data to display):

Name
Description
Parameters
return values
List of tests for verifying each access method
Below is an example format that has been used for describing each test. Your tests might not have information for all those fields, but you should try to specify exactly how each of the pages behaves.

           
           Use case name : 
                Verify login with valid user name and password
            Description:
                Test the Google login page
            Pre-conditions (what needs to be true about the system before the test can be applied):
                User has valid user name and password
            Test steps:
                1. Navigate to login page
                2. Provide valid user name
                3. Provide valid password
                4. Click login button
            Expected result:
                User should be able to login
            Actual result (when you are testing this, how can you tell it worked):
                User is navigated to dashboard with successful login
            Status (Pass/Fail, when this test was performed)
                Pass
            Notes:
                N/A
            Post-conditions (what must be true about the system when the test has completed successfully):
                User is validated with database and successfully signed into their account.
                The account session details are logged in database. 
This is a Design Document for Developers
This should be a document that you would hand to developers (not a homework assignment where you list the question and then the answer). It should be easy to tell what your design for the database is going to encompass.

Please make sure it answers the following questions:

What are the tables you are going to have in the database?
What are the fields of each table?
What are the constraints for those table fields?
What are the relationships between tables?

What are the functions that will be created to access the database?

What are the tests to make sure those access routines work?

Which pages will need to access the database information?

What are the tests to make sure the pages access the correct data in the database?
