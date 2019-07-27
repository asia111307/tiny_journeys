// FIXED SIDEBAR
const sidebar = document.getElementsByClassName('sidebar')[0];
if (sidebar) {
    const sidebarTop = sidebar.getBoundingClientRect().top - document.body.getBoundingClientRect().top;
    window.addEventListener('scroll', function() {
        if (sidebarTop - document.documentElement.scrollTop <= 100  ){
            sidebar.style.position = 'fixed';
            sidebar.style.top = '60px';
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

window.addEventListener('resize', function() {
    const current_window_width = window.innerWidth;
    if ((current_window_width >= 880 && !document.getElementById('nav-icon1').classList.contains('open')) ||
        (current_window_width <= 880 && document.getElementById('nav-icon1').classList.contains('open'))) {
        document.getElementById('nav-icon1').click();
    }
});
document.getElementById('nav-icon1').click();
document.getElementById('nav-icon1').click();



// COMMENT BLOCK SECTION OPENING
const comments_headers = document.getElementsByClassName('comments-header');
const single_post = document.getElementsByClassName('single-post')[0];

function toggleOpenContentComments() {
    const comment_header = this;
    const arrow = comment_header.firstChild.nextElementSibling;
    const comment_content = comment_header.nextElementSibling;

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

if (comments_headers) {
    for (let i=0; i<comments_headers.length; i++){
        comments_headers[i].addEventListener('click', toggleOpenContentComments);
    }
}

if (single_post) {
    for (let i=0; i<comments_headers.length; i++){
        comments_headers[i].click();
    }
    lightbox.option({
      'wrapAround': true
    });
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


// DEACTIVATE IMAGE LINKS ON HOME
if (!single_post) {
    links = document.getElementsByName('image-a');
    if (links) {
        for (let i=0; i< links.length; i++) {
            links[i].href = "javascript:void(0)";
            links[i].style.cursor = 'default';
        }
    }
}


// WHEN THERE IS N0 CONTENT
const section_style = document.getElementsByClassName('section-style')[0];
const no_content = document.getElementsByClassName('no-content')[0];
if (no_content) {
    section_style.style.height = '100vh';
}

