# AI Engineer / Prompt Engineer

Welcome to the repo! This document outlines the tasks and requirements for candidates applying for a position in our team. Below, you'll find detailed descriptions of the job responsibilities, the dataset to be used, and the tasks to be completed as part of the recruitment process.

### Dataset

The dataset to be used for this project can be found on Hugging Face:
[coai/plantuml_generation](https://huggingface.co/datasets/coai/plantuml_generation)

### Task 1: Training a Large Language Model

- **Objective**: Train a Large Language Model using the provided dataset. The LLM should be capable of generating PlantUML code for a given scenario (which is an input to the LLM).
- **Platform**: The training can be conducted on Google Colab.
- **Deliverable**: A trained LLM that can successfully generate PlantUML code from scenario descriptions. Please upload the weights of the LLM on HuggingFace after training the LLM.

### Task 2: Backend and Frontend Development

- **Backend Development**:
  - **Objective**: Develop a backend service that generates PlantUML code from a given scenario and converts it into an image.
  - **Technology**: The backend could be built using FastAPI .
  - **Deliverable**: A functioning backend that takes scenario descriptions as input and outputs PlantUML diagrams as images.

- **Frontend Development**:
  - **Objective**: Develop a frontend interface where users can input scenarios and view the generated PlantUML diagrams.
  - **Technology**: The frontend can be built using ReactJS or NextJS.
  - **Deliverable**: A user-friendly web interface that displays the PlantUML diagrams based on user input.

## Getting Started

1. **Clone/Fork the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up the environment**:
    - Ensure you have Python and Node.js installed.
    - Install necessary Python packages for LLM training and FastAPI backend.
    - Install necessary JavaScript packages for ReactJS/NextJS frontend.
      
3. **Access the dataset**:
    - Download the dataset from [Hugging Face](https://huggingface.co/datasets/coai/plantuml_generation) and prepare it for model training.

4. **Begin with Task 1**:
    - Train the LLM on Google Colab.
    - Upload the weights to HuggingFace under own profile.
    - Save the trained model for use in the backend service.

5. **Develop the Backend**:
    - Create a FastAPI service that uses the trained LLM to generate PlantUML code.
    - Implement functionality to convert PlantUML code into images.

6. **Develop the Frontend**:
    - Build a ReactJS/NextJS application that interacts with the backend.
    - Ensure the frontend can display the generated PlantUML diagrams based on user input.

## Submission

- Ensure all code is well-documented and follows best practices.
- Create a detailed report explaining your approach, challenges faced, and how you overcame them. Let it be brief.
- Submit your final code and report by providing us the links to your repositories. The links to the weights on the HuggingFace should also be present in your report.

We look forward to seeing your innovative solutions and welcoming you to the DIAS Project team!

**Good luck!**



# PlantUML Generator Project

## Overview
This project is composed of several key components that work together to generate PlantUML diagrams from textual descriptions using a GPT-2 machine learning model. It features a FastAPI server for handling API requests, a model for generating the diagrams, and a training script for improving the model's accuracy.

## Components

### `server/api/app.py`

#### Description
This file implements a FastAPI application that provides a RESTful API to generate PlantUML diagrams. It uses authentication to secure endpoints and logs significant events to help in debugging and monitoring.

#### Main Tasks
- **Load Environment Variables**: Utilizes `dotenv` to manage sensitive information securely.
- **Configure Logging**: Sets up logging for different levels and formats to capture runtime information.
- **FastAPI Setup**: Initializes and configures a FastAPI application to handle incoming HTTP requests.
- **Endpoints**:
  - `/health`: A simple health check to confirm the API is operational.
  - `/uml/generator/`: Receives descriptions, generates UML diagrams using a GPT-2 model, and returns the diagrams as base64 images.

### `server/plantumlmodel.py`

#### Description
Defines the `PlantUMLModel` class, which interacts with a pre-trained GPT-2 model to generate UML diagrams based on textual descriptions. It ensures that the model and tokenizer are appropriately initialized and used for generating outputs.

#### Main Tasks
- **Model Initialization**: Loads the GPT-2 model and tokenizer.
- **Generate UML**: Provides a function to process text into UML diagrams by managing the input preparation, model invocation, and output decoding.

### `server/training.py`

#### Description
This script is responsible for training the GPT-2 model using a dataset of UML diagrams and descriptions. It includes data preprocessing, setting up the training environment, executing the training loop, and pushing the trained model to the Hugging Face Hub.

#### Main Tasks
- **Data Preprocessing**: Extracts and prepares training and validation datasets from a `.parquet` file.
- **Training Setup**: Configures training parameters, the model, and the tokenizer for training.
- **Model Training**: Manages the training process including evaluations, logging, and saving the model.
- **Push to Hub**: After training, the model and tokenizer are pushed to the Hugging Face Model Hub for accessibility.
