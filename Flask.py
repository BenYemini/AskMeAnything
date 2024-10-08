from flask import Flask, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


@app.route('/ask', methods=['POST'])
def generate_answer():
    try:
        data = request.json
        question = data.get('question')
        if not question:
            return jsonify({"error": "Please provide a valid question in the question field"}), 400
        chat_completion = client.completions.create(
            prompt=question,
            max_tokens=200,
            model='gpt-3.5-turbo-instruct'
        )

        answer = chat_completion.choices[0].text
        if not answer:
            raise Exception("OpenAI returned an empty answer")

        # TODO: Save question and answer in the DB.

        return jsonify({"question": question, "answer": answer}), 200

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    load_dotenv()
    app.run(host='127.0.0.1', port=5001, debug=True)
