const header = document.querySelector('#header')
const username = document.querySelector('#username')
const email = document.querySelector('#email')
const otp = document.querySelector('#OTP')
const password = document.querySelector('#newPassword')
const submitButton = document.querySelector('#input')
const warning = document.querySelector('#warning')
const warningMessage = document.querySelector('#warningMessage')
const warningCloseBtn = document.querySelector('#closeButton')
const submitButtonText = document.querySelector('.button__text')
const forgetPassBtn = document.querySelector('#forgetPassBtn')
const signinUPButton = document.querySelector('#signinUPButton')
const signinUpMessage = document.querySelector('#siginUPMessage')
const signinUpText = document.querySelector('#signin-upButtonTxt')
warning.style.display = "none"
otp.style.display = 'none'

username.style.display = "none"

submitButton.onclick = login
warningCloseBtn.onclick = closeWarning
forgetPassBtn.onclick = forgetPassword
signinUPButton.onclick = signup

//loading button

function loadingButton() {
    if (submitButton.classList.contains('button--loading')) {
        submitButton.classList.remove('button--loading')
        submitButton.disabled = false
    } else {
        submitButton.classList.add('button--loading')
        submitButton.disabled = true
    }
}

//display warining message
function warningFunction(message) {
    warningMessage.innerText = message
    warning.style.display = 'block'
    setTimeout(function () {
        warning.style.animation = 'fade-out 0.3s ease-in-out';
        setTimeout(function () {
            warning.style.display = 'none';
            warning.style.animation = '';
        }, 300);
    }, 3000);


}
//close warining message
function closeWarning() {
    warning.style.display = "none"
}

//validate input
function inputValidation() {
    var nameValue = document.querySelector('input[name="username"]').value
    var emailValue = document.querySelector('input[name="email"]').value
    var passwordValue = document.querySelector('input[name="password"]').value
    var otpValue = document.querySelector('input[name="OTP"]').value

    if (nameValue == "" && username.offsetParent !== null) {
        warning.style.backgroundColor = "#ff9800"
        warningFunction("Please provide username")
        return false
    } else if (emailValue == "" && email.offsetParent !== null) {
        warning.style.backgroundColor = "#2196F3"
        warningFunction('please provide email address')
        return false
    } else if (passwordValue == "" && password.offsetParent !== null) {
        warning.style.backgroundColor = "#f44336"
        warningFunction('please provide password')
        return false
    } else if (otpValue == '' && otp.offsetParent !== null) {
        warning.style.backgroundColor = '#f44336'
        warningFunction('Please Provide OTP')
    }
    else {
        return true
    }
}
function login() {
    if (inputValidation()) {
        const formEl = document.querySelector('#form')
        let formData = new FormData()

        formData.append('username', document.querySelector('input[name="email"]').value)
        formData.append('password', document.querySelector('input[name="password"]').value)
        loginData = new URLSearchParams(formData)
        loadingButton()
        fetch(`http://${location.host}/login`, {
            method: 'POST',
            body: loginData
        }).then(res => res.json()).then(data => {
            if (data.access_token) {
                localStorage.setItem('token', data.access_token)
                loadingButton()
                window.location.href(`http://${location.host}/`)
            } else {
                warningFunction('envalid Email and password')
                loadingButton()
            }

        }).catch(error => console.log(error))

    }
}

//Nevigate to forget password
function forgetPassword() {
    header.innerText = 'Forget Password?'
    password.style.display = 'none'
    forgetPassBtn.style.display = 'none'
    submitButtonText.innerText = 'Next'
    submitButton.onclick = function () {
        sendOTP()
        submitButton.onclick = function () {
            password.style.display = 'block'
            submitButton.onclick = resetPassword
            signin()
        }
    }
}

//Nevigate to signup
function signup() {
    header.innerText = 'Create Account'
    signinUpMessage.innerText = "Already have an account?"
    signinUpText.innerText = 'Signin'
    username.style.display = 'block'
    forgetPassBtn.style.display = 'none'
    submitButtonText.innerText = "Next"
    signinUPButton.onclick = function(){
        signin()
    }
    submitButton.onclick = function () {
        sendOTP()
        submitButton.onclick = createAccount
    }

}

//nevigate to sigin
function signin() {
    header.innerText = 'Login'
    signinUpMessage.innerText = "Don't have an account?"
    signinUpText.innerText = 'Signup'
    username.style.display = 'none'
    submitButton.onclick = login
    signinUPButton.onclick = signup

}

//send email to server for OTP
function sendOTP() {
    if (inputValidation()) {
        const emailData = {
            email: document.querySelector('input[name="email"]').value
        }
        loadingButton()
        fetch(`http://${location.host}/users/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(emailData)
        }).then(res => {
            if (res.status == 500) {
                warningFunction('Something went wrong, please try again!!')
                loadingButton()
            } else if (res.status == 422) {
                warningFunction('Invalid email')
                loadingButton()
            } else if (res.status == 202) {
                warningFunction("check out email for OTP")
                username.style.display = "none"
                email.style.display = "none"
                password.style.display = "none"
                otp.style.display = "block"
                loadingButton()

            }

        }).catch(error => console.log(error))

    }

}

function createAccount() {
    if (inputValidation()) {
        const userData = {
            user_name: document.querySelector('input[name="username"]').value,
            email: document.querySelector('input[name="email"]').value,
            password: document.querySelector('input[name="password"]').value,
            otp: document.querySelector('input[name="OTP"]').value
        }
        loadingButton()
        fetch(`http://${location.host}/users`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        }).then(res => {
            if (res.status == 409) {
                warningFunction('User with email already exist')
                loadingButton()
            } else if (res.status == 201) {
                warningFunction('User has been created')
                submitButtonText.innerText = "Login"
                submitButton.onclick = signin
                loadingButton()
            } else {
                warningFunction('Invalid OTP')
                loadingButton()
            }
        })
        console.log(userData)
    }
}
function resetPassword() {
    if (inputValidation) {
        const passwordData = {
            email: document.querySelector('input[name="email"]').value,
            new_password: document.querySelector('input[name="password"]').value,
            otp: document.querySelector('input[name="OTP"]').value,

        }
        fetch(`http://${location.host}/forget`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(passwordData)
        }).then(res => {
            if (res.status == 409) {
                warningFunction('Email does not fornd')
            } else if (res.status == 200) {
                signin()
                return res.json()
            } else {
                warningFunction('Ivalid Credential')
            }
        }).then(data => {
            warningFunction(`Welcome back ${data.user_name}`)
        })
            .catch(error => console.log(error))
    }
}