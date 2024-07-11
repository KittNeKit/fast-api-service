# FastAPI Application with User Authentication and File Uploads

This is a FastAPI application template that demonstrates user authentication and file upload functionalities. It uses SQLAlchemy for database interaction, Pydantic for data validation, and includes Docker Compose for easy deployment.

Features

	•	User Authentication: Allows users to sign up with email and password, and login to obtain a JWT token for authentication.
	•	Post Management: Provides endpoints to add, retrieve, and delete posts. Supports file uploads for posts.
	•	Token-based Authentication: Uses JWT tokens for secure authentication of API endpoints.
	•	In-memory Caching: Implements caching for the GetPosts endpoint to improve performance.
	•	Docker Support: Includes Docker Compose setup for easy deployment with MySQL database.

Prerequisites

Before running the application, ensure you have the following installed:

	•	Python 3.9 or higher
	•	Docker (for Docker Compose setup)

Installation

1.	Clone the repository:
```bash
git clone https://github.com/KittNeKit/fast-api-service
cd fast-api-service
```

2. Run docker-compose up to start the application and MySQL database:
```bash
docker-compose up --build
```


docs: http://localhost:8000/docs