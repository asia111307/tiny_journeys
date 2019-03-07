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
function scrollToSection() {
    var path = window.location.pathname;
    if (path !== '/') {
        document.getElementsByClassName('page-content')[0].scrollIntoView();
    }
}
scrollToSection();
if (arrow) {
    arrow.addEventListener('click', toggleOpenContent);
}
if (comments.length) {
    arrow.click();
}
for (var i=0; i< posts.length; i+=2) {
    posts[i].style.backgroundColor = 'rgba(0, 0, 0, 0.05)';
}
// TITLE ANIMATION -------------------
const titleAnm = document.querySelector(".title-anm");
const cursor = document.querySelector(".cursor");
const title = "Greece my Love";
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
const anmInt = setInterval(animation, 250);
const cursorAnimation = () => {
    cursor.classList.toggle("cursor-hide");
};
setInterval(cursorAnimation, 400);
document.querySelector(".jumb-video").addEventListener("loadedmetadata", function (){
        this.currentTime = 27;
    }, false
);

// let span = document.getElementsByClassName('.note-icon-caret');
// console.log(span);

// while (spans.length) {
//     spans[0].classList.remove('note-icon-caret');
// }