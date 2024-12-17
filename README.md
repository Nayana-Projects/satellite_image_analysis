# Satellite Image Analysis with DVC and Google Cloud Storage

## Project Overview
This project focuses on managing and versioning large satellite image datasets using **Data Version Control (DVC)** with **Google Cloud Storage (GCP)**. The goal is to analyze satellite images for tasks such as land use classification and environmental monitoring, ensuring reproducibility and efficient data management.

---

## Prerequisites
Ensure the following tools and libraries are installed on your system:

### **Required Tools**
- Python 3.x
- Git
- Google Cloud CLI

### **Required Python Libraries**
Install all required libraries with the following command:

```bash
pip install dvc numpy pandas matplotlib scikit-learn tensorflow torch rasterio geopandas
```

---

## Step-by-Step Setup

### **Step 1: Initialize the Project**
1. Navigate to your project directory:
   ```bash
   cd satellite_image_analysis
   ```
2. Initialize DVC:
   ```bash
   dvc init
   ```
3. Verify DVC setup:
   ```bash
   git status
   ```

---

### **Step 2: Add Data to DVC**
1. Add your raw satellite image dataset:
   ```bash
   dvc add data/raw/
   ```
2. Commit the `.dvc` file to Git:
   ```bash
   git add data/raw.dvc .gitignore
   git commit -m "Track raw satellite images with DVC"
   ```

---

### **Step 3: Set Up Google Cloud Storage (GCP)**
Follow these steps to configure a GCP bucket as the remote storage for DVC:

#### **A. Create a New GCP Project**
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and provide a project name.

#### **B. Enable Cloud Storage**
1. Navigate to **APIs & Services > Library**.
2. Ensure **Cloud Storage API** is enabled for your project.

#### **C. Create a GCP Bucket**
1. Go to **Cloud Storage > Buckets**.
2. Click **Create Bucket** and provide the following:
   - **Bucket Name**: Unique name for your project.
   - **Region**: Select a region close to your location.
3. Click **Create**.

#### **D. IAM Role and Service Account**
1. Go to **IAM & Admin > Service Accounts**.
2. Create a service account with the **Storage Admin** role.
3. Generate a key for the service account:
   - Click on the service account > **Keys > Add Key > JSON**.
   - Save the key file securely.

---

### **Step 4: Configure DVC to Use GCP Remote Storage**
1. Add the GCP bucket as the DVC remote:
   ```bash
   dvc remote add -d gcsremote gs://<your-bucket-name>
   ```
   Replace `<your-bucket-name>` with the name of your GCP bucket.

2. Pass the GCP credentials using the service account key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
   ```

---

### **Step 5: Push Data to GCP**
Push the tracked data to your GCP remote:

```bash
dvc push
```

Verify that the data is successfully uploaded to your GCP bucket:
```bash
gsutil ls gs://<your-bucket-name>
```

---

## Working with DVC and Data Versions

### **Add New Versions of Data**
1. Update the `data/raw/` directory with new or modified satellite images.
2. Re-add the updated dataset:
   ```bash
   dvc add data/raw/
   git add data/raw.dvc
   git commit -m "Updated satellite image dataset"
   dvc push
   ```

### **Access Older Versions**
To switch to a previous version of the dataset:
1. Use `git checkout` to navigate to an earlier commit:
   ```bash
   git checkout <commit-hash>
   ```
2. Pull the corresponding data version:
   ```bash
   dvc checkout
   ```

---

## Visualization with Matplotlib
To display the most recent satellite images from your `data/raw/` directory, you can use the following script:

```python
import os
import matplotlib.pyplot as plt

def get_recent_image_paths(directory):
    image_extensions = {".png", ".jpg", ".jpeg", ".tif"}
    images = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in image_extensions]
    return sorted(images, key=os.path.getmtime, reverse=True)[:5]

def display_images(image_paths):
    fig, axes = plt.subplots(1, len(image_paths), figsize=(15, 5))
    for ax, img_path in zip(axes, image_paths):
        img = plt.imread(img_path)
        ax.imshow(img)
        ax.set_title(os.path.basename(img_path))
        ax.axis("off")
    plt.tight_layout()
    plt.show()

data_directory = "data/raw"
recent_images = get_recent_image_paths(data_directory)
display_images(recent_images)
```

Run this script in a Jupyter Notebook to display the most recent satellite images.

---

## Benefits of Using DVC with GCP
- **Version Control**: Easily switch between versions of large datasets.
- **Reproducibility**: Track and share exact versions of datasets for analysis.
- **Efficient Storage**: Deduplication ensures only changes are stored.
- **Scalability**: GCP enables seamless scaling for large datasets.

---

## Commands Summary
| Command                          | Description                                      |
|----------------------------------|--------------------------------------------------|
| `dvc init`                       | Initialize DVC in the project.                  |
| `dvc add <path>`                 | Track data with DVC.                            |
| `dvc remote add -d <name> <url>` | Add a DVC remote storage (GCP, AWS, etc.).      |
| `dvc push`                       | Push tracked data to remote storage.            |
| `dvc checkout`                   | Reconstruct the dataset for a specific version. |
| `git checkout <commit>`          | Switch to a specific Git commit.                |

---

## Final Notes
This project showcases how **DVC** and **Google Cloud Storage** work together to manage, version, and share large datasets for satellite image analysis. The setup ensures reproducibility, efficiency, and collaboration in data science workflows.

Feel free to contribute to this project or reach out for further assistance!
