# Papyr

<p align="center">
  <img src="assets/logo.png" width="200" height="200" />
</p>

## Description
N/A.

## Installation

### Prerequisites
- **MongoDB** (either local or remote)
- **Python 3.11**
- **awscli** (for access to AWS S3 via boto3)

### Setup
1. **Get MongoDB**
   - [Set up MongoDB locally](https://www.mongodb.com/docs/manual/installation/) or use a remote instance.

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
     # On Windows
     .venv\Scripts\activate
     # On Unix or MacOS
     source .venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
### Environment Variables

The following environment variables are required:

- **S3_BUCKET_NAME**
- **SECRET_KEY** (for JSON Web Tokens)

If you are using a remote instance of MongoDB, you also need to set the following variables:

- **MONGO_HOST** (e.g. cluster0.abcxyz.mongodb.net)
- **MONGO_NAME** (The name of your database)
- **MONGO_USER** (username)
- **MONGO_PASS** (password)

### Running the Application
1. **Run the Application**
   ```bash
   python src/run.py
   ```

   By default, this starts a local server on port 5000. Test it by making a GET request to this endpoint:
   ```bash
   curl http://localhost:5000/api/health
   ```
