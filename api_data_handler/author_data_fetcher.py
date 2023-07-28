import requests

def search_authors(query):
    url = "https://openlibrary.org/search/authors.json"
    params = {"q": query}

    response = requests.get(url, params=params)
    data = response.json()
    return data


if __name__ == "__main__":
    search_word = "Stephen King"  # Replace this with the search word of your choice
    result = search_authors(search_word)

    if result:
        # Process the result here, depending on the structure of the API response
        print(result)
    else:
        print("No data returned.")
