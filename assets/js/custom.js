

document.querySelector('#menubar__handler').addEventListener('click', ()=>{
    let element = document.querySelector('nav.header__navbar__navitems');
    let bgdark = document.querySelector('.bg__darkglass');
    element.classList.add('header__navbar__navitems__active');
    bgdark.style.display = 'block';
});

document.querySelector('.toggle__nav').addEventListener('click', ()=>{
    let element = document.querySelector('nav.header__navbar__navitems');
    let bgdark = document.querySelector('.bg__darkglass');
    element.classList.remove('header__navbar__navitems__active');
    bgdark.style.display = 'none';
});

document.querySelector('.bg__darkglass').addEventListener('click', ()=>{
    let element = document.querySelector('nav.header__navbar__navitems');
    let bgdark = document.querySelector('.bg__darkglass');
    element.classList.remove('header__navbar__navitems__active');
    bgdark.style.display = 'none';
});

document.querySelector('#click_lang_open_id').addEventListener('click', ()=>{
    let element = document.querySelector('#lang_wrapper');
    if(element.classList.contains('d-none'))
        element.classList.remove('d-none');
    else
        element.classList.add('d-none');
});

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.getElementById('bg__loader').classList.add('d-none');
        setTimeout( () => {
            document.getElementById('bg__loader').classList.remove('d-none');
        }, 500)
    } else {
        document.getElementById('bg__loader').classList.remove('d-none');
        setTimeout( () => {
            document.getElementById('bg__loader').classList.add('d-none');
        }, 500)
    }
};
