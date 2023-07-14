var otp = document.getElementById('OTP')
var email = document.getElementById('email')
var newPassword = document.getElementById('newPassword')
var warning = document.querySelector('.warning')
const warningMessage = document.querySelector('#warningMessage')
const close = document.querySelector("#closeButton")

warning.style.display = "none"
newPassword.style.display = "none"
otp.style.display = "none"
const form_button = document.getElementById('input')

close.onclick = hidewarning;
form_button.onclick = showOtp;
//function to close to warning
function hidewarning() {
    warning.style.display = "none"
}
//function to sent otp to provided email
function showOtp() {
    const user = {
        email: document.querySelector('input[name="email"]').value,
    };
    fetch(`http://${location.host}/users/verify`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    }).then(res => {
        if (res.status === 500) {
            warningMessage.innerText = "server busy"
            warning.style.display = "block"

        }
        else if (res.status === 422) {
            warningMessage.innerText = "Invalid email"
            warning.style.display = "block"

        } else if (res.status === 202) {
            warningMessage.innerText = "OTP is sent to your email"
            otp.style.display = "block"
            newPassword.style.display = "block"
            form_button.setAttribute('value', "Submit")
            form_button.onclick = resetPassword
            return res.json();
        }
    }).catch(error => console.log(error))

}
function resetPassword() {
    const passwordData = {
        email: document.querySelector('input[name="email"]').value,
        new_password: document.querySelector('input[name="password"]').value,
        otp: document.querySelector('input[name="OTP"]').value,

    }
    console.log(passwordData)
    fetch(`http://${location.host}/forget`, {
        method: "PUT",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(passwordData)
    }).then(res => {
        return res.json()
    }).catch(error => console.log(error))
}