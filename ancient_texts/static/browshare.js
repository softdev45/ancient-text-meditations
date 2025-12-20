
const API_BASE = window.location.href.split('/')[0] + "/api/"
const COMMAND_URL = API_BASE + 'browshare/cmd'; // POST endpoint

const logDisplay = document.getElementById('log-display');
const contentDisplay = document.getElementById('word');

let contentHist = []
let currentElem = 0
let currentVerseNum = NaN
let chapterData = new Map()

function current() {
  return contentHist[0]
}
function getCurrentVerse(){
  return current().verses[currentElem]
}
function getCurrPath() {
  return `#/${current().command}/${currentElem}/${currentVerseNum}`
}
function getBookChapter(verse){
  return `${verse.book}:${verse.chapter}`
}

function handleCommandResult(data) {
  console.log(data)
  if (data.command.startsWith('<>')) {
    // const currentData = getCurrentVerse()
    chapterData.set(getBookChapter(getCurrentVerse()), data.result)
    renderView()
  } else {
    contentHist.unshift({
      verses: data.result,
      command: data.command,
      // verses: data.verses,
      // timestamp: Date.now(),
      // type: 'ref'
    })
    currentVerseNum = data.result[0].verse;
  }
}


async function sendCommand(command) {
  // if (command.length === 0 || isProcessing) return;

  // setProcessingState(true);

  // contentDisplay.innerHTML = `<p class="message">Sending command...</p>`;

  // const wordString = composedWord.map(tile => tile.title).join(' ');

  try {
    const response = await fetch(COMMAND_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ cmd: command })
    });

    const data = await response.json();

    if (!response.ok) {
      renderError(data.detail || data.message || `Server responded with status ${response.status}.`);
    } else {

      handleCommandResult(data)
      renderView();

    }
  } catch (error) {
    console.error('Analysis Request Error:', error);
    renderError(`Could not connect to the analysis endpoint. (${error.message})`);
  } finally {
    // setProcessingState(false);
    // updateWordDisplay();
  }
}

function createVerseElem(data) {
  console.log(data)
  const verse = document.createElement('div')
  const versesOfCurrentChapter = chapterData.get(getBookChapter(getCurrentVerse()))

  if (versesOfCurrentChapter) {
    if (currentVerseNum > versesOfCurrentChapter.length) {
      currentVerseNum = versesOfCurrentChapter.length
    }
    if (currentVerseNum <= 0) {
      currentVerseNum = 1
    }
  }

  if (currentVerseNum != data.verse && versesOfCurrentChapter) {
    data = versesOfCurrentChapter[currentVerseNum - 1]
  }

  console.log(data)


  const ref = document.createElement('span')
  ref.innerText = `${data.book} ${data.chapter}:${data.verse}`
  ref.classList.add('verse-ref')
  const text = document.createElement('div')
  text.classList.add('verse-text')
  text.innerText = data.text

  verse.appendChild(ref)
  verse.appendChild(text)

  return verse;

}

function renderView() {

  contentDisplay.replaceChildren()

  // for (let i = contentHist.length - 1; i >= 0; --i) {
  // if (!currentElem){
  //   currentElem = contentHist.length -1;
  // }

  const resultNode = document.createElement('div')
  const data = current().verses

  const title = document.createElement('div')
  title.innerText = '#' + current().command
  resultNode.appendChild(title)



  // console.log(data)
  data.slice(currentElem, currentElem + 1).forEach(element => {
    const item = createVerseElem(element)
    // item.innerText = JSON.stringify(element);
    resultNode.appendChild(item)
  });
  contentDisplay.appendChild(resultNode)

  history.replaceState(null, null, getCurrPath())

  // }
}

function changeView(step = 0) {
  if (step != 0) {
    currentElem += step;
    currentElem %= current().verses.length
    if (currentElem < 0) currentElem = current().verses.length - 1
    currentVerseNum = getCurrentVerse().verse
    renderView()
  }
}


function stepVerse(step) {
  console.log(currentVerseNum)
  let currentVerse = getCurrentVerse()
  currentVerseNum += step
  if (!chapterData.has(getBookChapter(currentVerse))) {
    sendCommand(`<>${currentVerse.book}:${currentVerse.chapter}`)
  } else {
    console.log(currentVerseNum)
    renderView()
  }
}

function renderError(message) {
  // Keep renderError separate as it displays a temporary, critical message
  logDisplay.innerHTML = `
                    <div class="error-message">
                        <h3>⚠️ Fetch Error</h3>
                        <p>${message}</p>
                        <p><strong>Please ensure your Python Flask server is running on <a href="${API_BASE.slice(0, -5)}" target="_blank">http://127.0.0.1:5000</a>.</strong></p>
                    </div>
                `;
}


document.addEventListener('keydown', function (event) {
  // Check if the pressed key is the tilde (~) key.
  // The key value might be '~' or '`' depending on keyboard layout.
  if (event.key === '~' || event.key === '`') {
    // Prevent default action to avoid issues, e.g., if ~ is part of a browser shortcut.
    event.preventDefault();

    // Get the element to toggle. Replace 'your-element-id' with the actual ID of your element.
    const targetElement = document.getElementById('command-control');
    const commandInput = document.getElementById('query-input');

    if (targetElement) {
      // Toggle the display style property
      if (targetElement.style.display === 'none') {
        targetElement.style.display = 'block'; // Or 'flex', 'inline-block', etc., depending on desired layout
        commandInput.focus();
      } else {
        targetElement.style.display = 'none';
      }
    } else {
      console.warn("Element with ID 'your-element-id' not found.");
    }
  }
  if (event.key === "ArrowUp") {
    event.preventDefault()
    changeView(-1)
  }
  if (event.key === "ArrowDown") {
    event.preventDefault()
    changeView(1)
  }
  if (event.key === "ArrowLeft") {
    event.preventDefault()
    stepVerse(-1)
  }
  if (event.key === "ArrowRight") {
    event.preventDefault()
    stepVerse(1)
  }
});

const queryInput = document.getElementById('query-input');

if (queryInput) {
  queryInput.addEventListener('keydown', function (event) {
    // Check for Ctrl key and Enter key
    // if (event.ctrlKey && event.key === 'Enter') {
    if (event.key === 'Enter') {
      // Prevent the default action (e.g., new line in a textarea)
      event.preventDefault();

      // --- Your custom action goes here ---
      console.log("Ctrl+Enter pressed on the element with ID 'your-element-id'!");
      // For example, if it's a textarea, you might want to submit a form:
      // document.getElementById('your-form-id').submit();
      // Or trigger another function:
      // performMyAction();
      // ------------------------------------
      sendCommand(event.target.value)
      event.target.value = '';
    }
  });
} else {
  console.warn("Element with ID 'your-element-id' not found for Ctrl+Enter binding.");
}






sendCommand('Jesus')


