import subprocess
from pathlib import Path
from local_files import nvtt_path, bc1_file, bc3_file, bc1_file_output, bc3_file_output

p = subprocess.run([nvtt_path, f'{bc1_file}', '-f', 'bc1a', '--no-mips=true', f'--output={Path(bc1_file_output).stem}_bc1a.dds'], shell=True, check=True, capture_output=True, encoding='utf-8')
print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}')
p = subprocess.run([nvtt_path, f'{bc3_file}', '-f', 'bc3', '--no-mips=true', f'--output={Path(bc3_file_output).stem}_bc3.dds'], shell=True, check=True, capture_output=True, encoding='utf-8')
print(f'Command {p.args} exited with {p.returncode} code, output: \n{p.stdout}')
