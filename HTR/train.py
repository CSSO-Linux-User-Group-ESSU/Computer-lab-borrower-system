import os
import subprocess
import shutil


# Define paths
scanned_images_dir = 'HTR/processedImages'  # Directory where your images are located
output_dir = '/home/davon/Computer-lab-borrower-system/HTR/output'  # Directory where the training output will be saved
model_name = 'handwriting_model'  # Name of the model
tessdata_dir = '/usr/share/tesseract-ocr/5/tessdata'  # Path to tessdata (change if necessary)
start_model = 'eng'  # Starting model (if you want to fine-tune an existing model)

# Make sure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the previous trained data if it exists and copy it to the output directory
traineddata_path = os.path.join(tessdata_dir, f"{model_name}.traineddata")
if os.path.exists(traineddata_path):
    print(f"Loading previous trained model from {traineddata_path}")
    shutil.copy(traineddata_path, output_dir) 

# Function to run shell commands
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Output: {result.stdout}")

# Generate box files for all images in the directory
for filename in os.listdir(scanned_images_dir):
    if filename.endswith(('.tif', '.png', '.jpg')):
        image_path = os.path.join(scanned_images_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_base = os.path.join(output_dir, base_name)
        print(output_base)

        # Generate box file command (save in output_dir)
        box_command = f"tesseract {image_path} {os.path.join(output_dir, base_name)} -c tessedit_create_boxfile=1"
        print(f"Generating box file for {filename}...")
        run_command(box_command)

        # Convert image to .tif format for LSTMF file generation
        tif_command = f"convert {image_path} {os.path.join(output_dir, base_name)}.tif"
        print(f"Converting {filename} to .tif format...")
        run_command(tif_command)

if input("Please examine the box files\nIf you're done type D: ").upper()!= 'D':
    quit()

# Generate LSTMF files using the box files generated earlier
for filename in os.listdir(scanned_images_dir):
    if filename.endswith(('.tif', '.png', '.jpg')):
        base_name = os.path.splitext(filename)[0]

        # Generate LSTMF file command (using box files from output_dir)
        lstmf_command = f"tesseract {os.path.join(output_dir, base_name)}.tif {os.path.join(output_dir, base_name)} --psm 6 --oem 1 lstm.train"
        print(f"Generating LSTMF file for {filename}...")
        run_command(lstmf_command)


for filename in os.listdir(output_dir):
    if filename.endswith((".box", ".lstmf", ".tif")):
        base_name = os.path.splitext(filename)[0]
        # Combine files into the final .traineddata model
        combine_command = f"combine_tessdata -o {os.path.join(output_dir, model_name)}.traineddata {output_dir}/{base_name}.*"
        print("Combining the trained data into final model...")
        run_command(combine_command)

print(f"Training complete! The trained model is saved as {os.path.join(output_dir, model_name)}.traineddata")

# save_to_use = f"sudo cp HTR/output/handwriting_model.traineddata /usr/share/tesseract-ocr/5/tessdata/"
# run_command(save_to_use)


# for filename in os.listdir(output_dir):
#     file_path = os.path.join(output_dir, filename)
#     os.remove(file_path)  # Delete the file
#     print(f"Deleted: {file_path}")  # Print confirmation of deletion
