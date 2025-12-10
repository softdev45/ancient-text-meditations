from flask import Flask, render_template, request, session
from ancient_texts.core import get_nav_data

from ancient_texts.use_text_query import trigger_request, get_verse, get_greek
import time

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

#TODO query heb word by eng word

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import random

from ancient_texts.verse_browser import VerseBrowser
from tools.func_tools import gen_book_map

VB = VerseBrowser('./bible_en.xml')
book_map = gen_book_map()

from ancient_texts.heb_char import h_rev

# Initialize the Flask app
# app = Flask(__name__)

# Enable CORS for all routes, allowing the frontend (running on a different origin/port) to access the API.
CORS(app)

# --- Endpoint 1: Initial Grid Content (Load on Page Load) ---
@app.route('/api/grid-content', methods=['GET'])
def get_grid_content():
    """
    API endpoint to fetch the display content for all 25 squares upon page load.
    Now includes the max_word_length limit.
    """
    print("Serving request for initial grid content.")
    # Simulate a quick initial network delay
    #time.sleep(random.uniform(0.1, 0.4)) 
    
    nav = get_nav_data()
    grid_data = []
    for i in range(1, 26):
        # Determine the phase based on the tile number
        title = '<br>'.join((map(lambda el: f"{el}", list(nav.items())[i-1][1])))
        grid_data.append({
            "id": i,
            # This is the content that will be written inside the square
            "display_title": f"{title}",
            "symbol": f"{h_rev[i-1][0] if i < 23 else ''}"
        })
        
        
    # NEW: Define and include the maximum word length limit
    max_length = 9
    
    return jsonify({
        "grid_data": grid_data,
        "max_word_length": max_length
    }), 200


@app.route('/api/location', methods=['GET'])
def location():
    loc:list = request.args.get('loc')
    verse_type:str = str(request.args.get('type', default=False))

    print('getting loc:', loc, 'verse_type=', verse_type)

    if verse_type == 'inter':
        return jsonify(get_verse(loc))


    loc = loc.split(',')
    loc.remove(loc[1])
    result = VB.query_ref(loc)
    return jsonify(result)

# --- Endpoint 2: Detailed Click Data (Process Word) ---
@app.route('/api/process-word', methods=['POST'])
def process_word():
    """
    API endpoint to receive the composed word string via POST and return a custom report.
    """
    try:
        data = request.get_json()
        composed_word = data.get('word', '').strip()
    except Exception:
        composed_word = '' # Treat as empty if parsing fails
        
    print(f"Received word for processing: {composed_word}")
    
    # Simulate longer processing time for analysisכ
    # time.sleep(random.uniform(1.0, 2.5)) 

    # --- Processing Logic ---
    parts = composed_word.split(' ') if composed_word else []
    num_parts = len(parts)
    
    if num_parts == 0:
        return jsonify({
            "report_title": "Processing Error",
            "status": "Failed",
            "color_code": "#dc2626", # Red
            "detail": "No valid tiles were submitted to form a word."
        }), 400

    # Determine report based on number of parts
    # if num_parts < 3:
    #     status_message = "Short Sequence"
    #     detail_msg = f"Sequence contains only {num_parts} part(s). Analysis is preliminary."
    #     color = "#f59e0b" # Yellow
    # elif num_parts <= 5:
    #     status_message = "Standard Sequence"
    #     detail_msg = f"Standard sequence of {num_parts} parts received. Deep analysis initiated."
    #     color = "#10b981" # Green
    # else:
    #     status_message = "Complex Sequence"
    #     detail_msg = f"Long sequence of {num_parts} parts received. Requires extensive computation."
    #     color = "#3b82f6" # Blue
    from ancient_texts.core import get_translation
    
    start_time = time.time()
    # ext_res = trigger_request(get_translation(parts))
    ext_res = trigger_request(','.join(parts))
    import json
    # ext_res = json.load(ext_res)
    print(ext_res)

    total_time = round(time.time() - start_time,3)
    print(ext_res)
    status_message = "N/A"
    color = "#ccccc"

    translated = get_translation(parts)
    print(parts)
    print(translated)
    words_transl = list(zip(parts[::-1], translated[::-1]))
    print(words_transl)

    input_mapped = list(map(lambda elem: elem[0] + f"({elem[1]}) ", words_transl))

    result = {
        "title": f"{composed_word}: ({get_translation(parts)})",
        "input_parts": parts,
        # "parts_translation": translated,
        "input_word": f"{' '.join(input_mapped)}",
        "input_translation": translated,
        "color_code": color,
        "detail": ext_res,
        "load_time_ms": total_time
    }
    print('dbg:', result)

    return jsonify(result), 200 # Returns HTTP 200 success code

@app.route('/api/command', methods=['POST'])
def process_command():
    """
    API endpoint to receive the composed word string via POST and return a custom report.
    """
    try:
        data = request.get_json()
        command = data.get('command', '').strip()
    except Exception:
        command = '' # Treat as empty if parsing fails
        
    print(f"Received command for processing: {command}")

    
    # Simulate longer processing time for analysisכ
    # time.sleep(random.uniform(1.0, 2.5)) 

    # --- Processing Logic ---
    # parts = composed_word.split(' ') if composed_word else []
    # num_parts = len(parts)
    
    
    # if num_parts == 0:
    #     return jsonify({
    #         "report_title": "Processing Error",
    #         "status": "Failed",
    #         "color_code": "#dc2626", # Red
    #         "detail": "No valid tiles were submitted to form a word."
    #     }), 400

    # from nav import get_translation
    
    # start_time = time.time()
    # # ext_res = trigger_request(get_translation(parts))
    # ext_res = trigger_request(','.join(parts))
    # import json
    # # ext_res = json.load(ext_res)
    # print(ext_res)

    # total_time = round(time.time() - start_time,3)
    # print(ext_res)
    # status_message = "N/A"
    # color = "#ccccc"

    # translated = get_translation(parts)
    # words_transl = list(zip(parts, translated))
    # print(words_transl)

    # input_mapped = list(map(lambda elem: elem[0] + f"({elem[1]}) ", words_transl))

    if '@' in command:
        loc = list(map( lambda el: int(el) if el.isdigit() else str(el), command[1:].split(':')))
        verses = VB.query_ref(loc)
    elif '#' in command:
        verses = VB.query_word(command[1:])
    elif '$' in command:
        verses = get_greek(command[1:])
    



    result = {
        # "title": f"{composed_word}: ({get_translation(parts)})",
        "ref": command,
        "verses": verses
        # "input_parts": parts,
        # "parts_translation": translated,
        # "input_word": f"{' '.join(input_mapped)}",
        # "input_translation": translated,
        # "color_code": color,
        # "detail": ext_res,
        # "load_time_ms": total_time
    }
    print('dbg:', result)

    return jsonify(result), 200 # Returns HTTP 200 success code

# --- Server Run Command ---
if __name__ == '__main__':
    print("----------------------------------------------------------------")
    print("Flask Server is running. Access the API at http://127.0.0.1:5000")
    print("Run the index.html file in your browser.")
    print("----------------------------------------------------------------")
    app.run(debug=True, port=5000)
