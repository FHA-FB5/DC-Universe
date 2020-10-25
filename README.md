# Fachschafts-Bot
<p align="center">
    <a href="https://github.com/FHA-FB5/DC-Universe/releases"><img src="https://img.shields.io/github/downloads/FHA-FB5/DC-Universe/total?label=Downloads&labelColor=30363D&color=2FBF50" alt="Downloads"></a>
    <a href="https://github.com/FHA-FB5/DC-Universe/graphs/contributors"><img src="https://img.shields.io/github/contributors/FHA-FB5/DC-Universe?label=Contributors&labelColor=30363D&color=2FBF50" alt="Contributors"></a>
</p>


## Table of Contents
* [About the project](#about-the-project)
* [Getting Started](#getting-started)
    * [Installing](#installing)
    * [Run bot](#run-bot)
    * [bot.sh](#botsh)
* [Versioning](#versioning)
* [Built With](#built-with)
* [Authors](#authors)

## About the project
*Coming soon*

## Getting Started
### Installing

Install all dependencies
```BASH
apt install libffi-dev libnacl-dev python3-dev python3-pip python3-mysqldb tmux
```

Clone the repository and go to the cloned folder
```BASH
git clone git@github.com:FHA-FB5/DC-Universe.git
cd DC-Universe
```

Install all required packages
```bash
pip3 install -r requirements.txt
```

Copy the example files
```bash
cp .env.example .env
cp alembic.example.ini alembic.ini
```

Edit the .env file (it is important that you add your bot token and database settings)
```bash
nano .env 
```

Edit the alembic.ini file (it is important that you add your database settings in line 38)
```bash
nano alembic.ini
```

Set up the database
```bash
alembic upgrade head
```

### Run bot
You can start the bot manually with the following command
```bash
python3 run.py 
```

or if you are developr and want the bot to restart after each change:
```bash
./dev.sh
```

### bot.sh
For using the `bot.sh` please look [here in the Wiki](https://github.com/FHA-FB5/DC-Universe/wiki/bot.sh).

## Versioning
We use [SemVer](http://semver.org/) for versioning. For available versions, see the [tags on this repository](https://github.com/FHA-FB5/DC-Universe/tags). 

## Built With
* [discord.py](https://github.com/Rapptz/discord.py) - An API wrapper for Discord written in Python.

## Authors
* **Patrik Schmolke** - *Development* - [Rec0gnice](https://github.com/Rec0gnice)
* **Titus Kirch** - *Development* - [TitusKirch](https://github.com/TitusKirch)

See also the list of [contributors](https://github.com/FHA-FB5/DC-Universe/graphs/contributors) who participated in this project.
