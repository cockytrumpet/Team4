# Project Milestone 5: SQL Design (15 pts)
This is the SQL Design document for Team 4. 

# Tables

## Tags Table
### Name:
tags
### Description:
A table that stores the list of user created tags, with an automatically generated unique id, a title that the user creates, and a description of the tag. 
### Fields:
__id:__ primary key, declared serial so auto increments each time a tag is added. <br>
__title:__ title of the tag, user generated - limit of 150 characters - VARCHAR(150) <br>
__descr:__ description of the tag - TEXT <br>

### Access Methods:
#### 1. add to the tags table (add_to_tags)
__Name:__ add_to_tags 
<br>
__Description:__ This is a method that allows a user to add a tag to the tags table
<br>
__Parameters:__ The tag title and description that the user wants to use for the new tag. The function also requires a database connection. 
<br>
__Return Values:__ There is no return value, just side effects - the table is updated with the new tag.
<br>
__Test:__ see test 1 in the tests section.
<br>
#### 2. retrieve all tags
__Name:__ get_tags
<br>
__Description:__ This is a method that retrieves all of the tags from the tags table to render on the front end
<br>
__Parameters:__ The only parameter is a database connection.
<br>
__Return Values:__ The return value is an array of tags and their associated attributes from the tags table.
<br>
__Test:__ see test 2 in the tests section.
<br>

#### 3. search for resources by tag (get_tagged_resources)
__Name:__ get_tagged_resources
<br>
__Description:__ This is a method that retrieves resources that are tagged with a specific tag.
<br>
__Parameters:__ The method requires a database connection and a tag_id that the user wants to find resources for.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
__Test:__ see test 3 in the tests section.
<br>

#### 4. search for resources by tag(s) or resource title
__Name:__ search_resources
<br>
__Description:__ This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
__Test:__ see test 4 in the tests section.
<br>

### Tests:
#### 1. Test adding to the tags table
__Description:__ <br>
When a user creates a new tag, it will be stored in the tags table.
<br>
__Preconditions:__ <br>
The database has been created and the user can access the tags form.
<br>
__Test steps:__ <br>
1. Access the create tags page
2. Fill out the form with the tag title and description
3. Click submit

__Expected result:__ <br>
The newly created tag should be visible on the list of available tags
<br>
__Actual result:__ <br>
There is a new row in the tags table with the created tag id, tag title and tag description.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
The only primary key is the tag_id, so it is possible to create tags with the same title
<br>
__Post-conditions:__ <br>
The tag is available to add either to a new resource or an existing resource.
<br>

#### 2. Test retrieving all tags
__Description:__ <br>
When a user wants to view all of the available tags, we need to return all of them from the table.
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table.
<br>
__Test steps:__ <br>
1. Access the tags page
2. Check that all of the tags are visible

__Expected result:__ <br>
The list of tags are visible to the user
<br>
__Actual result:__ <br>
A query is executed against the tags table and all of the tags are returned from the tags table to the front-end.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
The query returns all fields from the tags table, even though the tag id is not visible to the user.
<br>
__Post-conditions:__ <br>
The list of tags is visible to the user on the tags page and on the add to resources page.
<br>

#### 3. Search for resources by tag
__Description:__ <br>
When a user wants to view all of the resources related to a specific tag, we need to access the tags table, resources table, and resources tags table. This is because we need to retrieve the resources by tag title. 
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table. It is also required that the tags resources table and the resources table has been created. It will return an empty list if there are no resources that match the tag, so it is not required to have a mapping from the tag to the resource. 
<br>
__Test steps:__ <br>
1. Access the resources page
2. Click the tags filter to filter the resources by a tag.

__Expected result:__ <br>
The list of resources are visible to the user that match the tag that was selected.
<br>
__Actual result:__ <br>
A query is executed to retrieve resources that are tagged with the tag title passed in from the front-end. The query joins the resources and tags table using the resource_tags table and returns the matching resources and tag title to the front-end to display to the user.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This is related to the tags table, the resources table, and the resource_tag table. 
<br>
__Post-conditions:__ <br>
The list of resources that match the tag title selected by the user are visible.
<br>

#### 4. Search for resources by tag(s) or resource title
__Description:__ <br>
When a user wants to view all of the resources related to a user search which could contain either a resource title or one or more tags associated with a resource. This access method touches three tables - we need to access the tags table, resources table, and resources tags table. This is because we need to retrieve the resources that match either one or more tags or one or more resource titles related to a resource.
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table. It is also required that the tags resources table and the resources table has been created. Is is also helpful if there is at least one resource and one tag that have been mapped in the resource_tags table and added to their respective tables. It will return an empty list if there are no resources that match the search.
<br>
__Test steps:__ <br>
1. Access the search page
2. Enter a search that contains either one or more tags or one or more resource titles into the search bar
3. Hit submit
4. Read through the returned results and make sure they match the search criteria

__Expected result:__ <br>
The list of resources that match either the tag title(s) or resource title(s) submitted in the search are visible to the user.
<br>
__Actual result:__ <br>
A query is executed to retrieve resources that are tagged with the tag title(s) or resource title(s) that are passed in to the search bar from the front-end. The query joins the resources and tags table using the resource_tags table and returns the matching resources to the front-end to display to the user.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This is related to the tags table, the resources table, and the resource_tag table. 
<br>
__Post-conditions:__ <br>
The list of resources that match the tag title(s) or the resource title(s) entered into the search bar by the user are visible.
<br>

## Resources Table
### Name: 
resources
### Description:
A table that stores the list of user created resources, with an automatically generated unique id, the date when the resource is created (this has a default value of the current system date of when the row is added), a title, a link, and a description.
### Fields:
__id:__ primary key for the table, automatically increments every time a resource is added <br>
__create_date:__ when the resource is initially created - automatically captures system date as the default value DATE DEFAULT (CURRENT_DATE) <br>
__title:__ a short title for the resource - limit of 150 characters - VARCHAR(150) <br>
__link:__ link to the resource that the user provides - TEXT <br>
__descr:__ description that the user provides - TEXT <br>

### Access Methods:
#### 1. Add a resource to the resources table
__Name:__ add_to_resources
<br>
__Description:__ This is a method that allows a user to create and store a new resource.
<br>
__Parameters:__ The method requires a title, link, description that the user wants to use to create a new resource, as well as a database connection.
<br>
__Return Values:__ The return value is the resource id of the newly created resource that's been added to the resources table. 
<br>
__Test:__ see test 1 in the tests section.
<br>

#### 2. Retrieve resource from the resources table
__Name:__ get_resource_by_id
<br>
__Description:__ This is a method that allows a user to retrieve a resource from the resources table by a specific resource id.
<br>
__Parameters:__ The method requires a resource id and a database connection.
<br>
__Return Values:__ The return value is the resource and it's associated attributes from the resources table that matches the resource id passed to the function.
<br>
__Test:__ see test 2 in the tests section.
<br>

#### 3. Retrieve resource and related tags
__Name:__ get_resource
<br>
__Description:__ This is a method that allows a user to retrieve a resource from the resources table by a specific resource id and also return the related tag information associated with the resource retrieved.
<br>
__Parameters:__ The method requires a resource id and a database connection.
<br>
__Return Values:__ The return value is the resource and it's associated attributes from the resources table, as well as the related tag titles from the tags table. 
<br>
__Test:__ see test 3 in the tests section.
<br>

#### 4. Retrieve all resources from the resources table (get_resources)
__Name:__ get_resources
<br>
__Description:__ This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
__Test:__ see test 4 in the tests section.
<br>

#### 5. Update a resource with new details
__Name:__ update_resource
<br>
__Description:__ This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
__Test:__ see test 4 in the tests section.
<br>
<br>
Delete resource from the resource table (delete_resource_by_id)
<br>
search for resources by tag or resource (search_resources)
<br>
get resources by tag id 
<br>

### Tests:
__Test adding a new resources__
<br>
__Description:__
test adding a new resource, given input from the user
<br>
__Preconditions:__
the database has been created
<br>
__Test steps:__
1. Navigate to the add resource page
2. Fill out the form and add a title, a description, and a link.
3. Add the tags to the resource from the available tags if needed
4. Click submit
__Expected result:__
A new resource should be accessible from the resources page
<br>
__Actual result:__
A new resource is created in the resources table, and a new row in the resources tags table if tag(s) are added to the resource
<br>
__Status:__
Pass (conducted July 26th 2023)
<br>
__Notes:__
This test is related to the resourcetags table if there are tags assigned to the resource.
<br>
__Post-conditions:__
The user has successfully created a new resource, and it can be accessed via the resources page.
<br>


#### Search for resources by tag
__Description:__ <br>
When a user wants to view all of the resources related to a specific tag, we need to access the tags table, resources table, and resources tags table. This is because we need to retrieve the resources by tag title. 
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table. It is also required that the tags resources table and the resources table has been created. It will return an empty list if there are no resources that match the tag, so it is not required to have a mapping from the tag to the resource. 
<br>
__Test steps:__ <br>
1. Access the resources page
2. Click the tags filter to filter the resources by a tag.

__Expected result:__ <br>
The list of resources are visible to the user that match the tag that was selected.
<br>
__Actual result:__ <br>
A query is executed to retrieve resources that are tagged with the tag title passed in from the front-end. The query joins the resources and tags table using the resource_tags table and returns the matching resources and tag title to the front-end to display to the user.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This is related to the tags table, the resources table, and the resource_tag table. 
<br>
__Post-conditions:__ <br>
The list of resources that match the tag title selected by the user are visible.
<br>

#### Search for resources by tag(s) or resource title
__Description:__ <br>
When a user wants to view all of the resources related to a user search which could contain either a resource title or one or more tags associated with a resource. This access method touches three tables - we need to access the tags table, resources table, and resources tags table. This is because we need to retrieve the resources that match either one or more tags or one or more resource titles related to a resource.
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table. It is also required that the tags resources table and the resources table has been created. Is is also helpful if there is at least one resource and one tag that have been mapped in the resource_tags table and added to their respective tables. It will return an empty list if there are no resources that match the search.
<br>
__Test steps:__ <br>
1. Access the search page
2. Enter a search that contains either one or more tags or one or more resource titles into the search bar
3. Hit submit
4. Read through the returned results and make sure they match the search criteria

__Expected result:__ <br>
The list of resources that match either the tag title(s) or resource title(s) submitted in the search are visible to the user.
<br>
__Actual result:__ <br>
A query is executed to retrieve resources that are tagged with the tag title(s) or resource title(s) that are passed in to the search bar from the front-end. The query joins the resources and tags table using the resource_tags table and returns the matching resources to the front-end to display to the user.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This is related to the tags table, the resources table, and the resource_tag table. 
<br>
__Post-conditions:__ <br>
The list of resources that match the tag title(s) or the resource title(s) entered into the search bar by the user are visible.
<br>


__Test retrieving resources from the resources table__
<br>
__Description:__
<br>
__Preconditions:__
<br>
__Test steps:__
<br>
__Expected result:__
<br>
__Actual result:__
<br>
__Status:__
<br>
__Notes:__
<br>
__Post-conditions:__
<br>

## Projects Table
### Name: 
projects
### Description:
A table that stores the list of user created projects, with an automatically generated unique id, the title that the user adds, and a description of the project. 
### Fields:
__id:__ primary key for the table, automatically increments every time a project is added to the table <br>
__title:__ the user created title for the project -  limit of 150 characters VARCHAR(150) <br>
__descr:__ the description of the project created by the user - TEXT <br>
### Access Methods:
Get all projects (get_projects)
<br>
Add a new project (add_to_projects)
<br>

### Tests:
__Test 1__
<br>
__Description:__ 
<br>
__Preconditions:__ 
<br>
__Test steps:__
<br>
__Expected result:__
<br>
__Actual result:__
<br>
__Status:__
<br>
__Notes:__
<br>
__Post-conditions:__
<br>

## ResourcesTags Table
### Name:
resource_tags
### Description: 
Given the many-to-many relationship between our resources and our tags objects, we need an additional table to store the relationship between them. Each row represents the distinct combination between each tag and each resource that are mapped together. The table leverages the primary keys of the tags and resources tables, and has a foreign key requirement to ensure that the relationship between a resource and a tag is referring to tags and resources that actually exist. 
### Fields:
__id:__ the primary key for teh table, automatically increments every time a new relationship between a tag and a resource is stored. <br>
__resource_id:__ the primary key of the resources table, the key that points to the resource being mapped to a tag. the table requires that this is a foreign key that references the resources table. <br>
__tag_id:__ the primary key of the tags table, the key that points to the tag being mapped to a resource. The table requires that this is a foreign key that references the tags table. <br>


### Access Methods:
Get resource by id  with tag information (get_resource)
Delete resource and related tags (delete_resource_by_id
Update resource information (update_resource)
Get resources with tag information (get_resources)
Search for resources by tag or title (search_resources)
Retrieve tagged resources (get_tagged_resources)
Add tag to a resource (add_tag_to_resource)

#### Search for resources by tag
__Description:__ <br>
When a user wants to view all of the resources related to a specific tag, we need to access the tags table, resources table, and resources tags table. This is because we need to retrieve the resources by tag title. 
<br>
__Preconditions:__ <br>
The tags table has been created and there are tags available to query from the tags table. It is also required that the tags resources table and the resources table has been created. It will return an empty list if there are no resources that match the tag, so it is not required to have a mapping from the tag to the resource. 
<br>
__Test steps:__ <br>
1. Access the resources page
2. Click the tags filter to filter the resources by a tag.

__Expected result:__ <br>
The list of resources are visible to the user that match the tag that was selected.
<br>
__Actual result:__ <br>
A query is executed to retrieve resources that are tagged with the tag title passed in from the front-end. The query joins the resources and tags table using the resource_tags table and returns the matching resources and tag title to the front-end to display to the user.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This is related to the tags table, the resources table, and the resource_tag table. 
<br>
__Post-conditions:__ <br>
The list of resources that match the tag title selected by the user are visible.
<br>


## ProjectsResources Table
### Name:
project_resources
### Description:
Given the many-to-many relationship between our projects and our resources, we need an additional table to store the relationship between them. Each row represents the distinct combination between each project and each resource that are mapped together. The table leverages the primary keys of each project and each resource that are mapped together, and has a foreign key requirement to ensure that the relationship between a project and a resource is referring to a project and a resource that actually exist. 
### Fields:
__id:__ primary key for the table, automatically increments every time a new relationship between a project and a resource is added. <br>
__project_id:__ the primary key of the projects table, points to the project being mapped to a resource. the table requires that this is a foreign key that references the projects table. <br>
__resource_id:__ the primary key of the resources table, points to the resource being mapped to a project. the table requires that this is a foreign key that references the resources table. <br>

### Access Methods:

### Tests:
__Test 1__
<br>
__Description:__
<br>
__Preconditions:__
<br>
__Test steps:__
<br>
__Expected result:__
<br>
__Actual result:__
<br>
__Status:__
<br>
__Notes:__
<br>
__Post-conditions:__
<br>


## ProjectsTags Table
### Name:
project_tags
### Description:
Given the many-to-many relationship between our projects and our tags, we need an additional table to store the relationship between them. Each row represents the distinct combination between each project and each tag that are mapped together. The table leverages the primary keys of each project and each tag that are mapped together, and has a foreign key requirement to ensure that the relationship between a project and a tag is referring to a project and a tag that actually exist.
### Fields:
__id:__ primary key for the table, automatically increments every time a new relationship between a project and a resource is added. <br>
__project_id:__ primary key of the projects table, points to the project being mapped to a tag. the table requires that this is a foreign key that references the projects table. <br>
__tag_id:__ primary key of the tags table, points to the tag being mapped to a project. the table requires that this is a foreign key that references the tags table. <br>
#### Access Methods:

#### Tests:
__Test 1__
<br>
__Description:__
<br>
__Preconditions:__
<br>
__Test steps:__
<br>
__Expected result:__
<br>
__Actual result:__
<br>
__Status:__
<br>
__Notes:__
<br>
__Post-conditions:__
<br>




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
