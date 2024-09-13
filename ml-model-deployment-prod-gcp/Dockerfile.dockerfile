FROM gcr.io/deeplearning-platform-release/base-cpu.py310
WORKDIR /opt/app/
# copy requirements file
COPY requirements.txt .
# Install dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# install additional python helper modules for prediction script to use.
COPY helper_python_modules/ .
RUN pip install -e .
# Copy model artifacts
COPY model_artifacts/model.pkl ./model
COPY model_artifacts/scaler.pkl ./model
# Copy prediction_script.py
COPY prediction_script.py .
# Set the command to run the FastAPI application
CMD ["uvicorn", "prediction_script:app", "--host", "0.0.0.0", "--port", "8080"] 
