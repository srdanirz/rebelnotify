/*chrome.runtime.onInstalled.addListener(() => {

    chrome.storage.local.set({'lastProduct': ''});

    let saveinfo = {
        accountemail: null,
        accountpass: null,
        fullname: null,
        cardnumber: null,
        expirymonth: 'default',
        expiryyear: 'default',
        cuotas: 'default',
        cvv: null,
        rut: null
    }

    chrome.storage.local.set({"info": saveinfo});

    let savedata = {
        link: null,
        size: 'default',
        delay: null,
        payment: 'credit',
        atc: 'on',
        sizeselect: 'on',
        checkoutselect: 'on',
        restockselect: 'on',
        soundselect: 'on'
    }

    chrome.storage.local.set({"data": savedata});

    let discord = {
        access_token: null,
        refresh_token: null
    }

    chrome.storage.local.set({"authCodes": discord})
});*/


// Manifest V3 Service Worker
// Note: Audio API no funciona directamente en service workers
// El sonido se reproduce desde los content scripts

chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
        console.log(`Request: ${request}`);
        if(request.playSound == 'playCartSound') {
            // Enviar mensaje de vuelta al content script para reproducir sonido
            chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
                if (tabs[0]) {
                    chrome.tabs.sendMessage(tabs[0].id, {action: 'playSound'});
                }
            });
        }
        sendResponse({success: true});
        return true;
    }
)