function fillById (id, val) {
    if(document.getElementById(id)) {
        document.getElementById(id).focus();
        //document.getElementById(id).setAttribute('value', val);
        document.getElementById(id).value = val;
        document.getElementById(id).dispatchEvent(new Event('change', {
            bubbles: true,
            cancelable: false,
        }));
        document.getElementById(id).blur();
    }
}

function _fillById (id, val) {
    setTimeout(() => {
        if(document.getElementById(id)) {
            document.getElementById(id).focus();
            document.getElementById(id).click();
            //document.getElementById(id).setAttribute('value', val);
            document.getElementById(id).value = val;
            document.getElementById(id).dispatchEvent(new Event('change', {
                bubbles: true,
                cancelable: false,
            }));
            document.getElementById(id).blur();
        }
    }, 1500)
}

function AL(id, val) {
    document.getElementById(id).addEventListener('Change', (event) => {
        if(!event.isTrusted) {
            this.value += event.data;
        }
    }, false)
}

function clickByClass (_class, index) {
    if(document.getElementsByClassName(_class)[index]) {
        document.getElementsByClassName(_class)[index].click();
    }
}

function clickById (id) {
    if(document.getElementById(id)) {
        document.getElementById(id).click();
    }
}

function unchangingClickById (id) {
    if(document.getElementById(id)) {
        document.getElementById(id).click();
        document.getElementById(id).dispatchEvent(new Event('change', {
            bubbles: true,
            cancelable: false
        }));
    }
}

// Listener para reproducir sonido (Manifest V3 compatible)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'playSound') {
        const sound = new Audio(chrome.runtime.getURL('sound.mp3'));
        sound.play().catch(err => console.log('Error playing sound:', err));
        sendResponse({success: true});
    }
    return true;
});