# Articles-Web-App
This web application was developed as an article website. It includes the following functionality:
- New users registration
- New articles creation
- View user profile (email, username and user avatar);
- Users can download a new profile photo;
- Ability to login with admin rights;

The application includes the following tools:
- Flask
- Jinja 
- SQLite
- Flask-Login
- WTForms
- Docker

# Running a Docker Container
1. Create an image from a dockerfile: ```docker build -t web_app .```
2. Run the app into a container: ```docker run --name app -p 5000:5000 web_app```

# Web App Pics
<img src="https://i.imgur.com/TFJbJbD.png" alt="home_page_pic" width='900'>
<br>
<img src="https://i.imgur.com/Ndt12zH.png" alt="home_page_pic" width='900'>
