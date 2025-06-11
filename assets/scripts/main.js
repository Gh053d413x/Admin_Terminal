// get dialogue element
// const dialog = document.querySelector('.my-dialog')
// const dialog = document.querySelector('dialog.my-dialog')
// const dialog = document.getElementsByClassName('my-dialog')
// const dialog = document.querySelector('#my-dialog')
// const dialog = document.querySelector('dialog#my-dialog')
// const dialog = document.getElementsByClassName('my-dialog')

const splashes = [
    'Welcome to my website!',
    'Thanks for visiting!',
    'Rate it 5 stars!',
    'Where are my skills again?',
    'NO WAY!',
    'I am a web developer!',
    'OOPS',
    'JavaScript is pretty cool!',
    '<love class="HTML" id="And">Coding in General!</love>',
    'const programmer = "Web Developer";',
    'Error: NULL Pointer Exception',
    'Error: Array Index Out of Bounds Exception',
    'Error: Stack Overflow Exception',
    'Error: Out of Memory Exception',
    'Error: Class Not Found Exception',
    'Error: No Class Def Found Error',
    'Error: No Such Method Error',
    'Error: No Such Field Error',
    'Error: No Such Element Exception',
    'Error: Bug Forbidden',
    'Error: Bug Not Fixed',
    'Error: Bug Not Found',
    'Error: Bug Not Reproducible',
    'Error: Bug Not Reported',
    'Error: Bug Detected',
    'Info: Bug Reported',
    'Info: Bug Fixed',
    'Info: Bug Reproducible',
    'YIKES! My project is broken!',
    'YIKES! My project is not working!',
    'YIKES! My project is not working at all!',
    'YIKES! Where did my projects go?',
    'I am not a web developer! I am a software engineer!',
]

const msg_warning = `
 ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄   ▄ 
▐░░░░░░░░░░░▌ ▐░░░░░░░░░░░▌ ▐░░░░░░░░░░░▌ ▐░░░░░░░░░░░▌ ▐░▌
▐░█▀▀▀▀▀▀▀▀▀   ▀▀▀▀█░█▀▀▀▀  ▐░█▀▀▀▀▀▀▀█░▌ ▐░█▀▀▀▀▀▀▀█░▌ ▐░▌
▐░▌                ▐░▌      ▐░▌       ▐░▌ ▐░▌       ▐░▌ ▐░▌
▐░█▄▄▄▄▄▄▄▄▄       ▐░▌      ▐░▌       ▐░▌ ▐░█▄▄▄▄▄▄▄█░▌ ▐░▌
▐░░░░░░░░░░░▌      ▐░▌      ▐░▌       ▐░▌ ▐░░░░░░░░░░░▌ ▐░▌
 ▀▀▀▀▀▀▀▀▀█░▌      ▐░▌      ▐░▌       ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀  ▐░▌
          ▐░▌      ▐░▌      ▐░▌       ▐░▌ ▐░▌            ▀ 
 ▄▄▄▄▄▄▄▄▄█░▌      ▐░▌      ▐░█▄▄▄▄▄▄▄█░▌ ▐░▌            ▄ 
▐░░░░░░░░░░░▌      ▐░▌      ▐░░░░░░░░░░░▌ ▐░▌           ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀        ▀        ▀▀▀▀▀▀▀▀▀▀▀   ▀             ▀ 
`

const navBar = document.querySelector('#navBar')
const darkmode = document.getElementById('darkmode')
const confirmation = document.getElementById('confirmation')
const html = document.querySelector('html')

const counter = document.getElementById('timer')

const splash_text = document.getElementById('splash-text').innerText = splashes[Math.floor(Math.random() * splashes.length)]
const display_dependent = document.getElementById('display-dependent').style.display = 'block'

console.log("Splash Text: " + splash_text)
console.log("Navigation Bar Check:");
console.log(navBar)

function set_admin() {
    window.location.href = 'admin.html'
}

// Contact
const showContactLink = document.querySelector('a#contact');
const contactDialog = document.querySelector('dialog#contact');
const closeContactButton = document.querySelector('button#closeContact');

console.log()
console.log("Contact Dialog Check:")
console.log(contactDialog)

console.log(msg_warning)
console.log("You are in the console!\nDo not enter any commands someone else has given you!\nIf you do, you might get hacked!\n Enter commands only if you know what they do and that they are safe and trusted!\n\n")

showContactLink.addEventListener('click', () => {
    contactDialog.showModal();
});
closeContactButton.addEventListener('click', () => {
    contactDialog.close();
})

// This is other code that is not related to the above code

function startCountdown(duration) {
    let timer = duration, minutes, seconds;
    console.log('Timer Started for ' + duration + ' seconds!')
    let countdownInterval = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? '0' + minutes : minutes;
        seconds = seconds < 10 ? '0' + seconds : seconds;

        counter.innerText = minutes + ' : ' + seconds

        if (--timer < 0) {
            clearInterval(countdownInterval);
            console.log('TIMES UP!');
            counter.innerText = 'TIMES UP!'
        }
    }, 1000);
}

// Backend code is in backend.js