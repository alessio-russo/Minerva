# Minerva - A flask based tool for automating blogs creation

<img src="/static/images/logo.svg" width="300">

## Overview

Minerva is an open-source project designed to streamline the process of creating and publishing blog posts. 
The tool is based on a Flask web application that automatically analyzes the content of a specified folder, 
generates blog posts based on Markdown (`.md`) files, and formats them using a pre-defined template.


This tool is designed to save you time and effort in creating blog posts from your Markdown files. 
We hope it makes your blogging process more efficient and enjoyable!
## Features

- **Folder-Based Content Analysis:** Automatically scans a specified folder for `.md` files and generates blog structure and posts based on his content.
- **Customizable:** Easily customize the tool by adding new templates or modifying the existing one

## Installation


### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alessio-russo/Minerva.git
   cd Minerva
   ```

2. **Create a Virtual Environment (Optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   python3 app.py
   ```

5. **Access the Application:**

   Open your web browser and navigate to `http://127.0.0.1:8080` 

## Usage

### Setup Your Content Folder

Place all the Markdown (`.md`) files you want to convert into the `content` folder. 
The tool will analyze this folder to generate blog posts.

Folders and files placed in the `content` folder must follow the following conventions:

1. Folder and file names must match the `ID%Name` pattern. The ID is a numeric value used to specify the order in which content is presented
2. Within the contents folder you can create sections, subsections and subsections by nesting folders
3. A folder whose name begins with the `%` character will not be shown within the blog

## Contributing

We welcome contributions to Minerva. Please ensure your code adheres to the project's coding standards and is well-documented.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used for this project.
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine used in the project.
- [Markdown](https://daringfireball.net/projects/markdown/) - The content format supported by the tool.
- [Bootstrap](https://getbootstrap.com/) - Front-end framework used for the user interface design.
