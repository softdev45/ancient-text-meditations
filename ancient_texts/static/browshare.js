import { buildSentenceOfWordBlocks } from "./blockbuilder.js";

const API_BASE = window.location.href.split('/')[0] + "/api/"
const COMMAND_URL = API_BASE + 'browshare/cmd'; // POST endpoint
const SETTINGS_URL = API_BASE + 'browshare/settings'; // POST endpoint
const LOC_URL = API_BASE + 'location'; // POST endpoint

let SETTINGS = {}
let version = undefined

const logDisplay = document.getElementById('log-display');
const contentDisplay = document.getElementById('word');
let interlinear_div = document.getElementById('interlinear')

let wordSearchResults = new Map()
let chapterData = new Map()
let currentCollection = []
let currentIndex = NaN

// let currentElem = 0
let currentVerseNum = NaN
let currentBookChapter = NaN
let lastCommand = '<cmd>'
let firstHref = ''
let steppingOn = null


function gtCurVerse() {
  if (steppingOn == 'chapter') {
    return chapterData.get(currentBookChapter)[currentVerseNum - 1]
  }
  return currentCollection[currentIndex]
}
// function getCurrentVerse() {
//   if (!gtCurVerse()) {
//     return undefined;
//   }
//   return gtCurVerse().verses[currentElem]
// }
// function getBookChapter(verse = undefined) {
//   if (!verse) {
//     verse = getCurrentVerse()
//   }
//   console.log(currentElem, verse)
//   if (!verse) {
//     return `JOH/1`
//   }
//   return `${verse.book}/${verse.chapter}`
// }
function getCurrPath() {
  console.log(wordSearchResults.size)

  if (!wordSearchResults) {
    return '#'
  }
  return `#/${version.split('_')[1]}/${lastCommand}/${currentIndex}/${currentBookChapter}/${currentVerseNum}`
}

function getCurrentBookChapter() {
  return `${gtCurVerse().book}/${gtCurVerse().chapter}`;
}

function selectVerse() {
  currentBookChapter = getCurrentBookChapter()
  currentVerseNum = gtCurVerse().verse
}

function handleCommandResult(data) {
  console.log('Handling cmd result:', data)
  if (data.command.startsWith('<chapter>')) {
    // const currentData = getCurrentVerse()
    const cmdBookChapter = data.command.split('>')[1]
    // chapterData.set(getBookChapter(getCurrentVerse()), data.result)
    chapterData.set(cmdBookChapter, data.result)
    // renderView()
  } else {
    steppingOn = 'searchResult'
    wordSearchResults.set(data.command, {
      verses: data.result,
      command: data.command,
      // verses: data.verses,
      // timestamp: Date.now(),
      // type: 'ref'
    })
    currentCollection = data.result;
    currentIndex = 0
    lastCommand = data.command
    selectVerse()
    // currentVerseNum = data.result[0].verse;
  }
  renderView()
}


/* function buildSentenceOfWordBlocks(wordList) {
  const container = document.createElement('div');
  container.classList.add('result-block-container'); // Styled for flex layout and background

  if (!Array.isArray(wordList) || wordList.length === 0) {
    container.textContent = "No result blocks to display.";
    container.classList.add('message');
    return container;
  }

  wordList.forEach(word => {
    const block = document.createElement('div');
    block.style.display = "inline";
    block.classList.add('result-block-item', 'oh-font'); // Styled as a colored block
    // block.textContent = word.join('<br>');
    word.slice(0, 4).forEach((part, index) => {
      const subblock = document.createElement('div');
      if (index <= 1) {
        subblock.classList.add('large-font')
      }
      subblock.innerText = part
      block.appendChild(subblock);

    })
    container.appendChild(block);
  });

  return container;
} */

async function sendCommand(command) {
  // if (command.length === 0 || isProcessing) return;

  // setProcessingState(true);

  // contentDisplay.innerHTML = `<p class="message">Sending command...</p>`;

  // const wordString = composedWord.map(tile => tile.title).join(' ');


  console.log('sending cmd for v.: ', version)
  try {
    const response = await fetch(COMMAND_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ cmd: command, version: version })
    });

    const data = await response.json();

    if (!response.ok) {
      renderError(data.detail || data.message || `Server responded with status ${response.status}.`);
    } else {

      logDisplay.innerHTML = ``

      handleCommandResult(data)
      // renderView();

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
  console.log('creating elem:', data)
  const verse = document.createElement('div')
  const versesOfCurrentChapter = chapterData.get(currentBookChapter)


  if (!data && (true || currentVerseNum != data.verse) && versesOfCurrentChapter) {
    if (versesOfCurrentChapter) {
      if (currentVerseNum > versesOfCurrentChapter.length) {
        currentVerseNum = versesOfCurrentChapter.length
      }
      if (currentVerseNum <= 0) {
        currentVerseNum = 1
      }
    }
    data = versesOfCurrentChapter[currentVerseNum - 1]
  }

  console.log(data)

  if (!data) return;


  const verseReference = document.createElement('span')
  verseReference.innerText = `${data.book} ${data.chapter}:${data.verse}`
  verseReference.classList.add('verse-ref')

  const verseText = document.createElement('div')
  verseText.classList.add('verse-text')
  verseText.innerText = data.text

  verse.appendChild(verseReference)
  verse.appendChild(verseText)

  return verse;

}

function renderView(elemToRender = undefined) {

  contentDisplay.replaceChildren()

  // for (let i = contentHist.length - 1; i >= 0; --i) {
  // if (!currentElem){
  //   currentElem = contentHist.length -1;
  // }

  const resultNode = document.createElement('div')
  // if (!current()) return;
  // const data = current().verses

  const title = document.createElement('div')
  title.innerText = '#' + lastCommand
  resultNode.appendChild(title)



  if (!elemToRender) {
    elemToRender = gtCurVerse()
  }
  const item = createVerseElem(elemToRender)
  if (item)
    resultNode.appendChild(item)

  // // console.log(data)
  // data.slice(currentElem, currentElem + 1).forEach(element => {
  //   const item = createVerseElem(element)
  //   // item.innerText = JSON.stringify(element);
  //   resultNode.appendChild(item)
  // });

  contentDisplay.appendChild(resultNode)
  interlinear_div.innerHTML = '';

  history.replaceState(null, null, getCurrPath())

  // }
}

function changeView(step = 0) {
  steppingOn = 'searchResult'
  if (step != 0) {
    currentIndex += step;
    currentIndex %= currentCollection.length
    if (currentIndex < 0) currentIndex = currentCollection.length - 1
    currentVerseNum = gtCurVerse().verse
    currentBookChapter = getCurrentBookChapter()

    renderView()
  }
}


function stepVerse(step) {
  steppingOn = 'chapter'
  console.log('stepping from: ', currentVerseNum, step)
  currentVerseNum += step
  //overstepping check
  const versesOfCurrentChapter = chapterData.get(currentBookChapter)

  if (versesOfCurrentChapter) {
    if (currentVerseNum > versesOfCurrentChapter.length) {
      currentVerseNum = versesOfCurrentChapter.length
    }
    if (currentVerseNum <= 0) {
      currentVerseNum = 1
    }
  }

  if (!chapterData.has(currentBookChapter)) {
    sendCommand(`<chapter>${currentBookChapter}`)
  } else {
    console.log(currentVerseNum)
    let currVerse = chapterData.get(currentBookChapter)[currentVerseNum - 1]
    renderView(currVerse)
  }
}

function renderError(message) {
  // Keep renderError separate as it displays a temporary, critical message
  logDisplay.innerHTML = `
                    <div class="error-message">
                        <h3>⚠️ Fetch Error</h3>
                        <p>${message}</p>
                    </div>
                `;
}

async function loadAncientText() {

  let loc = `${currentBookChapter},${currentVerseNum}`
  loc = loc.replace('/', ',')
  const response = await fetch(LOC_URL + `?loc=${encodeURIComponent(loc)}&type=inter`);

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  const data = await response.json(); // Process the response body as JSON

  // --- 3. Process and Add Data to Page ---
  const verseText = document.createElement('div');
  verseText.appendChild(buildSentenceOfWordBlocks(data));
  interlinear_div.innerHTML = ''
  interlinear_div.appendChild(verseText); //link -< parent

}

document.addEventListener('keydown', async function (event) {
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
    changeView(1)
  }
  if (event.key === "ArrowDown") {
    event.preventDefault()
    changeView(-1)
  }
  if (event.key === "ArrowLeft") {
    event.preventDefault()
    stepVerse(-1)
  }
  if (event.key === "ArrowRight") {
    event.preventDefault()
    stepVerse(1)
  }

  if (event.ctrlKey && event.key === "h") {

    loadAncientText()

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


async function getSettings() {
  try {
    console.log('Getting settings...')
    const response = await fetch(SETTINGS_URL, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      // body: JSON.stringify({ cmd: command })
    });

    const data = await response.json();

    if (!response.ok) {
      renderError(data.detail || data.message || `Server responded with status ${response.status}.`);
    } else {

      SETTINGS = data
      console.log("Settings: ", SETTINGS)
      version = SETTINGS['versions'][0]

      const selectEl = document.getElementById('version-select');
      // const displayEl = document.getElementById('display-version');

      // 3. Create the dropdown items from the list
      SETTINGS['versions'].forEach(ver => {
        const option = document.createElement('option');
        option.value = ver;
        option.textContent = ver;
        selectEl.appendChild(option);
      });

      // Initial display update
      // displayEl.textContent = version;

      // 4. Update the global variable on change
      selectEl.addEventListener('change', (event) => {
        version = event.target.value;
        // displayEl.textContent = version; // Update UI to show it worked
        console.log("Global version is now:", version);
      });

      // renderView();

    }
  } catch (error) {
    console.error('Analysis Request Error:', error);
    renderError(`Could not connect to the analysis endpoint. (${error.message})`);
  } finally {
    // setProcessingState(false);
    // updateWordDisplay();
  }
}


async function goToRef(path) {
  const pth = path.split('/')
  console.log(pth)

  if (!pth.includes('#')) {
    return
  }

  version = 'bible_' + path.at(-6)
  lastCommand = pth.at(-5);
  if (!wordSearchResults.has(lastCommand)) {
    await sendCommand(lastCommand)
  }

  let bookChap = `${pth.at(-3)}/${pth.at(-2)}`
  if (!chapterData.has(bookChap)) (
    await sendCommand(`<chapter>${bookChap}`)
  )

  console.log('Setting current from path: ', path)
  currentIndex = Number(pth.at(-4))
  currentVerseNum = Number(pth.at(-1))
  currentBookChapter = bookChap; //pth.at(-3)
  console.log(currentVerseNum, typeof (currentVerseNum))
  let toRender = chapterData.get(bookChap)[currentVerseNum - 1]

  renderView(toRender);
}


document.addEventListener('DOMContentLoaded', function () {

  console.log(SETTINGS)
  if (!('version' in SETTINGS)) {
    getSettings()
  }

  // console.log(location.href)
  firstHref = location.href
  sendCommand('Jealous')
  goToRef(firstHref)

});


window.stepVerse = stepVerse;
window.changeView = changeView;
window.loadAncientText = loadAncientText;