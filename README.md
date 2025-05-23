
![Logo](https://media.discordapp.net/attachments/1170346449083580530/1375417550103515166/logo.png?ex=68319ce9&is=68304b69&hm=63aa05debac38c36ee12dd0cbfd27eab557ccaa15968b07e963acc4eafa8059b&=&format=webp&quality=lossless&width=1488&height=744)


# Captcha Solver

this is my final project for AI studies in school

this project is a tool that enables you to solve textual captchas of length 5 automatically

## Features

- the AI model that solves captchas
- API
- chrome extension
- website for showcase



## Installation

before starting Installation make sure you have the following [*](#comments) 
```bash
python@3.12.10
pip@25.0.1
```

download the project files by running the following
```
git clone https://github.com/JustABoredDev/supreme-happiness && cd supreme-happiness
```

then download the model weights from [here](https://github.com/JustABoredDev/supreme-happiness/releases/download/v0.4/theModelWeights.zip) unzip them and place them in the project's root

### installing prequisites
1. create a virtual enviroment
    ```
    python3 -m venv venv
    ```
2. activate the virtual enviroment
    * on windows:
        ```
        .\venv\Scripts\activate
        ```
    * on macOS/linux:
        ```
        source venv/bin/activate
        ```
3. install the required packages
```bash
  pip install starlette uvicorn captcha torch torchvision opencv-python numpy pillow pandas matplotlib 
```

### loading the chrome extension
go [here](chrome://extensions) (if it doesn't allow you to search chrome://extensions in chrome's search bar)\
enable developer mode and click on 'load unpacked'\
go to the project's root, then head to extension and click on [select folder]
the extension should now be installed.

### comments
<div style="color:gray;font-size:6px">
*versions represent the minimum version anything above should work.
</div>

## Run Locally


### Start the server
on windows:
```bash
  start startCaptchaGenerator && start startSolverServer
```

then double click on ./website/index.html

enjoy!

