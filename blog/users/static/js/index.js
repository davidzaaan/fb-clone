console.log('Hi! Im served :)');

const showPassword = document.querySelector('#show-password');
const passwordInput = document.querySelector('#floatingPassword');

showPassword.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
})