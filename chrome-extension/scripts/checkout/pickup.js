window.onload = () => {

    chrome.storage.local.get(['info','data'], (res) => {

        if(res.data.checkoutselect == 'on') {
                clickById('pickupDataSubmit')
        }
    });
}