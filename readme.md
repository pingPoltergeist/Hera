<section align="center">
    <div align="center">
        <h1>Hera | Home Media Server</h1>
        <div align="center">
            <img src="https://img.shields.io/badge/Version-0.9.0-fe7d37?style=for-the-badge&logo=Git&logoColor=ffffff" alt="Version - 0.9.0"> 
        </div>
    </div>
</section>

<br>

<div align="center">
    Hera is a home media server for managing movies and TV shows. It is built on Python django and Next JS React framework. It automatically scans specified folders for movies and TV shows and automatically indexes if any match is found. We use TheMovieDB API to fetch details about movies and TV shows.
</div>

<br>
<br>

### Installation

1. Run the file "main.py" with the command `.\back\venv\Python\python.exe main.py`

2. A dialog box will open up. Close that and get into the folder "front"

3. Run the command inside the "front" folder `npm run build` and let the process finish

4. Get one directory back and run "main.py" once again using `.\back\venv\Python\python.exe main.py`

<br>
<br>

### Usage

1. Navigate to `localhost:8008` and sign in with username `hera` and password `Hera1234`

2. Go to the settings panel and add your media libraries and other users as necessary as well

<br>
<br>

### Build

1. Clone the repository in an appropriate directory

2. Use the portable python interpreter provided in the back directory to run the django dev server by using `.\venv\Python\python.exe manage.py runserver` from inside the "back directory"

3. Ensure the configuration in the .env file is correct
   
4. Run the command `npm run dev` inside the "front" directory

<br>
<br>

<div align="center">
    Copyright (c) 2021 Poltergeist
</div>

<br>
<br>
