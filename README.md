# Django Social Network
<img src="https://www.sapphiresolutions.net/images/django_development/images/django_development_banner.svg"><br>
## Introduction

Welcome to Django Social Network, a powerful and customizable social networking platform built using the Django web framework. This project aims to provide a foundation for creating feature-rich social networking websites with ease.

## Features

- **User Authentication:** Secure user registration, login, and authentication system.
- **Profiles:** User profiles with customizable information, profile pictures, and cover photos.
- **Posts:** Share updates, photos, and links with other users.
- **Friendship System:** Connect with other users, send and receive friend requests.
- **News Feed:** View a personalized feed of posts from friends.
- **Notifications:** Receive real-time notifications for friend requests, comments, and more.
- **Messaging:** Private messaging system for one-on-one communication.
- **Customization:** Easily extend and customize the platform to meet your specific requirements.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sinanazem/django-social-network.git
   cd django-social-network
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to [http://localhost:8000](http://localhost:8000) to access the application.

## Configuration

- Customize the `settings.py` file to suit your project's specific needs, such as database configuration, static files, and more.

## Contributing

We welcome contributions! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
