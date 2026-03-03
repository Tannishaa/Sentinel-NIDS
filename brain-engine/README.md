# Sentinel: The Brain Engine (AI Inference)

This module acts as the intelligence center for the Sentinel NIDS project. It receives raw network packet data from the C++ Edge Sniffer, calculates stateful traffic metrics, and uses a Random Forest Machine Learning model to detect malicious anomalies (like DoS attacks) in real-time. 

If an attack is detected, it forwards a JSON alert to the Java Spring Boot Manager Dashboard.

## Tech Stack
* **Language:** Python 3.9+ 
* **Libraries:** Scikit-Learn, Pandas, Joblib, Requests, Socket 
* **Dataset:** NSL-KDD (Used for offline training) 

##  Setup Instructions

### 1. Install Dependencies
You need to install the required Python libraries to run the AI model. Open your terminal in this folder and run:
```bash
pip install pandas scikit-learn joblib requests numpy
```

### 2. Add the Dataset
Make sure you have downloaded the NSL-KDD dataset (`KDDTrain+.txt`) and placed it directly inside this `brain-engine` folder. (Note: This file is ignored by git because it is too large).

## How to Run the Brain

### Step 1: Train the Model (Run Once)
Before the system can detect attacks, you must train the Random Forest model.
```bash
python train_model.py
```
This will clean the dataset, train the AI on the safe features, and generate a model.pkl file.

### Step 2: Start the Listener (Runs continuously)
Start the real-time inference engine. This script will open a socket on Port 6000 and wait for the C++ sniffer to send data.

```Bash
python inference.py
```
### Step 3: Test the Pipeline
If Sonika's C++ code is not ready yet, you can simulate a Denial of Service (DoS) attack using the built-in mock script. While inference.py is running in one terminal, open a second terminal and run:

```Bash
python fake_sonika.py
```
You should see the AI detect the high volume of traffic and trigger an alert

## 🔌 The Contracts (Data Flow)

* Input (From C++ on Port 6000): Expects a CSV string: "Source_IP,Destination_Port,Protocol,Size,TCP_Flags" 


* Output (To Java on Port 8080): Sends a JSON HTTP POST request to /api/alert containing the sourceIp, attackType, and confidence.