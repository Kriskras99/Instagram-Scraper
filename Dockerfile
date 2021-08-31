FROM pytorch/pytorch

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    unzip \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

# Clone EasyOCR repo
RUN mkdir -p "/app/easyocr" \
    && git clone "https://github.com/JaidedAI/EasyOCR.git" "/app/easyocr"

# Build
RUN cd "/app/easyocr" \
    && python setup.py build_ext --inplace -j 4 \
    && python -m pip install -e .

# Predownload models
COPY models/* "/root/.EasyOCR/model/"

COPY instagram_scraper/* "/app/scraper/"

RUN cd "/app/scraper" \
    && python -m pip install -r requirements.txt
    && python setup.py install --user

CMD ["python", "/app/scraper/main.py"]
