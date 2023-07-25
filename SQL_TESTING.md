Project Milestone 5: SQL Design (15 pts)
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
