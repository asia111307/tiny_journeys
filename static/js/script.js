// COMMENT BLOCK SECTION OPENING ----------------
const arrow = document.getElementsByClassName('caret-icon-fa')[0];
const comment_content = document.getElementsByClassName('visible-post-comments-content')[0];
const comments = document.getElementsByClassName('comment');
const posts = document.getElementsByClassName('view_post');
function toggleOpenContent() {
    if (arrow.classList.contains('open')) {
        comment_content.style.display = 'none';
        arrow.classList.remove('fa-caret-up');
        arrow.classList.add('fa-caret-down');
        arrow.classList.remove('open');
    } else {
        comment_content.style.display = 'block';
        arrow.classList.remove('fa-caret-down');
        arrow.classList.add('fa-caret-up');
        arrow.classList.add('open');
    }
}
if (arrow) {
    arrow.addEventListener('click', toggleOpenContent);
}
if (comments.length) {
    arrow.click();
}
if (posts) {
    for (var i=0; i< posts.length; i+=2) {
        posts[i].style.backgroundColor = 'rgba(0, 0, 0, 0.05)';
    }
}



// TITLE ANIMATION -------------------
const titleAnm = document.querySelector(".title-anm");
const cursor = document.querySelector(".cursor");
const title = "Tiny Journeys";
const description = document.querySelector(".small-jumb p");
const descWord = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.";
let letterNumber = 0;
const animation = () => {
    titleAnm.textContent += title[letterNumber++];
    if (letterNumber === title.length){
        clearInterval(anmInt);
        document.querySelector(".underline").style.opacity = "1";
        letterNumber = 0;
        setTimeout(()=>{
            const anmDes = setInterval(()=>{
                description.textContent += descWord[letterNumber++];
                if (letterNumber === descWord.length) {
                    clearInterval(anmDes);
                    letterNumber = 0;
                }
            },80);
        },1500)
    }
};


// CURSOR ANIMATION------------------------------------
const jumb_video = document.querySelector(".jumb-video");
const anmInt = setInterval(animation, 250);
const cursorAnimation = () => {
    cursor.classList.toggle("cursor-hide");
};
if (jumb_video) {
    setInterval(cursorAnimation, 500);
    jumb_video.addEventListener("loadedmetadata", function (){
            this.currentTime = 27;
        }, false
    );
}



// TRIP TIMER ---------------------
const trip = new Date("2019-08-11 04:00:00").getTime();

const day = document.querySelector('.days');
const hour = document.querySelector('.hours');
const minute = document.querySelector('.minutes');
const second = document.querySelector('.seconds');

const tripTimer = () => {
    const today = new Date().getTime();

    let days = Math.floor((trip / (1000 * 60 * 60 * 24)) - (today / (1000 * 60 * 60 * 24)));
    days = days < 10 ? `0${days}` : days;

    let hours = Math.floor((trip / (1000 * 60 * 60)) - today / (1000 * 60 * 60)) % 24;
    hours = hours < 10 ? `0${hours}` : hours;

    let minutes = Math.floor(trip / (1000 * 60) - today / (1000 * 60)) % 60;
    minutes = minutes < 10 ? `0${minutes}` : minutes;

    let seconds = Math.floor(trip / 1000 - today / 1000) % 60;
    seconds = seconds < 10 ? `0${seconds}` : seconds;

    day.textContent = days;
    hour.textContent = hours;
    minute.textContent = minutes;
    second.textContent = seconds;
};
if (day && hour && minute && second) {
    tripTimer();
    setInterval(tripTimer,1000);
}
