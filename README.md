![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg) ![Machine-Learning-Client Tests](https://github.com/software-students-fall2024/4-containers-ballincat43/actions/workflows/machine.yaml/badge.svg) ![Web-App Tests](https://github.com/software-students-fall2024/4-containers-ballincat43/actions/workflows/web.yaml/badge.svg)

# Ballin Speech Analyzer

## Description

Our project is a speech analyzer that recieves microphone or audio file input, transcribes it to text, then computes various data from it, including a variety score, most common word, longest word, and more, allowing the user to see how they might improve their use of language. Users can also compare their own statistics with everone else who has used the app.

## Teammates:
- Bohan Hou, [Github](https://github.com/bowohan)
- Joseph Hwang, [Github](https://github.com/JosephNYU)
- David Jimenez, [Github](https://github.com/drj8812)
- Sean Lee, [Github](https://github.com/jseanlee)

## Configuration and How to Run Application

### Setting up 
Before compiling and running this project, make sure you have __Docker Desktop__ installed and running on your local machine. 

To compile and run this project, clone this respository in a directory of your choosing:

```
git clone <repository url> 
```

__Environment variables__: To connect the database to the rest of the project, a `.env` file will be provided privately to instructors. Add this file to the root directory of the respository. 

Navigate into the respository that you have just cloned, and run the following docker command to compile and run the program: 

```
docker compose up --build -d
```

Once running, the terminal should produce a link to the web app that you can access:
```
https://127.0.0.1:5000
```

### Using the App
The app will start off at the login page. You can choose to create your own account, in which you need to create a username and password, or you can sign in using this premade account: `username = bob123 | password = test`. Logging in will take you to the user home menu, from where you can use the app's features. To start, hit the start record button, then the stop record button. Note that it may take some time to process your speech. To ensure a smooth experience, try to use Google Chrome as your web browser.

### Closing the App
To close the app, run the following docker command in your terminal:
```
docker compose down
```
