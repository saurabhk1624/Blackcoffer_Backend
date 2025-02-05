# Project Setup & Running Guide

## Prerequisites
Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Steps to Run the Project

1. **Clone the repository**
   ```sh
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build the Docker containers**
   ```sh
   docker compose build
   ```

3. **Start the containers in detached mode**
   ```sh
   docker compose up -d
   ```

4. **Access the Django container**
   ```sh
   docker exec -it django bash
   ```

5. **Run the Django development server**
   ```sh
   ./manage.py runserver 0.0.0.0:8000
   ```

The application should now be running at `http://localhost:8000/`.

## Stopping the Project
To stop the running containers, use:
```sh
docker compose down
```

## Additional Notes
- Ensure the required environment variables are properly configured.
- Modify `docker-compose.yml` as needed for your setup.

---

Happy coding! 🚀

