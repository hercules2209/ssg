import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(dir_path_content,
                             template_path,
                             dest_dir_path,
                             basepath):
    os.makedirs(dest_dir_path, exist_ok=True)
    for name in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, name)
        if os.path.isdir(from_path):
            generate_pages_recursive(
                from_path,
                template_path,
                os.path.join(dest_dir_path, name),
                basepath
            )
        else:
            if not name.endswith(".md"):
                continue
            dest_path = Path(os.path.join(dest_dir_path, name))\
                        .with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} -> {dest_path}")
    markdown_content = open(from_path).read()
    template         = open(template_path).read()
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}",   title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/',  f'src="{basepath}')

    os.makedirs(dest_path.parent, exist_ok=True)
    with open(dest_path, "w") as out:
        out.write(template)

def extract_title(md):
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found in " + md[:30])
