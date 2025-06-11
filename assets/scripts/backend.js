
function enter_command(){
    var argument = prompt('Command Pallete\nEnter a command\nExample: cd 10s\nAvailable Commands:\ncd - Countdown\nsetAdmin - Access the Admin Panel (Will Require A Password)\nEnter Command:')
    command(arg=argument)
}

function command(arg){
    if (arg != undefined){
        var command = arg
    }else{
        console.error('Please enter a valid command')
    }
    setTimeout(function (){
        if (command == 'test'){
            console.log('Test Command Ran')
        }else if (command == 'cd'){
            var time = Number(prompt('Enter Time:'))
            startCountdown(time)
        }else if (command == 'setAdmin'){
            window.location.href = 'admin.html'
        }else{
            console.error(`Invalid Command: ${command}, Please check if the command exists and that you have permission to use it`)
            alert(`Invalid Command: ${command}, Please check if the command exists and that you have permission to use it`)
        }
    }, 250)
}

function hover(element) {
    // Remove the unhighlighting class if it exists to allow hover to take over
    element.classList.remove('unhighlighting');
    // Your existing image change logic
    if (element.id === "download") {
        element.setAttribute('src', 'assets/images/download_highlighted.png'); // Assuming you have hovered images
    } else if (element.id === "about") {
        element.setAttribute('src', 'assets/images/about_highlighted.png');
    } else if (element.id === "changelog") {
        element.setAttribute('src', 'assets/images/changelog_highlighted.png');
    }
}

function unhover(element) {
    // Add the class to trigger the unhighlight animation
    element.classList.add('unhighlighting');

    // Listen for the end of the animation to clean up
    element.addEventListener('animationend', function handler() {
        element.classList.remove('unhighlighting');
        element.style.transform = 'scale(1)'; // Ensure it snaps back to scale(1) after animation
        element.removeEventListener('animationend', handler); // Remove the listener
    }, { once: true }); // Ensure the listener runs only once

    if (element.id === "download") {
        element.setAttribute('src', 'assets/images/download.png');
    } else if (element.id === "about") {
        element.setAttribute('src', 'assets/images/about.png');
    } else if (element.id === "changelog") {
        element.setAttribute('src', 'assets/images/changelog.png');
    } else {
        element.setAttribute('src', 'http://dummyimage.com/100x100/000/fff?text=Hovered');
    }
}

function click(element) {
    if (element.id === "download") {
        alert("Download button clicked! This would normally trigger a download action.");
    }
    else if (element.id === "about") {
        alert("About button clicked! This would normally show information about the application.");
    }
    else if (element.id === "changelog") {
        alert("Changelog button clicked! This would normally show the changelog of the application.");
    } else {
        element.setAttribute('src', 'http://dummyimage.com/100x100/f00/fff?text=Hovered');
    }
    element.setAttribute('src', 'http://dummyimage.com/100x100/000/fff');
}

const checkbox = document.getElementById('agree');
const button = document.getElementById('beta');

checkbox.addEventListener('change', function () {
    button.disabled = !this.checked;
});