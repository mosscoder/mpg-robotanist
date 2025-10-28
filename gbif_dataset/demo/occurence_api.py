import os
import json
import requests
from pathlib import Path

species_target = 'Achillea millefolium'
demo_dir = 'gbif_dataset/demo'
image_dir = os.path.join(demo_dir, 'images')
json_dir = os.path.join(demo_dir, 'metadata')

# Use GBIF occurrence API to get 100 records with associated field images for the target species
# Save the image for the first item as well as the citation and metadata as a JSON file

# Link for occurrence API: https://techdocs.gbif.org/en/openapi/v1/occurrence
# Link for image API: https://techdocs.gbif.org/en/openapi/images


def query_gbif_occurrences(species_name, limit=100):
    """
    Query GBIF occurrence API for records with images.

    Args:
        species_name: Scientific name of the species
        limit: Maximum number of records to retrieve

    Returns:
        List of occurrence records with associated images
    """
    base_url = "https://api.gbif.org/v1/occurrence/search"

    params = {
        'scientificName': species_name,
        'mediaType': 'StillImage',  # Only get records with images
        'limit': limit
    }

    print(f"Querying GBIF for {species_name}...")
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()
    results = data.get('results', [])
    print(f"Found {len(results)} records with images")

    return results


def download_image(image_url, save_path):
    """
    Download an image from a URL and save it to disk.

    Args:
        image_url: URL of the image to download
        save_path: Path where the image should be saved
    """
    print(f"Downloading image from {image_url}...")
    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    # Create parent directory if it doesn't exist
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"Image saved to {save_path}")


def save_metadata(record, save_path):
    """
    Save occurrence record metadata and citation to a JSON file.

    Args:
        record: GBIF occurrence record dictionary
        save_path: Path where the JSON file should be saved
    """
    # Extract relevant metadata and citation information
    metadata = {
        'gbifID': record.get('gbifID'),
        'scientificName': record.get('scientificName'),
        'species': record.get('species'),
        'decimalLatitude': record.get('decimalLatitude'),
        'decimalLongitude': record.get('decimalLongitude'),
        'country': record.get('country'),
        'locality': record.get('locality'),
        'eventDate': record.get('eventDate'),
        'recordedBy': record.get('recordedBy'),
        'institutionCode': record.get('institutionCode'),
        'collectionCode': record.get('collectionCode'),
        'catalogNumber': record.get('catalogNumber'),
        'basisOfRecord': record.get('basisOfRecord'),
        'license': record.get('license'),
        'publisher': record.get('publisher'),
        'media': record.get('media', []),
        'citation': f"GBIF Occurrence Download https://doi.org/10.15468/dl.{record.get('gbifID', 'unknown')}",
        'datasetKey': record.get('datasetKey'),
        'publishingOrgKey': record.get('publishingOrgKey')
    }

    # Create parent directory if it doesn't exist
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to {save_path}")


def main():
    """Main execution function."""
    try:
        # Query GBIF for occurrence records
        records = query_gbif_occurrences(species_target, limit=100)

        if not records:
            print(f"No records found for {species_target}")
            return

        # Process the first record
        first_record = records[0]
        record_id = first_record.get('gbifID', 'unknown')

        print(f"\nProcessing record {record_id}...")

        # Get the first image from the record's media
        media = first_record.get('media', [])
        if not media:
            print("No media found in the first record")
            return

        first_image = media[0]
        image_url = first_image.get('identifier')

        if not image_url:
            print("No image URL found in media")
            return

        # Determine image file extension from URL
        image_extension = image_url.split('.')[-1].split('?')[0]
        if image_extension not in ['jpg', 'jpeg', 'png', 'gif']:
            image_extension = 'jpg'  # Default to jpg

        # Create paths using the GBIF ID as the unique identifier
        image_file = os.path.join(image_dir, f"{record_id}.{image_extension}")
        json_file = os.path.join(json_dir, f"{record_id}.json")

        # Download the image
        download_image(image_url, image_file)

        # Save metadata
        save_metadata(first_record, json_file)

        print(f"\n✓ Successfully processed record {record_id}")
        print(f"  Image: {image_file}")
        print(f"  Metadata: {json_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
