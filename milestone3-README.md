## Q&A 

Q: Why did you choose to test the code that you did?
  
A: I decided to test my main server files that is critical to running my
   application as excpected. So to have my application run accordingly to
   my expectation I have test all my functions that defines the logic of 
   my application and test if my functions holds true to any anticipated 
   input by a client. The test also helps me design or style me files based
   on an open source guide such as Airbnb for my front-end styling. Testing
   also helped me fix many issue that would have poped up after the development
   phase and it would be costly in the real world. So I decided to test my
   back-end logic and styling as well as styling for the front-end to be
   sure that me logic holds true to a given input.

---

Q: Is there anything else you would like to test if you had the time 

A: I wanted to test my Github login method that makes to HTTP requests to
   get user authenticated with Github and I am able to fetch their email (available),
   name, and their Avatar from their account. Also, If I had time I wanted to
   do CICD usng CricleCI. 

---

## Pylint disable errors 
### models.py
   - no-member
   - too-few-public-methods
   - invalid-name
   - too-many-arguments
### app.py
   - no-member
   - too-many-arguments