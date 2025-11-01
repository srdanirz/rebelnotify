let lastUrl = location.href; 
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    onUrlChange();
  }
}).observe(document, {subtree: true, childList: true});
 
 
function onUrlChange() {
  let loc = location.href;
  if(loc.includes('cart')) {
      _cartScript();
  } else if(loc.includes('shipping')) {
      _shippingScript();
  } else if(loc.includes('delivery')) {
      _deliveryScript();
  } else if(loc.includes('payment-details')) {
      _paymentScript();
  }
}

function _cartScript() {
    chrome.storage.local.get('data', (res) => {
        let site = window.location.href.includes('bold') ? 'bold' : 'drops';

        if(site == "bold") {
            window.location = "https://bold.cl/checkout/";
        } else {
            if(res.data.checkoutselect == 'on') {
                if(document.querySelector('table').children[0].children[0].children[0].childElementCount > 0) {
                    if(site == 'drops') {
                        window.location.href = 'https://moredrops.cl/cart/checkout';
                    }
                } else if(document.querySelector('table').children[0].children[0].children[0].childElementCount == 0) {
                    chrome.storage.local.get('lastProduct', (result) => {
                        window.location.href = result.lastProduct;
                    })
                }
            }
        }
    });
}

function _shippingScript() {
    chrome.storage.local.get(['data'], (res) => {

        if(res.data.checkoutselect == 'on') {
            if(window.location.href.includes('bold')) {
                setInterval(() => {
                    clickByClass('cx-btn btn btn-block btn-primary', 0);
                }, 200);
            } else {
                clickByClass('btn btn-default js-address-book col-md-12', 0);
                clickByClass('btn btn-primary btn-block', 1);
            }
        }
    });
}

function _deliveryScript() {
    chrome.storage.local.get(['info','data'], (res) => {

        if(res.data.checkoutselect == 'on') {
            if(window.location.href.includes('bold')) {
                setInterval(() => {
                    clickByClass('btn btn-block btn-primary', 0)
                }, 200)
                
            } else {
                clickByClass('btn btn-primary btn-block checkout-next', 0);
            }
            chrome.storage.local.set({"lastProduct": ''});
        }
    });
}

function _paymentScript() {
    chrome.storage.local.get(['info','data'], (res) => {
        if(res.data.checkoutselect == 'on') {
            let o = setInterval(() => {
                /*AL('accountHolderName');
                AL('cardNumber');
                AL('expiracy')
                AL('cVVNumber')
                AL('docNumber')*/
                _fillById('accountHolderName', res.info.fullname);
                _fillById('cardNumber', res.info.cardnumber);
                _fillById('expiracy', res.info.expirymonth+'/20'+res.info.expiryyear); // MM/YYYY
                _fillById('cVVNumber', res.info.cvv);
                _fillById('docNumber', res.info.rut); // RUT
                let v = setInterval(() => {
                    if(document.getElementsByClassName('ng-dropdown-panel-items scroll-host')[0] && document.getElementsByClassName('ng-dropdown-panel-items scroll-host')[0].lastElementChild.childElementCount > 1) {
                        clearInterval(v);
    
                        runCuotas()
    
                        clickByClass('btn btn-primary btn-block submit_silentOrderPostForm checkout-next', 0)
                    }
                }, 500);
            }, 200);
            setTimeout(() => {
                clearInterval(o)
            }, 3000)
        }
    });
}

function runCuotas(cuotas) {
    for(let cuota of document.getElementsByClassName('ng-dropdown-panel-items scroll-host')[0].lastElementChild.children) {
        if(cuota.innerText.split(' ')[0] == cuotas) {
            cuota.click();
        }
    }
}