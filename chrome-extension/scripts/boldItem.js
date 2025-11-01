window.onload = () => {

    document.querySelector("body > app-root").id = "TESTID"


    chrome.storage.local.get(['info', 'data'], (res) => {
        let site = window.location.href.includes('drops') ? 'moredrops' : 'bold';

        if(res.data.sizeselect == 'on') {

            let v = setInterval(() => {
                if(document.getElementsByClassName('sizes-pdp-options')[0]) {
                    //console.log('yeS')
                    clearInterval(v);

                    // site redirect save the product
                    chrome.storage.local.set({"lastProduct": window.location.href});

                    // if shoe size is found boolean
                    let found = false;

                    
                    let l = setInterval(() => {
                        if(document.getElementsByClassName('sizes-pdp-options')[0].children) {
                            console.log('FOUND');
                            clearInterval(l);

                            // finding shoe sizes using regex and loop. breaks when size is found.
                            for(let size of document.getElementsByClassName('sizes-pdp-options')[0].children) {
                                // if matchgin size is found and no shoe sizes before are already selected, then select it and break loop
                                if(size.getAttribute('title') == res.data.size && size.classList[0] != "selected") {
                                    found = true;
                                    size.click();
                                    break;
                                }
                                // when tab refreshes on shoe size selection and a size is detected to have been already selected, break loop and go to next step.
                                if(size.getAttribute('title') == res.data.size && size.classList[0] == "selected") {
                                    found = true;
                                    break;
                                }
                            }
                    
                            // if size is found, add to cart and redirect
                            if(found === true && res.data.atc == "on") {                
                                if(document.getElementsByClassName('btn btn-default btn-block js-add-to-cart btn-icon glyphicon-shopping-cart outOfStock')[0] && document.getElementsByClassName('btn btn-default btn-block js-add-to-cart btn-icon glyphicon-shopping-cart outOfStock')[0].disabled === true) {
                                    if(res.data.restockselect == 'on' && res.data.delay != '') {
                                        setTimeout(() => {
                                            window.location.reload();
                                        }, res.data.delay*1000)
                                    } else {
                                        alert('Size not found.')
                                    }
                                } else {
                                    checkCart(site);
                                }
                                
                            } else if(found === false) {
                                // if shoe size is not found then turn on restock monitor if matching url and delay is not blank
                                if(res.data.restockselect == 'on' && res.data.delay != '' && window.location.href == res.data.link) {
                                    setTimeout(() => {
                                        window.location.reload();
                                    }, res.data.delay*1000)
                                } else {
                                    // if restock monitor is off, just alert size not found.
                                    alert('Size not found.');
                                }
                            }
                        }
                    }, 200)
            } else {
                //console.log('NO')
            }
        }, 200);
        } else if(res.data.atc == "on" && res.data.sizeselect != 'on' && res.data.checkoutselect == 'on') {
            checkCart(site);
        } // if it's the right site and auto checkout is enabled, add the product to cart and redirect to checklout page

    });
}

function checkCart (site) {
    //let site = window.location.href.includes('drops') ? 'moredrops' : 'bold';
    for(let size of document.getElementsByClassName('sizes-pdp-options')[0].children) {
        if(size.classList[0] == "selected") {
            // atc button
            document.getElementsByClassName('btn btn-primary btn-block btn-icon glyphicon-shopping-cart')[0].click();
            
            playSound();

            window.location.href = 'https://bold.cl/cart';

            /*
            chrome.storage.local.get(['data'], (result) => {
                    function stopRun () {
                        clearInterval(run);
                    }
                    let cont = true;
                    let run = setTimeout(() => {
                        fetch(`https://${site}.cl/cart/miniCart/SUBTOTAL?_=1620930014385`, {
                            method: 'GET',
                        }).then(res => {
                            return res.json();
                        }).then(data => {
                            //console.log('Cart Product Count: ' + data.miniCartCount);
                            if(data.miniCartCount >= 1) {
                                stopRun();
                                console.log('At least 1 item in cart. Redirecting...');
                                playSound();
                                if(document.readyState == 'complete') { window.location.href = `https://${site}.cl/cart/checkout`; }
                            } else if (data.miniCartCount < 1) {
                                console.log('0 Stock detected. Retrying.');
                                setTimeout(() => {
                                    if(cont == true && result.data.restockselect == 'on') {
                                        cont = false;
                                        window.location.reload();
                                    }
                                }, result.data.delay*1000-500);
                                stopRun();
                            } else {
                                console.log('UNKNOWN ERROR');
                            }
                        }).catch(error => {
                            console.log('Error: ' + error);
                            stopRun();
                        })
                    }, 500);                
            });*/

        }
    }
}

function playSound() {
    chrome.storage.local.get(['data'], (result) => {
        if(result.data.soundselect == 'on') {
            chrome.runtime.sendMessage({playSound: "playCartSound"});
        }
    })
}