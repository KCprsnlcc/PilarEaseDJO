import os

font_folders = [
    "Aguafina_Script",
    "Epilogue",
    "Gothic_A1",
    "Inter"
]

css_content = ""

for folder in font_folders:
    font_path = f"../fonts/{folder}"
    for font_file in os.listdir(f"./fonts/{folder}"):
        if font_file.endswith(".ttf"):
            font_name = os.path.splitext(font_file)[0]
            css_content += f"""
            @font-face {{
                font-family: '{font_name}';
                src: url('{font_path}/{font_file}') format('truetype');
                font-weight: normal;
                font-style: normal;
            }}
            """

with open("./css/home.css", "w") as css_file:
    css_file.write(css_content)

print("CSS has been generated.")
