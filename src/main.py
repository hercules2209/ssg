import os
import shutil
from block_markdown import markdown_to_html_node

def main():
    source_dir = "static"
    destination_dir = "public"
    
    copy_static(source_dir, destination_dir)

    generate_page_recursive()


def copy_static(src: str, dst: str):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(dst):
        item_path = os.path.join(dst, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_static(src_path, dst_path)
        else:
            shutil.copy(src_path, dst_path)
            print(f"copied: {src_path} to {dst_path}")

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):  # Fixed the typo here
            return stripped_line[2:].strip()
    raise ValueError("No H1 Header found in the markdown")

def generate_page(from_path: str = "content/index.md", template_path: str = "template.html", dest_path: str = "public/index.html"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()

    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    
    title = extract_title(markdown_content)

    parent_node = markdown_to_html_node(markdown_content)
    html_content = parent_node.to_html()  

    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    with open(dest_path, "w") as dest_file:
        dest_file.write(page_content)
    print(f"Page generated and saved to {dest_path}")

def generate_page_recursive(from_path: str = "content/", template_path: str = "template.html", dest_path: str = "public/"):

    for item in os.listdir(from_path):
        item_from_path = os.path.join(from_path, item)
        item_to_path = os.path.join(dest_path, item)

        if os.path.isdir(item_from_path):
            if not os.path.exists(item_to_path):  
                os.makedirs(item_to_path)
            generate_page_recursive(item_from_path, template_path, item_to_path)

        elif item.endswith(".md"):

            html_file_path = os.path.splitext(item_to_path)[0] + ".html"
            generate_page(item_from_path, template_path, html_file_path)

        else:
            continue  

            


if __name__ == "__main__":
    main()
