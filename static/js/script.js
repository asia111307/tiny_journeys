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
    console.log(posts[i]);
}