window.onload = () => {

    chrome.storage.local.get(['info','data'], (res) => {

        if(res.data.checkoutselect == 'on') {

            unchangingClickById('Terms1');
            clickById('placeOrder');
        }
    });
}