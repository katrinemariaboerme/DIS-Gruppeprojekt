# DIS-Gruppeprojekt - WatchFlix Documentation

## Project description

WatchFlix is a small Flask web application for browsing movies and TV shows. The application uses a PostgreSQL database and runs through Docker Compose.

The user can:

- view movies and TV shows on the home page
- add content to a watchlist
- mark content as favourite
- view the watchlist
- view favourites

The project follows an MVC-inspired structure:

- `controllers/` handles routes and user requests
- `models/` handles database queries
- `templates/` contains the HTML pages
- `static/` contains CSS and static files
- `database.py` handles database connection and table initialization

---

## E/R diagram

![E/R diagram](static/er-diagram.jpg)

The E/R diagram shows the intended database model for WatchFlix.

The main entity is `Content`, which represents both movies and TV shows. We chose to use one shared `Content` entity instead of separate entities for movies and TV shows, because both types of content share many attributes, such as title, content type, release year and IMDb rating.

The `User` entity represents a user of the application. A user has a `user_id`, username, email and password. The email is unique so that two users cannot register with the same email.

The relationship between `User` and `Content` is handled by the junction table `UserContentList`. This table stores which content a user has added to their list. It also stores a `status`, for example whether the content is in the watchlist or marked as a favourite. The primary key is the combination of `user_id` and `content_id`, because the same user should not have the same content item twice in their list.

The `Actor` entity stores information about actors. Since one actor can appear in many movies or shows, and one movie or show can have many actors, this is a many-to-many relationship. Therefore, we use the junction table `ContentActor`.

The `Genre` entity stores genres such as comedy, drama or action. Since one content item can have many genres, and one genre can belong to many content items, this is also a many-to-many relationship. Therefore, we use the junction table `ContentGenre`.

The main relationships are:

- One `User` can have many rows in `UserContentList`.
- One `Content` item can appear in many users' content lists.
- One `Content` item can have many actors.
- One `Actor` can appear in many content items.
- One `Content` item can have many genres.
- One `Genre` can belong to many content items.

Because of time limitations, the implemented database was simplified compared to the full E/R diagram. In the implementation, we did not include individual users, actors and genres as separate tables. Instead, the implemented version uses `Content`, `Credits`, `Watchlist` and `Favourites`.

---

## Implemented database tables

The implemented version of the database contains the following tables:

```text
Content(
    content_id,
    title,
    show_type,
    description,
    release_year,
    age_certification,
    runtime,
    genres,
    production_countries,
    seasons,
    imdb_id,
    imdb_score,
    imdb_votes,
    tmdb_popularity,
    tmdb_score
)

Credits(
    id,
    person_id,
    content_id,
    name,
    character_name,
    role
)

Watchlist(
    content_id,
    status,
    added_at
)

Favourites(
    content_id,
    status,
    added_at
)
```

The `Content` table stores movie and TV show information. This includes title, type, release year, runtime, genres and IMDb score.

The `Credits` table stores actor and director data. In the full E/R design, actors would have been separated into their own `Actor` table, but in the implemented version the name and role are stored directly in `Credits`.

The `Watchlist` table stores content added to the watchlist.

The `Favourites` table stores content marked as favourite.

The implemented database is therefore a simplified version of the E/R diagram.

---

## Project structure

```text
flask-project/
│
├── app.py
├── database.py
├── db_initialization.py
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── pyproject.toml
│
├── controllers/
│   ├── homepage.py
│   ├── watchlist.py
│   └── favorites.py
│
├── models/
│   ├── homepage.py
│   ├── watchlist.py
│   └── favorites.py
│
├── templates/
│   ├── index.html
│   ├── watchlist.html
│   └── favorites.html
│
├── static/
│   ├── style.css
│   └── er-diagram.jpg
│
└── data/
    ├── titles.csv
    └── credits.csv
```

---

## How to compile the web app from source

The application is written in Python. In this project, "compile from source" means building the Docker image and starting the required containers.

The project uses Docker Compose with two services:

- `web`: the Flask application
- `database`: the PostgreSQL database

Before running the project, Docker Desktop must be installed and running.

The commands below assume that you are in the `flask-project` folder. From the repository root, first run:

```bash
cd flask-project
```

Then build and start the project with:

```bash
docker compose up --build
```

This command:

1. builds the Flask web container from the `Dockerfile`
2. installs the Python dependencies from `pyproject.toml`
3. starts the PostgreSQL database container
4. waits for the database to be ready
5. starts the Flask application

The database is initialized through the `init_db()` function in `database.py`. This function connects to PostgreSQL and creates the required tables if they do not already exist.

The database connection in Docker uses:

```python
host="database"
database="watchflix_db"
user="postgres"
password="123"
```

These values match the PostgreSQL service defined in `docker-compose.yml`.

---

## How to run and interact with the web app

To run the web application, first start Docker Desktop.

Then open a terminal and go to the project folder:

```bash
cd flask-project
```

Start the application with:

```bash
docker compose up --build
```

When the containers are running, open the application in a browser:

```text
http://localhost:5001
```

The reason the application runs on port `5001` is that `docker-compose.yml` maps port `5001` on the local computer to port `5000` inside the Flask container:

```yaml
ports:
  - "5001:5000"
```

---

## Pages in the application

### Home page

URL:

```text
http://localhost:5001/
```

The home page shows movies and TV shows from the database. From this page, the user can add content to the watchlist or mark content as favourite.

### Watchlist page

URL:

```text
http://localhost:5001/watchlist
```

The watchlist page shows content that has been added to the watchlist.

### Favourites page

URL:

```text
http://localhost:5001/favorites
```

The favourites page shows content that has been marked as favourite.

---

## How to stop the application

To stop the application, press:

```bash
CTRL + C
```

in the terminal where Docker Compose is running.

To remove the running containers, run:

```bash
docker compose down
```

To reset the database completely, including the database volume, run:

```bash
docker compose down -v
```

After this, the database will be recreated the next time the application is started.

---

## AI declaration

We used AI tools during the project. ChatGPT was used as an assistant.

AI was used to help with:

- understanding Flask, Docker and PostgreSQL errors
- debugging route, template and database issues

