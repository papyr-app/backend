# Papyr

<p align="center">
  <img src="assets/logo.png" width="200" height="200" />
</p>

## Description
N/A.

## Installation For Local Development

### Prerequisites
- **SQLite3**
- **Python 3.11**
- **awscli** (for access to AWS S3 via boto3)

### Setup
1. **Get SQLite3**
     ```bash
     # Via apt
     sudo apt update
     sudo apt install sqlite3

     # Via Brew
     brew install sqlite3
     ```

2. **Install AWS CLI**
   - Install the AWS CLI following the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
   - Configure the AWS CLI with your credentials.
     ```bash
     aws configure
     ```

3. **Set Up Virtual Environment**
   - It is recommended to use a virtual environment for the Python dependencies.
     ```bash
     # Create a virtual environment
     python -m venv .venv

     # Activate the virtual environment
     source .venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Database Migration**
   ```bash
    export FLASK_APP=src/manage.py
    flask db upgrade
   ```

### Environment Variables

The following environment variables are required:

- **S3_BUCKET_NAME**
- **SECRET_KEY** (for JWTs, during local development this can be anything)
- **FLASK_ENV**
- **DEV_DATABASE_URL** 

### Running the Application
1. **Run the Application**
   ```bash
   python src/run.py
   ```

   By default, this starts a local server on port 5000. Test it by making a GET request to this endpoint:
   ```bash
   curl http://localhost:5000/api/health
   ```
