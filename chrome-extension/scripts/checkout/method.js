window.onload = () => {

    chrome.storage.local.get(['info','data'], (res) => {

        if(res.data.checkoutselect == 'on') {
            fillById('cardholderName', res.info.fullname);
            fillById('cardNumber', res.info.cardnumber);
            fillById('expiracy', res.info.expirymonth+'/20'+res.info.expiryyear); // MM/YYYY
            fillById('securityCode', res.info.cvv);
            fillById('docNumber', res.info.rut); // RUT
            setInterval(() => {
                if(document.getElementById('installments').length > 1 && !document.getElementById('installments').hasAttribute('changed')) {
                    fillById('installments', res.info.cuotas) // -1 default => 1,3,6,9,12
                    document.getElementById('installments').setAttribute('changed', 'yes')
                    clickByClass('btn btn-primary btn-block submit_silentOrderPostForm checkout-next', 0)
                }
            }, 500);
        }
    });
}

// document.getElementsByClassName('btn btn-primary btn-block submit_silentOrderPostForm checkout-next')[0]