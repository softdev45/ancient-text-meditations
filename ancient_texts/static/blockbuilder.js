export
  function buildSentenceOfWordBlocks(wordList) {
  const container = document.createElement('div');
  container.classList.add('result-block-container'); // Styled for flex layout and background

  if (!Array.isArray(wordList) || wordList.length === 0) {
    container.textContent = "No result blocks to display.";
    container.classList.add('message');
    return container;
  }
  console.log(wordList)
  wordList.forEach(word => {
    const block = document.createElement('div');
    block.style.display = "inline";
    block.classList.add('result-block-item', 'oh-font'); // Styled as a colored block
    // block.textContent = word.join('<br>');
    let wrd = undefined
    if ('greek' in word) {
      wrd = [word.greek, word.eng, word.grammar, word.transliter]
    } else {
      wrd = word.slice(0, 4)
    }
    wrd.forEach((part, index) => {
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
}