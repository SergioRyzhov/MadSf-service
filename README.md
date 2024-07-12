# MadSf-service

### Meme API

This project implements a RESTful API for managing memes. It allows users to perform CRUD operations (Create, Read, Update, Delete) on memes, including uploading images for each meme. The API is built using FastAPI, SQLAlchemy with async support for database operations, and integrates with an object storage service like MinIO for image uploads.

### How to Download and Run Locally

To download and run the project locally, follow these steps:git 

1. **Clone the Repository:**

```bash
git@github.com:SergioRyzhov/MadSf-service.git
cd MadSf-service
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Start project:**

```bash
docker-compose -f docker-compose up -d
```

4. **Access the API:**

The FastAPI server will start at `http://localhost:8000`.

The swagger documentation is available on `http://localhost:8000/docs`.

## Running Tests

To run tests on a clean database:

1. **Ensure the database is set up:**

   * Make sure the database is created and accessible.
   * Run project as specified above.

     ```bash
     docker exec -it fastapi_app pytest
     ```

### Additional Notes

* **MinIO Setup:** Ensure MinIO is running and accessible at the specified endpoint (`MINIO_ENDPOINT`).
* **3 containers:** Enshure that there are 3 containers is running (fastapi_app, postgres_db, minio)
* **Environment Variables:** Modify `.env` file as per your local setup (If you want).
* **Documentation:** Explore API documentation for endpoint details and schemas.
