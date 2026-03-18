import os
import sass
from pathlib import Path

def compile_css():
    src_path = Path(__file__).parent / "src"
    build_path = Path(__file__).parent.parent / "static" / "build"
    compile_folder(src_path, build_path)
    print("\nBuild\n")

def compile_folder(src_folder, dst_folder):
    for root, dirs, files in os.walk(src_folder):
        # Compute matching output directory
        rel = os.path.relpath(root, src_folder)
        out_dir = os.path.join(dst_folder, rel)

        # Make sure output dir exists
        os.makedirs(out_dir, exist_ok=True)

        for file in files:
            if file.endswith(".scss"):
                src_path = os.path.join(root, file)
                out_file = os.path.splitext(file)[0] + ".css"
                dst_path = os.path.join(out_dir, out_file)


                css = sass.compile(filename=src_path, output_style="compressed")

                with open(dst_path, "w") as f:
                    f.write(css)

# Usage
if __name__ == '__main__':
    compile_css()