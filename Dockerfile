# use the official Python 3.8 image as the base
FROM python:3.8

# install system dependencies for R and related packages
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# add the GPG key for the R repository and install R
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B8F25A8A73EACF41 \
    && echo "deb https://cloud.r-project.org/bin/linux/debian bookworm-cran40/" > /etc/apt/sources.list.d/r-project.list \
    && apt-get update \
    && apt-get install -y r-base

# install R packages
RUN R -e "install.packages('readxl', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('dplyr', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('gvlma', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('shapr', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('ggplot2', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"
RUN R -e "install.packages('ggtext', dependencies = TRUE, repos = 'https://cran.rstudio.com/')"

# set the working directory for the Python app
WORKDIR /usr/src/app

# copy the rest of the application files
COPY . .

# install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# run the Python application
CMD ["python", "main.py"]