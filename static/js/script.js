// FIXED SIDEBAR
const sidebar = document.getElementsByClassName('sidebar')[0];
if (sidebar) {
    const sidebarTop = sidebar.getBoundingClientRect().top - document.body.getBoundingClientRect().top;
    window.addEventListener('scroll', function() {
        if (sidebarTop - document.documentElement.scrollTop <= 100  ){
            sidebar.style.position = 'fixed';
            sidebar.style.top = '120px';
        } else {
            sidebar.style.position = 'static';
            sidebar.style.top = 'auto';
        }
    });
}



// HAMBURGER MENU
document.getElementById('nav-icon1').addEventListener('click', function() {
  this.classList.toggle('open');
  const menu_items = document.getElementsByClassName('nav-hidden');
  const menu = this;
  for (let i=0; i< menu_items.length; i++) {
      if (menu.classList.contains('open')) {
          menu_items[i].style.display = 'flex';
      } else {
          menu_items[i].style.display = 'none';
      }
  }
});

document.getElementById('nav-icon1').click();
const current_window_width = window.innerWidth;
if (current_window_width <= 880) {
    document.getElementById('nav-icon1').click();
    sidebar.style.position = 'static';
}



// COMMENT BLOCK SECTION OPENING
const arrows = document.getElementsByClassName('caret-icon-fa');
const comments = document.getElementsByClassName('comment');
const single_post = document.getElementsByClassName('single-post')[0];

function toggleOpenContent() {
    const arrow = this;
    const comment_content = arrow.parentElement.nextElementSibling;

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

if (arrows) {
    for (let i=0; i<arrows.length; i++){
        arrows[i].addEventListener('click', toggleOpenContent);
    }
}

if (single_post) {
    for (let i=0; i<arrows.length; i++){
        arrows[i].click();
    }
}



// LIST OF POSTS BACKGROUND CHANGE
const posts = document.getElementsByClassName('view_post');
if (posts) {
    for (var i=0; i< posts.length; i+=2) {
        posts[i].style.backgroundColor = 'rgba(0, 0, 0, 0.05)';
    }
}



// TITLE & CURSON ANIMATION
const home = document.getElementById('home-feed');
if (home) {
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
}
