window.onload = () => {

    chrome.storage.local.get(['info', 'data'], (res) => {

        if(res.data.checkoutselect == 'on') {
            fillById('j_username', res.info.accountemail);
            fillById('j_password', res.info.accountpass);
            // click login button
            setTimeout(() => {
                clickByClass('btn btn-primary btn-block', 2);
            }, 500);
        }
    });
}