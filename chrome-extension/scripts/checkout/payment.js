window.onload = () => {

    chrome.storage.local.get(['info','data'], (res) => {

        if(res.data.checkoutselect == 'on') {
            if(res.data.payment == 'credit') {
                clickById('paymentModeCredit');
            } else if (res.data.payment == 'debit') {
                clickById('paymentModeDebit');
            }
            if(!document.getElementById('paymentModeSubmit').hasAttribute('disabled')) {
                clickById('paymentModeSubmit');
            }
        }
    });
}