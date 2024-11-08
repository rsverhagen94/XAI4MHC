# Use the official Python 3.8 image as the base
FROM python:3.8

# Install system dependencies for R and related packages
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    bzip2 \
    ca-certificates \
    libcurl4-openssl-dev \
    libssl-dev \
    build-essential \
    gfortran \
    libxml2-dev \
    libpng-dev \
    libjpeg-dev \
    libxt-dev \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add the GPG key for the R repository and install R (version 4.2.2)
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8F25A8A73EACF41 \
    && echo "deb https://cloud.r-project.org/bin/linux/debian bookworm-cran40/" > /etc/apt/sources.list.d/r-project.list \
    && apt-get update \
    && apt-get install -y r-base

# Install R packages (like 'readxl' and dependencies)
RUN R -e "install.packages('readxl', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('dplyr', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('gvlma', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('shapr', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('ggplot2', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('ggtext', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"

# Set the working directory for the Python app
WORKDIR /usr/src/app

# Copy the rest of the application files (Python app)
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Run the Python application
CMD ["python", "main.py"]
