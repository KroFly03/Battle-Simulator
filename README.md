# Battle-Simulator

A small game that allows you to choose two characters for battle. While editing characters, you can give them a name, class, weapons and armor. Each class has individual characteristics and a special skill that it can use once per game.

![](preview.png)

## Requirements

* Python 3.10.6
* Flask 2.1.3

## Build

Linux & MacOS

1. Create virtual environment

```bash
python3 -m venv venv
```

2. Activate virtual environment

```bash
source venv/bin/activate
```

3. Install requirements

```bash
pip install -r requirements.txt
```

4. Run flask application

```bash
export FLASK_APP=run.py
flask run
```
