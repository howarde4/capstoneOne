First project completed from Springboard bootcamp. Solo, full stack project- responsible for both front and back end development as well as design. Backend developed with Flask and WTForms, created a database with SQLAlchemy to store user registration, password, as well as content from page (user saves different drag queens to their database). Username password encrypted with bcrypt. Frontend developed with HTML, CSS and Bootstrap. 



*****************************************
API: https://drag-race-api.readme.io/docs


For this project I used the Rupaul's Drag Race API to search for different drag queens. I used the data to get their name, image and a quote. 

The website is called Rupaul's Drag Race and you can search for different drag queens. When you search for a queen a card comes up showing their name, image and quote. You can add the drag queen to your own All Stars list. All Stars are drag queens that have already competed on the show and are brought back to compete with each other. Your All Star list will be saved so you can always return to it and see who you've added, add more queens, or delete any queens you no longer want on your All Star list. 

This website allows a user to register with a username and password and then they can log in to access their drag queen search and All Star list. 

The user will first come to a register page and will enter a username and password. From there they will be taken to a search page where they can enter a drag queen's name to search. When the drag queen is found a card will appear with the drag queen's name, their image and their specific quote. On the bottom of the card is a button to add the queen to an All Star list. Once the queen is added, the user is redirected to the page with their All Star list. This page has cards displayed in a row of the different drag queens the user has saved with their name, image and quote and a trash can icon at the bottom to delete. The user is able to always come back to this list and add more drag queens or delete them. There is a title bar at the top of the page to logout or redirect to the All Star list or back to the search page. If the Log Out button is pushed the user is logged out and redirected to the Log In page. There is also a button at the bottom right of the search page to delete the user. If the user decides to delete their account they will push the Delete User button and will be logged out and their user data will be deleted. 

I used bootstrap, jquery, flask, jinja and wtforms to complete this. 
