import requests
if __name__ == '__main__':
    url = "http://127.0.0.1:5001/ask"
    question = input("Please provide a question: ")
    try:
        response = requests.post(url, json={"question": question})

        if response.status_code == 200:
            data = response.json()
            print(f"The answer has been saved to the DB, along with the question!\n"
                  f"Question: {data.get('question')}\nAnswer: {data.get('answer')}")
        else:
            error_message = response.json().get('error')
            print(f"Error: {error_message} (HTTP {response.status_code})")

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors (e.g., connection issues)
        print(f"Error while connecting to the flask server: {e}")
