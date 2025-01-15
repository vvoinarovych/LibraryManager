
# Library Manager

**Authors**: Valerii Voinarovych and Weronika Stryj

## Overview

Library Manager is a project designed to help manage library systems, allowing you to track books, users, and manage borrowing transactions. This application is built in Python and uses a set of libraries that can be easily installed via the `requirements.txt` file.

## Setup Instructions

Follow the steps below to set up the project on your local machine.


### 1. Install Required Libraries

Once the virtual environment is activated, install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

This will install all the dependencies listed in the `requirements.txt` file.

### 2. Set Up Environment Variables

Some parts of the application require configuration through environment variables (e.g., database connection details). These variables are stored in a `.env` file.

#### 2.1 Create a `.env` File

Create a `.env` file in the root directory of the project. The file should contain your database credentials like this:

```makefile
# .env example
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library_db
```

Make sure to replace the values with your actual database configuration details.


### 3ю Run the Project

After setting up the environment and installing the required libraries, you can run the project.

For example:

```bash
python main.py
```

This will start the Library Manager application.
