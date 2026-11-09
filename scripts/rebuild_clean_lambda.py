import os
import shutil
import subprocess
import zipfile

def build_lambda_zip():
    staging_dir = os.path.abspath('scratch/clean_lambda')
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    pkg_json = '''{
  "name": "attech-send-email-lambda",
  "version": "1.0.0",
  "dependencies": {
    "nodemailer": "^9.0.3",
    "pdfkit": "^0.19.1"
  }
}
'''
    with open(os.path.join(staging_dir, 'package.json'), 'w', encoding='utf-8') as f:
        f.write(pkg_json)

    print("Running npm install --omit=dev in clean staging folder...")
    subprocess.run(['npm', 'install', '--omit=dev'], cwd=staging_dir, shell=True, check=True)

    # Copy fonts
    target_fonts = os.path.join(staging_dir, 'fonts')
    os.makedirs(target_fonts, exist_ok=True)
    src_font = os.path.abspath('fonts/NotoSansTC-Regular.ttf')
    if os.path.exists(src_font):
        shutil.copy2(src_font, target_fonts)
        print("Copied NotoSansTC-Regular.ttf")

    # Copy index.js and lambda.js
    shutil.copy2('index.js', staging_dir)
    shutil.copy2('lambda.js', staging_dir)
    print("Copied index.js and lambda.js")

    # Verify that index.js can be loaded and createStyledPDF works
    verify_cmd = [
        'node',
        '-e',
        'const { handler, createStyledPDF } = require("./index.js"); '
        'createStyledPDF("test", [{title: "t", rows: [{label: "l", value: "v"}]}], "c")'
        '.then(b => console.log("Verification OK, PDF bytes:", b.length));'
    ]
    subprocess.run(verify_cmd, cwd=staging_dir, shell=True, check=True)

    # Create clean ZIP archive
    zip_output_path = os.path.abspath('lambda-package.zip')
    backup_zip_path = os.path.abspath('lambda-package.zip.bak')
    if os.path.exists(zip_output_path):
        shutil.copy2(zip_output_path, backup_zip_path)
        os.remove(zip_output_path)

    print(f"Creating clean zip archive at {zip_output_path}...")
    fixed_time = (2026, 11, 9, 12, 0, 0)

    with zipfile.ZipFile(zip_output_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        added_dirs = set()
        for root, dirs, files in os.walk(staging_dir):
            dirs.sort()
            files.sort()

            # Record directories
            for d in dirs:
                full_d = os.path.join(root, d)
                rel_d = os.path.relpath(full_d, staging_dir).replace('\\', '/') + '/'
                if rel_d not in added_dirs:
                    added_dirs.add(rel_d)
                    dinfo = zipfile.ZipInfo(filename=rel_d)
                    dinfo.date_time = fixed_time
                    dinfo.create_system = 3  # UNIX
                    dinfo.external_attr = (0o040755 << 16) | 0x10  # directory
                    zf.writestr(dinfo, '')

            # Record files
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, staging_dir).replace('\\', '/')

                zinfo = zipfile.ZipInfo(filename=rel_path)
                zinfo.date_time = fixed_time
                zinfo.compress_type = zipfile.ZIP_DEFLATED
                zinfo.create_system = 3  # UNIX
                zinfo.external_attr = (0o100644 << 16)  # regular file rw-r--r--

                with open(full_path, 'rb') as f_in:
                    zf.writestr(zinfo, f_in.read())

    zip_size = os.path.getsize(zip_output_path)
    print(f"[SUCCESS] Clean lambda-package.zip created.")
    print(f"Compressed size: {zip_size / (1024 * 1024):.2f} MB")

if __name__ == '__main__':
    build_lambda_zip()
