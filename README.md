## Project Overview
The purpose of this project is to assemble an image dataset for all known plant species at MPG Ranch. We will gather data from the Global Biodiversity Information Facility (GBIF) using their API system. It is critical to document metadata so that we can trace the provenance of each image and cite the contributors. Ultimately, we will train a DINOv3 model to classify images to plant species, and deploy this model on a Jetson Orin Nano for automated plant surveys.

## Demo
Find a demonstration script at `gbif_dataset/demo/occurence_api.py`. This script illustrates best practices for using the GBIF occurrence API to download images and metadata. We must respect the GBIF policies to ensure we do not exceed the rate limits and avoid violating their terms of use.

## TODO
    - [X] Populate the `species_list.txt` file with the scientific names of the species we are targeting for this work.
    - [ ] Study the GBIF API docs: https://techdocs.gbif.org/en/openapi/v1/occurrence, https://techdocs.gbif.org/en/openapi/images
    - [ ] Adatpt the demo script to loop over species list, refactored script goes to `gbif_dataset/download_dataset.py`. Images go to `gbif_dataset/images/{species_name}/{record_id}.{image_extension}` and metadata go to `gbif_dataset/metadata/{species_name}/{record_id}.json`. Limit the script to download a maximum of 1000 images per species.
