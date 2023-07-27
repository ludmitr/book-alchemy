import requests

KEY = "8795958bc3mshf2d8734866acdd4p18d0f5jsn14a80033d9f2"
HOST = "book-finder1.p.rapidapi.com"


def search_for_book_by_name(book_name: str):
    try:
        url = "https://book-finder1.p.rapidapi.com/api/search"

        querystring = {"title": f"{book_name}", "results_per_page": "5",
                       "page": "1"}

        headers = {
            "X-RapidAPI-Key": KEY,
            "X-RapidAPI-Host": HOST
        }

        res = requests.get(url, headers=headers, params=querystring)
        res.raise_for_status()  # This will raise a HTTPError for 4xx and 5xx status codes

        books = res.json()['results']
        result = [{'title': book['title'],
                   'isbn': book['canonical_isbn'],
                   'author': book['authors'][0],
                   'publication_year': book['published_works'][-1]['copyright']}
                  for book in books]
        return result

    except requests.exceptions.RequestException:
        return {
            "error": "We're having trouble reaching the book database. Please try again later."}

    except KeyError:
        return {
            "error": "We received an unexpected response while trying to find your book. Please try again later."}

    except Exception:
        return {
            "error": "An unexpected error occurred. Please try again later."}
