window.onload =  () => {
    authenticate();

    document.getElementById('status-one').onclick = () => {
        for(let b of document.getElementsByClassName('switch-on')) {
            b.click();
        }
    }
    document.getElementById('status-two').onclick = () => {
        for(let b of document.getElementsByClassName('switch-off')) {
            b.click();
        }
    }

    document.getElementById('button-oauth').onclick = () => {
        window.open('https://discord.com/api/oauth2/authorize?client_id=YOUR_DISCORD_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=identify%20email%20guilds');
    }
    document.getElementById('button-config').onclick = () => {
        toSettings();
    }
    document.getElementById('button-cross').onclick = () => {
        window.close();
    }
    document.getElementById('button-main').onclick = () => {
        toMain();
    }

    document.getElementById('button-save').addEventListener('click', () => {
        let saveinfo = {
            accountemail: document.getElementById('account-email').value,
            accountpass: document.getElementById('account-pw').value,
            fullname: document.getElementById('name').value,
            cardnumber: document.getElementById('cardnumber').value,
            expirymonth: document.getElementById('expirymonth').value,
            expiryyear: document.getElementById('expiryyear').value,
            cuotas: document.getElementById('cuotas').value,
            cvv: document.getElementById('cvv').value,
            rut: document.getElementById('rut').value
        }

        chrome.storage.local.set({"info": saveinfo}, () => {
            alert('Saved!');
        });
    });

    document.getElementById('button-save2').addEventListener('click', () => {
        let savedata = {
            link: document.getElementById('link').value,
            size: document.getElementById('size').value,
            delay: document.getElementById('delay').value,
            payment: document.getElementById('payment-one').checked ? 'credit' : 'debit',
            atc: document.getElementById('atc-one').checked ? 'on' : 'off',
            sizeselect: document.getElementById('size-one').checked ? 'on' : 'off',
            checkoutselect: document.getElementById('checkout-one').checked ? 'on' : 'off',
            restockselect: document.getElementById('restock-one').checked ? 'on': 'off',
            soundselect: document.getElementById('sounds-one').checked ? 'on': 'off'
        }

        chrome.storage.local.set({"data": savedata}, () => {
            alert('Saved!');
        });
    });
    
    document.getElementById('button-start').onclick = () => {
        window.open(document.getElementById('link').value);
    }
}

function authenticate () {
    toMain();
    load();/*
    toLogin();
    chrome.storage.local.get('authCodes', (result) => {
        
        if(result.authCodes != null) {
            fetch('https://discord.com/api/oauth2/token', {
                method: 'POST',
                body: new URLSearchParams({
                    client_id: 'YOUR_DISCORD_CLIENT_ID',
                    client_secret: 'YOUR_DISCORD_CLIENT_SECRET',
                    grant_type: 'refresh_token',
                    refresh_token: result.authCodes.refresh_token,
                }),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(res => { return res.json();
            }).then(data => {
                chrome.storage.local.set({'authCodes': data});
    
                fetch('https://discord.com/api/users/@me/guilds', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${data.access_token}`
                    }
                }).then(res => { return res.json();
                }).then(guilds => {
                    let found = false;
                    for(let i = 0; i < guilds.length; i++) {
                        guilds[i].id == '264445053596991498';
                        found = true;
                        break;
                    }
                    if(found === false) {
                        toLogin();
                    } else if(found === true) {
                        load();
                        toMain();
                    }
                });
    
            });
        }

    });*/
}

function load () {
    chrome.storage.local.get(['info', 'data'], (result) => {
        document.getElementById('account-email').value = result.info.accountemail;
        document.getElementById('account-pw').value = result.info.accountpass;
        document.getElementById('name').value = result.info.fullname;
        document.getElementById('cardnumber').value = result.info.cardnumber; 
        document.getElementById('expirymonth').value = result.info.expirymonth;
        document.getElementById('expiryyear').value = result.info.expiryyear;
        document.getElementById('cuotas').value = result.info.cuotas;
        document.getElementById('cvv').value = result.info.cvv;
        document.getElementById('rut').value = result.info.rut;

        document.getElementById('link').value = result.data.link;
        document.getElementById('size').value = result.data.size;
        document.getElementById('delay').value = result.data.delay;
        if(result.data.payment == 'debit') document.getElementById('payment-two').click();
        if(result.data.atc == 'off') document.getElementById('atc-two').click();
        if(result.data.sizeselect == 'off') document.getElementById('size-two').click();
        if(result.data.checkoutselect == 'off') document.getElementById('checkout-two').click();
        if(result.data.restockselect == 'off') document.getElementById('restock-two').click();

        if(result.data.soundselect == 'off') document.getElementById('sounds-two').click();
    });
}
function toLogin() {
    document.getElementById('second').style.display = 'none';
    document.getElementById('main').style.display = 'none';
    document.getElementById('login').style.display = 'block';
}
function toMain() {
    document.getElementById('second').style.display = 'none';
    document.getElementById('main').style.display = 'block';
    document.getElementById('login').style.display = 'none';
}
function toSettings() {
    document.getElementById('second').style.display = 'block';
    document.getElementById('main').style.display = 'none';
    document.getElementById('login').style.display = 'none';
}