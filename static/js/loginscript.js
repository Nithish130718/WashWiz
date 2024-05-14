const signInBtnLink = document.querySelector('.signInBtn-link');
const wrapper = document.querySelector('.wrapper');
signInBtnLink.addEventListener('click', () => {
    wrapper.classList.toggle('active');
});