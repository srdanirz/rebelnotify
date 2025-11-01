window.onload = () => {
    chrome.storage.local.get(['info','data'], (res) => {
        if(res.data.checkoutselect == 'on') {
            clickByClass('btn btn-primary btn-block checkout-next', 0);
            chrome.storage.local.set({"lastProduct": ''});
        }
    });
}