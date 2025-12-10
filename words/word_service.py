from flask import Flask, request, jsonify

# 1. Initialize the Flask application instance
app = Flask(__name__)

from words.text_query import word_query,verse_query
from tools.func_tools import filter_by

from ancient_texts.core import get_translation

@app.route('/verse',methods=['GET'])
def get_verse():
    loc:str = request.args.get('ref')
    verse = verse_query(loc)
    return jsonify(verse)
    



# --- Service Endpoint ---

# 2. Define the route
# We use methods=['POST'] to specifically handle POST requests to the /related_words path.
@app.route('/related_words', methods=['POST'])
def get_related_words():
    """
    Receives a word in a JSON payload and returns a list of related words.
    
    Expected JSON input: {"input_word": "example"}
    Returns JSON output: {"input_word": "example", "related": ["exhibit", "exemplify", "sample"]}
    """
    # 3. Get the JSON data from the request
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON payload"}), 400
        
        input_word = data.get('input_word')
        
        if not input_word:
            return jsonify({"error": "Missing 'input_word' in JSON payload"}), 400
            
    except Exception:
        # Catch cases where the request body isn't valid JSON
        return jsonify({"error": "Invalid JSON format"}), 400

    # 4. Core Logic (Placeholder)
    # In a real application, you would perform database lookup, NLP, etc., here.
    print(f"INPUT: {input_word}")
    input_seq = input_word.split(',')
    input_seq = get_translation(input_seq)
    words = word_query(input_seq)
    print(words)

    #map to english translations
    if len(words) == 1:
        print('only one match')
        words = words[0]
        for i in range(len(words[1])):
            words[1][i] = words[1][i].repr2()
        related_list = words[1] # return the only list returned in case of one result
    else:
        # words = list(filter( lambda el: (print(el.split('/')) or True) and el.split('/')[2][0].islower(),  map(lambda el: el[1][0].repr2(), words))) #1-wordlist, 0-first; el -> (dist, [word-occur], 'word')
        # filter-out duplicates by root
        names_present = set()
        # words_unique = []
        # for word in words:
        #     if word
         
        words = list(filter( lambda el: el.en[0].islower(),  map(lambda el: el[1][0], words))) #1-wordlist, 0-first; el -> (dist, [word-occur], 'word')

        # related_list = list(map( lambda wrd: wrd.en, words))
        #TODO
        words = filter_by(words, lambda el: el.en)
        def get_word(w):
            print(w)
            result = {key: val for key,val in w.__dict__.items()  if key in ["word","root", "en", "ctx_en"]}
            print(result)
            result.update({'loc': w.get_location(book_name=True), 'verse':w.get_verse()})
            return result
        # related_list = list(map( lambda wrd: wrd.get_data() + [wrd.get_verse(which='ctx')], words))
        related_list = list(map( lambda wrd: get_word(wrd), words))

    # print(set(related_list))
    # if input_word.lower() == "hello":
    #     related_list = ["hi", "greetings", "hey", "salutations"]
    # elif input_word.lower() == "flask":
    #     related_list = ["python", "microservice", "web", "api"]
    # else:
    #     related_list = [f"{input_word}_A", f"{input_word}_B", f"{input_word}_C"]

    # 5. Return the result
    # jsonify serializes the Python dictionary into a JSON response.
    return jsonify({
        "input_word": input_word,
        "related_count": len(related_list),
        "related": list(related_list)
    })

# --- Running the Service ---

def start_server():
    app.run(debug=True, port=5001)

if __name__ == '__main__':
    # Flask runs on http://127.0.0.1:5000/ by default
    app.run(debug=True, port=5001)
