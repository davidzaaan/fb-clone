console.log('Register page served');

const showPassword = document.querySelector('#show-new-password');
const showPasswordConf = document.querySelector('#show-new-password-conf');
const passwordInput = document.querySelector('#floatingPassword');
const passwordInputConfirmation = document.querySelector('#floatingPassword1');

showPassword.addEventListener('click', () => {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
    } else {
        passwordInput.type = 'password';
    }
});

showPasswordConf.addEventListener('click', () => {
    if (passwordInputConfirmation.type === 'password') {
        passwordInputConfirmation.type = 'text';
    } else {
        passwordInputConfirmation.type = 'password';
    }
});