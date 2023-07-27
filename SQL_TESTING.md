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
_________________________________________________________________________________________________________________________________________________________________________________
### Access Methods:
_________________________________________________________________________________________________________________________________________________________________________________
#### 1. add to the tags table
__Name:__ add_to_tags 
<br>
__Description:__ This is a method that allows a user to add a tag to the tags table
<br>
__Parameters:__ The tag title and description that the user wants to use for the new tag. The function also requires a database connection. 
<br>
__Return Values:__ There is no return value, just side effects - the table is updated with the new tag.
<br>
##### Test: Test adding to the tags table
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 2. retrieve all tags
__Name:__ get_tags
<br>
__Description:__ This is a method that retrieves all of the tags from the tags table to render on the front end
<br>
__Parameters:__ The only parameter is a database connection.
<br>
__Return Values:__ The return value is an array of tags and their associated attributes from the tags table.
<br>
##### Test: Test retrieving all tags
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 3. search for resources by tag (get_tagged_resources)
__Name:__ get_tagged_resources
<br>
__Description:__ This is a method that retrieves resources that are tagged with a specific tag.
<br>
__Parameters:__ The method requires a database connection and a tag_id that the user wants to find resources for.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Search for resources by tag
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 4. search for resources by tag(s) or resource title
__Name:__ search_resources
<br>
__Description:__ This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Search for resources by tag(s) or resource title
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
_________________________________________________________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________________________________________________________
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
_________________________________________________________________________________________________________________________________________________________________________________
### Access Methods:
_________________________________________________________________________________________________________________________________________________________________________________
#### 1. Add a resource to the resources table
__Name:__ add_to_resources
<br>
__Description:__ This is a method that allows a user to create and store a new resource.
<br>
__Parameters:__ The method requires a title, link, description that the user wants to use to create a new resource, as well as a database connection.
<br>
__Return Values:__ The return value is the resource id of the newly created resource that's been added to the resources table. 
<br>
##### Test: Test adding a new resource
__Description:__
Test adding a new resource, given input from the user on the front-end add a resource page.
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 2. Retrieve resource from the resources table
__Name:__ get_resource_by_id
<br>
__Description:__ This is a method that allows a user to retrieve a resource from the resources table by a specific resource id.
<br>
__Parameters:__ The method requires a resource id and a database connection.
<br>
__Return Values:__ The return value is the resource and it's associated attributes from the resources table that matches the resource id passed to the function.
<br>
##### Test: Test retrieve a resource
__Description:__
Test retrieval of a single resource for a given resource id from the resources table, given input from the front-end to retrieve a resource.
<br>
__Preconditions:__
The dataset must be created and there must be an active connection to the database. Additionally, the resources table must exist. However, it is not required that the resource id is in the table - if there are no records matching that resource, the query will return an empty array.
<br>
__Test steps:__
1. Navigate to the resources list
2. Select the resource you want to view more information about
3. Ensure that the resource is displayed fully on it's own page, which indicates that it's been successfully retrieved from the backend.

__Expected result:__
A single resource will be displayed to the user
<br>
__Actual result:__
A single resource is displayed on the page to the user, which matches the resource id that was passed to the back-end when the user selected a specific resource object to view. 
<br>
__Status:__
Pass (conducted July 26th 2023)
<br>
__Notes:__
This test is not related to any other tables, since we are querying the resources table by it's primary key, resource_id.
<br>
__Post-conditions:__
The user is able to see the resource that they have selected, and only that resource, since there should only be one resource per resource id. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 3. Retrieve resource and related tags
__Name:__ get_resource
<br>
__Description:__ This is a method that allows a user to retrieve a resource from the resources table by a specific resource id and also return the related tag information associated with the resource retrieved.
<br>
__Parameters:__ The method requires a resource id and a database connection.
<br>
__Return Values:__ The return value is the resource and it's associated attributes from the resources table, as well as the related tag titles from the tags table. 
<br>
##### Test: Test retrieve resource and related tags
__Description:__
Test retrieval of a single resource for a given resource id from the resources table, given input from the front-end to retrieve a resource.
<br>
__Preconditions:__
The dataset must be created and there must be an active connection to the database. Additionally, the resources table must exist. However, it is not required that the resource id is in the table - if there are no records matching that resource, the query will return an empty array.
<br>
__Test steps:__
1. Navigate to the resources list
2. Select the resource you want to view more information about
3. Ensure that the resource is displayed fully on it's own page, which indicates that it's been successfully retrieved from the backend.

__Expected result:__
A single resource will be displayed to the user
<br>
__Actual result:__
A single resource is displayed on the page to the user, which matches the resource id that was passed to the back-end when the user selected a specific resource object to view. 
<br>
__Status:__
Pass (conducted July 26th 2023)
<br>
__Notes:__
This test is not related to any other tables, since we are querying the resources table by it's primary key, resource_id.
<br>
__Post-conditions:__
The user is able to see the resource that they have selected, and only that resource, since there should only be one resource per resource id. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 4. Retrieve all resources from the resources table
__Name:__ get_resources
<br>
__Description:__ This is a method that returns all resources and their associated attributes and associated tags information from the back-end to render on the front-end.
<br>
__Parameters:__ The method requires a database connection.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Test retrieving all resources
__Description:__ <br>
This test is to make sure that we can retrieve all of the resources that exist from the backend, with their associated attributes and details, including tag information. This is to populate our resources page, where we display all of the available resources to a user. This requires use of the tags table, the resources table, and the resource_tags table in order to map the relationship between each resource and it's associated tags. 
<br>
__Preconditions:__ <br>
The resources table, the resource_tags table, and the tags tables must exist, and the database must be created and an active database connection established.
<br>
__Test steps:__ <br>
1. Access the resources page
2. Check to make sure that all of the resources that have been stored previously are visible with all of their associated attributes and tags. 

__Expected result:__ <br>
All of the stored resources should be visible to the user on the resources page, along with their associated attributes and tags. 
<br>
__Actual result:__ <br>
The query executes successfully, mapping the tags for each resource as an array and retrieving all of the other resource attributes for each resource in the table. The left join ensures that if a resource does not have any tags that it is still displayed.
<br>
__Status:__ <br>
Pass - 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
There are no side effects of this access because it is just executing a query, but it should always enable the user to see the entire list of resources on the resources list on the resources page. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 5. Update a resource with new details
__Name:__ update_resource
<br>
__Description:__ This is a method that allows a user to change and save details about an existing resource.
<br>
__Parameters:__ The method requires the id of the resource id, the new title, link, description, and tags. It also requires a database connection.
<br>
__Return Values:__ There is no return value, just side effects. The resources table is updated with the new information about the resource, and the new tags relationship is added to the resources_tag table.
<br>
##### Test: Test updating a resource
__Description:__ <br>
When a user wants to update an existing resource with new details and or new tags, we need to be able to modify the resources table and the resource_tags table to store those changes.
<br>
__Preconditions:__ <br>
The resources table and the resource_tags table must exist, and the database must be created and an active database connection established. Additionally,the resource that the user is trying to edit must exist. 
<br>
__Test steps:__ <br>
1. Access the resources page
2. Select the resource to modify
3. Enter the new information and/or change the tags associated with the resource
4. Select submit
5. Double check that the resource has been updated with the new information

__Expected result:__ <br>
The modified resource details should be visible to the user on the front-end, with the changes that have been made to one or more of the resources attributes and/or the selected tags. 
<br>
__Actual result:__ <br>
The modified resource is visible to the user and the new details are shown, including the change in tags. 
<br>
__Status:__ <br>
Still undergoing testing, but initially passing as of 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
The new resource details are stored in the database and all subsequent accesses to the modified resources will return the new data. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 6. Delete resource from the resource table (delete_resource_by_id)
__Name:__ delete_resource_by_id
<br>
__Description:__ This is a method that allows a user to remove a resource.
<br>
__Parameters:__ The method requires the id of the resource and a database connection.
<br>
__Return Values:__ There is no return value, just side effects. The resource_tags table is updated to remove the rows with the resource id we're deleting, and then the resources table is updated to remove the resource that matches the resource id passed in to the method.
<br>
##### Test: Test deleting a resource
__Description:__ <br>
When a user wants to delete a resource, they need a way to modify both the resources table and the resources_tags table so that there is not a relationship between a tag and a resource that no longer exists. This test ensures that a user can successfully delete a resource from the back-end tables. 
<br>
__Preconditions:__ <br>
The resources table and the resource_tags table must exist, and the database must be created and an active database connection established. 
<br>
__Test steps:__ <br>
1. Access the delete resource section on the resources page
2. Select the resource to delete
3. Select delete to delete the resource
4. Double check the resources list and make sure the resource is no longer available or visible

__Expected result:__ <br>
The resource that is deleted is no longer visible on the resources list. 
<br>
__Actual result:__ <br>
The resource id is passed to the back-end, and any rows where the resource id is tagged to a specific tag are removed. Then, the resource is removed from the resources table. Finally, the user is redirected to see the updated list of of resources, and the resource is no longer visible.
<br>
__Status:__ <br>
Still undergoing testing, but initially passing as of 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
The list of resources should no longer show the resource that has been deleted.
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 7. search for resources by tag or resource
__Name:__ search_resources
<br>
__Description:__ This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Test search for resources by tag(s) or resource title
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 8. get resources by tag id 
__Name:__ get_tagged_resources
<br>
__Description:__ This is a method that retrieves resources that are tagged with a specific tag.
<br>
__Parameters:__ The method requires a database connection and a tag_id that the user wants to find resources for.
<br>
__Return Values:__ The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: test search for resources by tag
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
_________________________________________________________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________________________________________________________
## Projects Table
### Name: 
projects
### Description:
A table that stores the list of user created projects, with an automatically generated unique id, the title that the user adds, and a description of the project. 
### Fields:
__id:__ primary key for the table, automatically increments every time a project is added to the table <br>
__title:__ the user created title for the project -  limit of 150 characters - VARCHAR(150) <br>
__descr:__ the description of the project created by the user - TEXT <br>
_________________________________________________________________________________________________________________________________________________________________________________
### Access Methods:
_________________________________________________________________________________________________________________________________________________________________________________
#### 1. Get all projects 
__Name:__ get_projects
<br>
__Description:__ This is a method that retrieves all of the projects and their associated details from the back-end to render on the front-end.
<br>
__Parameters:__ The method requires a database connection.
<br>
__Return Values:__ The return value is an array of all of the projects in the projects table and their associated attributes. 
<br>
##### Test: Test get all projects
__Description:__ 
The front-end needs to display all of the current projects that have been created.
<br>
__Preconditions:__
It's required that the database is created. It's also required that the projects table exists, and ideally there should be some projects in that table, otherwise it will return an empty array.
<br>
__Test steps:__
1. Navigate to the projects list page
2. Make sure that all of the projects that have been created are visible in the projects list
<br>
__Expected result:__
All of the previously created projects are visible on the projects list.
<br>
__Actual result:__
The projects list shows the list of created projects from the projects table that was returned from the method. If there are no projects in the projects table, it will not show anything.
<br>
__Status:__
Pass - 07/26/2023
<br>
__Notes:__
no notes
<br>
__Post-conditions:__
The list of projects is available to the user whenever they access the projects list page.
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### Add a new project (add_to_projects)
__Name:__ add_to_projects
<br>
__Description:__ This is a method that allows a user to add a new project to the projects table.
<br>
__Parameters:__ The method requires a database connection, as well as the title and description of the project that the user is creating.
<br>
__Return Values:__ There is no return value, only side effects. The projects table is udpated with the new project created by the user.
<br>
##### Test: Test adding a new project
__Description:__ 
The user wants to be able to add a project to the projects table with their inputted title and description.
<br>
__Preconditions:__
It's required that the database is created. If the projects table is not created it is created to add the projects table.
<br>
__Test steps:__
1. Navigate to the add projects page
2. Enter in the title and description
3. Hit submit
4. Check to make sure that the newly created project is visible on the front-end
<br>
__Expected result:__
The newly created project is visible on the front-end projects list.
<br>
__Actual result:__
The projects table is updated with the new project that the user created and the projects list is updated on the front-end to include the new project.
<br>
__Status:__
Pass
<br>
__Notes:__
no notes
<br>
__Post-conditions:__
The projects table contains the new project and it is visible on the list of projects.
<br>
_________________________________________________________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________________________________________________________

## ResourcesTags Table
### Name:
resource_tags
### Description: 
Given the many-to-many relationship between our resources and our tags objects, we need an additional table to store the relationship between them. Each row represents the distinct combination between each tag and each resource that are mapped together. The table leverages the primary keys of the tags and resources tables, and has a foreign key requirement to ensure that the relationship between a resource and a tag is referring to tags and resources that actually exist. 
### Fields:
__id:__ the primary key for teh table, automatically increments every time a new relationship between a tag and a resource is stored. <br>
__resource_id:__ the primary key of the resources table, the key that points to the resource being mapped to a tag. the table requires that this is a foreign key that references the resources table. <br>
__tag_id:__ the primary key of the tags table, the key that points to the tag being mapped to a resource. The table requires that this is a foreign key that references the tags table. <br>
_________________________________________________________________________________________________________________________________________________________________________________
### Access Methods:
_________________________________________________________________________________________________________________________________________________________________________________
#### 1. Get resource by id  with tag information
__Name:__ get_resource
<br>
__Description:__ This is a method that allows a user to retrieve a resource from the resources table by a specific resource id and also return the related tag information associated with the resource retrieved.
<br>
__Parameters:__ The method requires a resource id and a database connection.
<br>
__Return Values:__ The return value is the resource and it's associated attributes from the resources table, as well as the related tag titles from the tags table. 
<br>
##### Test: Test retrieve resource and related tags
__Description:__
Test retrieval of a single resource for a given resource id from the resources table, given input from the front-end to retrieve a resource.
<br>
__Preconditions:__
The dataset must be created and there must be an active connection to the database. Additionally, the resources table must exist. However, it is not required that the resource id is in the table - if there are no records matching that resource, the query will return an empty array.
<br>
__Test steps:__
1. Navigate to the resources list
2. Select the resource you want to view more information about
3. Ensure that the resource is displayed fully on it's own page, which indicates that it's been successfully retrieved from the backend.

__Expected result:__
A single resource will be displayed to the user
<br>
__Actual result:__
A single resource is displayed on the page to the user, which matches the resource id that was passed to the back-end when the user selected a specific resource object to view. 
<br>
__Status:__
Pass (conducted July 26th 2023)
<br>
__Notes:__
This test is not related to any other tables, since we are querying the resources table by it's primary key, resource_id.
<br>
__Post-conditions:__
The user is able to see the resource that they have selected, and only that resource, since there should only be one resource per resource id. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 2. Delete resource and related tags (delete_resource_by_id)
__Name:__ delete_resource_by_id
<br>
__Description:__ This is a method that allows a user to remove a resource.
<br>
__Parameters:__ The method requires the id of the resource and a database connection.
<br>
__Return Values:__ There is no return value, just side effects. The resource_tags table is updated to remove the rows with the resource id we're deleting, and then the resources table is updated to remove the resource that matches the resource id passed in to the method.
<br>
##### Test: Test deleting a resource
__Description:__ <br>
When a user wants to delete a resource, they need a way to modify both the resources table and the resources_tags table so that there is not a relationship between a tag and a resource that no longer exists. This test ensures that a user can successfully delete a resource from the back-end tables. 
<br>
__Preconditions:__ <br>
The resources table and the resource_tags table must exist, and the database must be created and an active database connection established. 
<br>
__Test steps:__ <br>
1. Access the delete resource section on the resources page
2. Select the resource to delete
3. Select delete to delete the resource
4. Double check the resources list and make sure the resource is no longer available or visible

__Expected result:__ <br>
The resource that is deleted is no longer visible on the resources list. 
<br>
__Actual result:__ <br>
The resource id is passed to the back-end, and any rows where the resource id is tagged to a specific tag are removed. Then, the resource is removed from the resources table. Finally, the user is redirected to see the updated list of of resources, and the resource is no longer visible.
<br>
__Status:__ <br>
Still undergoing testing, but initially passing as of 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
The list of resources should no longer show the resource that has been deleted.
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 3. Update resource information (update_resource)
__Name:__ update_resource
<br>
__Description:__ This is a method that allows a user to change and save details about an existing resource.
<br>
__Parameters:__ The method requires the id of the resource id, the new title, link, description, and tags. It also requires a database connection.
<br>
__Return Values:__ There is no return value, just side effects. The resources table is updated with the new information about the resource, and the new tags relationship is added to the resources_tag table.
<br>
##### Test: Test updating a resource
__Description:__ <br>
When a user wants to update an existing resource with new details and or new tags, we need to be able to modify the resources table and the resource_tags table to store those changes.
<br>
__Preconditions:__ <br>
The resources table and the resource_tags table must exist, and the database must be created and an active database connection established. Additionally,the resource that the user is trying to edit must exist. 
<br>
__Test steps:__ <br>
1. Access the resources page
2. Select the resource to modify
3. Enter the new information and/or change the tags associated with the resource
4. Select submit
5. Double check that the resource has been updated with the new information

__Expected result:__ <br>
The modified resource details should be visible to the user on the front-end, with the changes that have been made to one or more of the resources attributes and/or the selected tags. 
<br>
__Actual result:__ <br>
The modified resource is visible to the user and the new details are shown, including the change in tags. 
<br>
__Status:__ <br>
Still undergoing testing, but initially passing as of 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
The new resource details are stored in the database and all subsequent accesses to the modified resources will return the new data. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 4. Get resources with tag information
__Name:__ <br>
get_resources
<br>
__Description:__ <br>
This is a method that returns all resources and their associated attributes and associated tags information from the back-end to render on the front-end.
<br>
__Parameters:__ <br>
The method requires a database connection.
<br>
__Return Values:__ <br>
The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Test retrieving all resources
__Description:__ <br>
This test is to make sure that we can retrieve all of the resources that exist from the backend, with their associated attributes and details, including tag information. This is to populate our resources page, where we display all of the available resources to a user. This requires use of the tags table, the resources table, and the resource_tags table in order to map the relationship between each resource and it's associated tags. 
<br>
__Preconditions:__ <br>
The resources table, the resource_tags table, and the tags tables must exist, and the database must be created and an active database connection established.
<br>
__Test steps:__ <br>
1. Access the resources page
2. Check to make sure that all of the resources that have been stored previously are visible with all of their associated attributes and tags. 

__Expected result:__ <br>
All of the stored resources should be visible to the user on the resources page, along with their associated attributes and tags. 
<br>
__Actual result:__ <br>
The query executes successfully, mapping the tags for each resource as an array and retrieving all of the other resource attributes for each resource in the table. The left join ensures that if a resource does not have any tags that it is still displayed.
<br>
__Status:__ <br>
Pass - 07/27/2023
<br>
__Notes:__ <br>
This is related to the resources table and the resource_tags table.
<br>
__Post-conditions:__ <br>
There are no side effects of this access because it is just executing a query, but it should always enable the user to see the entire list of resources on the resources list on the resources page. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
#### 5. Search for resources by tag or title
__Name:__ <br>
search_resources
<br>
__Description:__ <br>
This is a method that allows a user to search for resources by either resource title or associated tag title.
<br>
__Parameters:__ <br>
The method requires a database connection and a list of words that the user is searching for from the front-end.
<br>
__Return Values:__ <br>
The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: Search for resources by tag(s) or resource title
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 6. Retrieve tagged resources
__Name:__ <br>
get_tagged_resources
<br>
__Description:__ <br>
This is a method that retrieves resources that are tagged with a specific tag.
<br>
__Parameters:__ <br>
The method requires a database connection and a tag_id that the user wants to find resources for.
<br>
__Return Values:__ <br>
The return value is an array of resources and their associated tag information from the joined tags and resources tables.
<br>
##### Test: test search for resources by tag
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
_________________________________________________________________________________________________________________________________________________________________________________
#### 7. Add tag to a resource (add_tag_to_resource)
__Name:__ <br>
add_tag_to_resource
<br>
__Description:__ <br>
This is a method that allows a user to add an existing tag to an existing resource.
<br>
__Parameters:__ <br>
This requires a resource id (of a resource that already exists), a tag id (of a tag that already exists), and a database connection. It also requires that the database exists and that the resources and tags tables exist. If the resource_tags table does not exist it is created in order to add the mapping of resource and tag to the table.
<br>
__Return Values:__ <br>
There is not a return value from the function, just side effects. The resource_tags table is updated with the newly created mapping and the tags associated with each resource are visible on the resources page.
<br>
##### Test: test adding a tag to a resource
__Description:__ <br>
When a user adds a tag to a resource, we have to store the new relationship between a tag and a resource in the back-end so that we can map the two together in other access methods. So this test is not explicitly visible to the user, but is a helper access method for other functions, specifically when a new tag is added to a resource. 
<br>
__Preconditions:__ <br>
The tag id and the resource id of the newly created resource tag relationship must exist in the tags table and the resources table. Also, the database must exist and there must be an active database connection.
<br>
__Test steps:__ <br>
1. Access the add resources page
2. Fill out the add resource form with the title, description, link and any tags associated with the resource.
3. Select submit
4. Confirm that the relationship between the resource and tag has been created by looking at the displayed resource and confirming that 

__Expected result:__ <br>
The resource has the tag associated with it on the resources page and is visible to the user.
<br>
__Actual result:__ <br>
A query is executed against tags_resources table to add a relationship between a tag and a resource by their respective id's. This relationship is used by other functions to display the resource and it's assocaited tag(s) to the user on the front-end.
<br>
__Status:__ <br>
Pass - tested 07/26/2023
<br>
__Notes:__ <br>
This only impact the resource_tags table, but references the tags and resources tables (via their primary keys).
<br>
__Post-conditions:__ <br>
The resources and their associated tags are visible to the user on the front-end when a new relationship between a tag and a resource are created.
<br>
_________________________________________________________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________________________________________________________
## ProjectsResources Table
### Name:
project_resources
### Description:
Given the many-to-many relationship between our projects and our resources, we need an additional table to store the relationship between them. Each row represents the distinct combination between each project and each resource that are mapped together. The table leverages the primary keys of each project and each resource that are mapped together, and has a foreign key requirement to ensure that the relationship between a project and a resource is referring to a project and a resource that actually exist. 
### Fields:
__id:__ primary key for the table, automatically increments every time a new relationship between a project and a resource is added. <br>
__project_id:__ the primary key of the projects table, points to the project being mapped to a resource. the table requires that this is a foreign key that references the projects table. <br>
__resource_id:__ the primary key of the resources table, points to the resource being mapped to a project. the table requires that this is a foreign key that references the resources table. <br>
_________________________________________________________________________________________________________________________________________________________________________________
### Access Methods:
_________________________________________________________________________________________________________________________________________________________________________________
#### Add a resource to a project
__Name:__ <br>
add_projects_resources
<br>
__Description:__ <br>
This is a method that allows a user to add a resource to an existing project.
<br>
__Parameters:__ <br>
The method requires a database connection and a resource id and a project id.
<br>
__Return Values:__ <br>
There is no return value, just side effects.
<br>
##### Test: test adding a resource to a project
__Description:__ <br>
When a user wants to add an existing resource to an existing project, they need a way to add that information to the databse.
<br>
__Preconditions:__ <br>
This method requires that there is a resource that has been already been created in the resources table and a project that has already been created in the projects table. It also requires that there is a database connection and that the project_resources table has already been created.
<br>
__Test steps:__ <br>
1. Access the resources page
2. Select the project that you want to add to the resource to
3. Hit submit
4. Check to make sure that the project contains the resource added to the project
__Expected result:__ <br>
The expected result is that the resource is added to the project that the user wanted to add the resource to.
<br>
__Actual result:__ <br>
The project_resources table is updated with the new relationship between an existing project and an existing resource to render on the front end.
<br>
__Status:__ <br>
Work in progress
<br>
__Notes:__ <br>
This method still needs to be implemented.
<br>
__Post-conditions:__ <br>
The database will be updated with the new mapping between project and resource and the resource will be visible on the respective project page. 
<br>
_________________________________________________________________________________________________________________________________________________________________________________
_________________________________________________________________________________________________________________________________________________________________________________
 
