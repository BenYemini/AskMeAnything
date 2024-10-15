from flask import Flask, jsonify, request
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from DialogueRecord import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Demo123@db:5432/postgresql'

db.init_app(app)

load_dotenv()
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
        answer = chat_completion.choices[0].text.strip()
        if not answer:
            raise Exception("OpenAI returned an empty answer")
        dialogue_record = DialogueRecord(question=question, answer=answer)
        db.session.add(dialogue_record)
        db.session.commit()

        return jsonify({"question": question, "answer": answer}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

