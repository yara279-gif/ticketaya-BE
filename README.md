"# ticketaya-BE" 
"## users branch"
### Methods and their urls
"1. adduser
 2. deleteuser
 3.retrieveuser by id
 4.updateuser by username
 5.searchuser
    1. POST  http://127.0.0.1:8000/account/adduser/
    2. POST http://127.0.0.1:8000/account/deleteuser/
    3. GET http://127.0.0.1:8000/account/retrieveuser/
    4. PATCH http://127.0.0.1:8000/account/updateuser/
    5. GET    http://127.0.0.1:8000/account/searchuser/
### Methods explanation
1. you can add user by adding first_name,last_name,username,password,e_mail.Don't add is admin it is set by default false
2. you can delete user by giving his username
3. you can get all user data by giving his id
4. you can update any user data you aren't required to give all fields only the one you want to update
### NOTE
i have added functionality in add admin to send email to the added admin
    
    "
