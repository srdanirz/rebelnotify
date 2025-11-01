function cartScript() {
    chrome.storage.local.get('data', (res) => {
        if(res.data.checkoutselect == 'on') {
            if(document.querySelector('table').children[0].children[0].children[0].childElementCount > 0) {
                window.location.href = 'https://moredrops.cl/cart/checkout';
            } else if(document.querySelector('table').children[0].children[0].children[0].childElementCount == 0) {
                chrome.storage.local.get('lastProduct', (result) => {
                    window.location.href = result.lastProduct;
                })
            }
        }
    });
}