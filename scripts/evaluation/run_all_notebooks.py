import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import glob
import os
import time

def run_notebooks():
    # Make sure we are running from project root
    notebook_dir = 'research/notebooks'
    notebooks = sorted(glob.glob(os.path.join(notebook_dir, '*.ipynb')))
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    
    success_count = 0
    failure_count = 0
    
    for nb_path in notebooks:
        basename = os.path.basename(nb_path)
        print(f"\n==================================================")
        print(f"Executing: {basename}")
        print(f"==================================================")
        
        start_time = time.time()
        
        try:
            with open(nb_path, encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # We run it with the working directory set to research/notebooks so relative paths are correct
            ep.preprocess(nb, {'metadata': {'path': notebook_dir}})
            
            # Write the completed notebook back
            with open(nb_path, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)
            
            elapsed = time.time() - start_time
            print(f"SUCCESS: {basename} ran successfully in {elapsed:.2f} seconds.")
            success_count += 1
            
        except Exception as e:
            print(f"FAILURE: {basename} failed after {time.time() - start_time:.2f} seconds.")
            print(f"Error details: {e}")
            failure_count += 1
            
    print("\n==================================================")
    print(f"Execution Summary: {success_count} succeeded, {failure_count} failed.")
    print("==================================================")
    
    if failure_count > 0:
        exit(1)
    else:
        exit(0)

if __name__ == '__main__':
    run_notebooks()
