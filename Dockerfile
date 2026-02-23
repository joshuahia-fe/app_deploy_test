FROM rocker/r-ver:4.2.0

ENV DEBIAN_FRONTEND=noninteractive
ENV RENV_VERSION=v1.0.2
ENV CRAN_MIRROR=https://cran.rstudio.com
ENV LANG=C.UTF-8
ENV TZ=Etc/UTC

# Install system dependencies (single RUN, no-install-recommends)
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
libcurl4-openssl-dev \
libssl-dev \
libxml2-dev \
zlib1g-dev \
ca-certificates \
wget \
tini \
&& rm -rf /var/lib/apt/lists/*
  
# Install remotes and renv (use Rscript)
RUN Rscript --vanilla -e "install.packages('remotes', repos = '${CRAN_MIRROR}')" \
&& Rscript --vanilla -e "remotes::install_github('rstudio/renv@${RENV_VERSION}')"

# Set the working directory
WORKDIR /app
COPY renv.lock renv.lock

# Use renv to restore packages from lockfile (clean install)
RUN Rscript --vanilla -e "options(repos = c(CRAN='${CRAN_MIRROR}')); \
    if (file.exists('renv.lock')) renv::restore(lockfile = 'renv.lock', confirm = FALSE, clean = TRUE)"

# Copy remaining app files (after restore to avoid invalidating package cache)
COPY . /app

EXPOSE 3838

# Run the app using shiny::runApp (host 0.0.0.0 so container is reachable)
CMD ["Rscript", "--vanilla", "-e", "shiny::runApp('/app/app', host = '0.0.0.0', port = 3838)"]
