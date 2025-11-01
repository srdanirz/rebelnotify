function shippingScript() {
    chrome.storage.local.get(['data'], (res) => {
        if(res.data.checkoutselect == 'on') {
            clickByClass('btn btn-default js-address-book col-md-12', 0);
            clickByClass('btn btn-primary btn-block', 1);
        }
    });
}