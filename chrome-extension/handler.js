window.addEventListener('load', () => {
    if(document.getElementsByClassName('alert alert-danger alert-dismissable getAccAlert')[0] && document.getElementsByClassName('alert alert-danger alert-dismissable getAccAlert')[0].innerText.includes('404')) {
        console.log('Error: 404, reloading.');
        window.location.reload();
    }
});