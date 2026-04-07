MINIMALIST SQLITE-BACKED NEURAL NETWORK

An end-to-end machine learning pipeline built from scratch, utilizing SQLite as a "Memory Block" for neural network weight storage and real-time inference.


OVERVIEW

This project demonstrates a lightweight, fully functional handwriting recognition system for the English alphabet (A-Z). Rather than relying on traditional compiled model files (like .pt or .h5), this architecture unpacks a trained neural network and stores the raw weight matrices directly inside a SQLite database (brain.db). 

A custom Flask backend reads these weights dynamically to compute dot products against live user drawings captured from an HTML5 canvas.

The "Why": This architecture was engineered as the foundational proof-of-concept for a distributed edge-computing pipeline. It is designed to allow heavy model training on a high-performance workstation, while deploying purely database-driven, low-overhead inference to edge devices (e.g., a Raspberry Pi in a robotics context).


REPOSITORY STRUCTURE

- NN_no1.ipynb: The core inference engine and Flask backend. It receives base64 image strings from the frontend, normalizes the 28x28 pixel arrays, accesses the SQLite memory block, and computes the mathematical prediction on the fly.
- index.html: The minimalist frontend UI featuring a responsive HTML5 canvas for drawing characters.
- TRNG.ipynb: The training loop. This script pulls the EMNIST dataset, trains the neural network architecture using PyTorch, extracts the learned weights as numpy arrays, and transplants them directly into the brain.db SQLite file.
- hand_grader.ipynb: A custom human-in-the-loop data labeling application. It pulls live, ungraded drawings from the SQLite log queue, renders the float arrays back into visible images, and allows the user to commit confirmed ground-truth labels to a clean training dataset.
- brain.db: The "Memory Block." This SQLite database acts as both the model file (via the model_store table) and the data collection pipeline (via the drawing_logs table).


QUICK START

Prerequisites:
- Python 3.8+
- flask, torch, torchvision, numpy, Pillow

Running the App:
1. Clone the repository:
   git clone https://github.com/VIC-OVR9000/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME

2. (Optional) If you want to train the model from scratch, run the training notebook:
   jupyter notebook TRNG.ipynb
   (This will download EMNIST, train the model, and overwrite the weights in brain.db.)

3. Launch the inference server:
   jupyter notebook NN_no1.ipynb

4. Open index.html in your browser (or navigate to the local Flask port provided in the terminal), draw a letter, and hit predict!


FUTURE SCOPE: THE GARDEN ID MACHINE

This pipeline is currently being adapted for a physical robotics project: The Garden ID Machine. 

The architecture will upgrade from a flat neural network to a Convolutional Neural Network (CNN
