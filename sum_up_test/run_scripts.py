import subprocess

def run_script(script_name):
    try:
        result = subprocess.run(['python3', script_name], check=True)
        print(f"Executed {script_name} successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

scripts = ['convert_data.py', 'fill_tables.py', 'queries.py']

for script in scripts:
    run_script(script)
