import requests

def get_book_cover(isbn):
    """Retrieve image link for a cover by isbn num. If no cover image found,
    return None"""
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

    response = requests.get(url)
    data = response.json()

    # Ensure the response contains 'items' field
    if 'items' in data:
        # Get the cover image link
        image_link = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']

        return image_link


