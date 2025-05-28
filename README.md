# Static Site Generator (SSG) - Markdown to HTML

This project is a **Static Site Generator (SSG)** that takes markdown files and converts them into HTML pages. It also supports the inclusion of CSS and images, and it is designed to help users easily build static websites from markdown content.

---

## Features

- **Convert Markdown to HTML**: The core functionality of this tool is to convert markdown files into HTML files, while preserving the structure of headings, paragraphs, lists, code blocks, and more.
- **Static Assets Support**: CSS files (such as `index.css`) and images (such as `rivendell.png`) can be included in the generated static site.
- **Directory Structure**: The generator preserves the folder structure when generating HTML files and copying static assets.
- **Custom Template**: You can easily customize the generated HTML using your own template (`template.html`).

---

## Directory Structure

Here’s a look at the project’s directory structure:

```
content/          # Markdown files used for content (not pushed to GitHub)
  .gitkeep        # Empty folder tracked by Git
  majesty/        # Example folder with markdown content
    index.md      # Example markdown file

static/           # Folder for static assets
  images/         # Folder for images (not pushed to GitHub)
    .gitkeep      # Empty folder tracked by Git
  index.css       # Your custom CSS file

src/              # Source code for the Static Site Generator (SSG)
  main.py         # Main Python script that generates HTML files
  ...
template.html     # HTML template used to generate pages

.gitignore        # Git ignore file to avoid pushing content and static assets to GitHub
README.md         # Project documentation (this file)
main.sh           # Shell script to run the generator and serve the page
test.sh           # Shell script to run tests for the generator
```

---

## Setup Instructions

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/ssg-project.git
cd ssg-project
```

### 2. Install Dependencies

Ensure you have Python >= 3.9 installed.

### 3. Add Your Markdown Content

To add content for your site:
- Place your markdown files inside the `content/` folder. For example, you can create `content/index.md`, `content/about/index.md`, etc.
- To link between files you can include a link in files based on there directory sructure For example in `content/index.md` to link to the about page in `content/about/index.md` you can link it as `/about`
- You can organize the files in subdirectories as needed (e.g., `content/majesty/index.md`).


### 4. Add Static Assets (CSS & Images)

To add custom CSS or images for your site:
- Place your CSS file (e.g., `static/index.css`) in the `static/` folder.
- Add images to `static/images/`.


### 5. Running the Generator

You can generate your site by running the following script:

```bash
./main.sh
```

This will:
1. Generate HTML files for all markdown files in the `content/` directory.
2. Copy static assets (like `index.css` and images) from `static/` to `public/`.
3. Start a local HTTP server to view the generated site.

> The generated HTML files will be saved in the `public/` folder, which is the output directory. The site will be served at `http://localhost:8888`.

---

## Usage

After running the generator, your site will be available locally. To view it, open a browser and go to:

```
http://localhost:8888
```

You can now navigate through your markdown-generated pages, styled with your custom CSS and featuring any images you included in the `static/images/` folder.

---

## Customizing the Template and the css

The HTML pages are generated using a custom template (`template.html`). You can modify this template to adjust the structure and styling of the generated pages. The `{{ Title }}` and `{{ Content }}` placeholders will be replaced with the title (from the H1 header in your markdown) and the HTML content (from the markdown), respectively.
The default css file is present `static/index.css` you can modify that to suit your needs

---

## .gitignore Configuration

In this project, we have configured `.gitignore` to:
- **Ignore the content and static directories** from being pushed to GitHub.
- **Track the empty folders** by using `.gitkeep` files, which allow the folder structure to be kept in Git while ensuring the content remains local.

> **Important**: The `content/` and `static/images/` folders are empty when pushed to GitHub. You can add your own files locally, and they will not be pushed to the remote repository.

---

## Running Tests

This project includes unit tests for the Static Site Generator functionality. You can run the tests with the following command:

```bash
./test.sh
```

This will run all tests in the `src` directory using Python’s `unittest` framework.

---

## Contributing

Feel free to fork this project, make improvements, and open pull requests. If you find any bugs or issues, please create an issue in the GitHub repository.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
