import os

def generate_font_css(font_dir='fonts', output_file='fonts.css'):
    # Supported font formats and their CSS format strings
    font_formats = {
        '.ttf': 'truetype',
        '.otf': 'opentype',
        '.woff': 'woff',
        '.woff2': 'woff2'
    }

    css_content = []

    # Check if directory exists
    if not os.path.exists(font_dir):
        print(f"Error: Directory '{font_dir}' not found.")
        return

    # Iterate through files in the font directory
    for filename in os.listdir(font_dir):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in font_formats:
            # Clean up the name for the font-family (e.g., "Average-Regular")
            font_family = name.replace(' ', '-')
            
            # Create the @font-face string
            entry = (
                f"@font-face {{\n"
                f"  font-family: '{font_family}';\n"
                f"  src: url('{font_dir}/{filename}') format('{font_formats[ext]}');\n"
		        # f"  src: url({{ url_for('static', filename='{font_dir}/{filename}') }}) format('{font_formats[ext]}'),"
                f"}}\n"
            )
            css_content.append(entry)

    # Write to the CSS file
    with open(output_file, 'w') as f:
        f.write("\n".join(css_content))

    print(f"Success! Created {output_file} with {len(css_content)} fonts.")

if __name__ == "__main__":
    generate_font_css()