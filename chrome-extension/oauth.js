window.onload = () => {
    if(window.location.href.includes('https://lonthentication.herokuapp.com/oauth')) {
        let code = window.location.href.split('https://lonthentication.herokuapp.com/oauth?code=')[1];   

        fetch('https://discord.com/api/oauth2/token', {
            method: 'POST',
            body: new URLSearchParams({
                client_id: '773360701288480819',
                client_secret: 'K-fAGkzCrS9xLs2deXHXASTzNId1MyWc',
                code: code,
                grant_type: 'authorization_code',
                redirect_uri: 'https://lonthentication.herokuapp.com/oauth',
                scope: 'identify email guilds'
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
                    alert('Failed to Authenticate');
                } else if(found === true) {
                    alert('Successfully Authenticated');
                }
            }).finally(() => {
                window.close();
            })

        });
/*
        chrome.storage.local.get('authCodes', (result) => {
            fetch('https://discord.com/api/users/@me/guilds', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${result.authCodes.access_token}`
                }
            }).then(res => { return res.json();
            }).then(data => {
                let found = false;
                for(let i = 0; i < data.length; i++) {
                    data[i].id == '264445053596991498';
                    found = true;
                    break;
                }
                if(found === false) {
                    alert('Failed to Authenticate');
                } else if(found === true) {
                    alert('Successfully Authenticated');
                }
            }).finally(() => {
                window.close();
            })
        })*/
    }
}