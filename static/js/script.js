// FIXED SIDEBAR
const sidebar = $('.sidebar')[0];
if (sidebar) {
    const sidebarTop = sidebar.getBoundingClientRect().top - document.body.getBoundingClientRect().top;
    $(window).on('scroll', function() {
        if (sidebarTop - document.documentElement.scrollTop <= 100  ){
            $(sidebar).addClass('fixed');
        } else {
            $(sidebar).removeClass('fixed');
        }
    });
}



// HAMBURGER MENU
$('#nav-icon1').on('click', function() {
  this.toggleClass('open');
  const menu_items = $('.nav-hidden');
  const menu = this;
  for (let i=0; i< menu_items.length; i++) {
      if (menu.hasClass('open')) {
          menu_items[i].css('display', 'flex');
      } else {
          menu_items[i].css('display', 'none');
      }
  }
});

$(window).on('resize', function() {
    const current_window_width = $(window).innerWidth;
    if ((current_window_width >= 880 && !$('#nav-icon1').hasClass('open')) ||
        (current_window_width <= 880 && $('#nav-icon1').hasClass('open'))) {
        $('#nav-icon1').click();
    }
});

const current_window_width = $(window).innerWidth;
if (current_window_width <= 880) {
    $('#nav-icon1').click();
    $('#nav-icon1').click();
}



const single_post = $('.single-post')[0];



// DEACTIVATE IMAGE LINKS ON HOME
if (!single_post) {
    console.log('np post');
    const links = $('a[name="image-a"]');
    if (links) {
        for (let i=0; i< links.length; i++) {
            links[i].href = "javascript:void(0)";
            links[i].style.cursor = 'default';
        }
    }
}



// COMMENT BLOCK SECTION OPENING
const comments_header = $('.comments-header')[0];

function toggleOpenContentComments(header) {
    const comment_header = $(header);
    const arrow = comment_header.find(".caret-icon-fa");
    const comment_content = comment_header.next();

    if (arrow.hasClass('open')) {
        comment_content.css('display', 'none');
        arrow.removeClass('fa-caret-up');
        arrow.addClass('fa-caret-down');
        arrow.removeClass('open');
    } else {
        comment_content.css('display', 'block');
        arrow.removeClass('fa-caret-down');
        arrow.addClass('fa-caret-up');
        arrow.addClass('open');
    }
}

if (single_post) {
        comments_header.click()
    }

// ADD COMMENTS
function addComment(post_id) {
    const class_comment = `comments-form-${post_id}`;
    const data = $(`.${class_comment}`).serialize();
    $.ajax({
			url: `/comment/add/${post_id}`,
			data: data,
			type: 'POST',
			success: function(response){
				const class_comment_block = `.comment-block-${post_id}`;
				$(class_comment_block).html(response);
				const comments_header = `.comments-header-${post_id}`;
				$(comments_header)[0].click();
			},
			error: function(error){
				console.log(error);
			}
		});


}


// DELETE COMMENTS
function deleteComment(post_id, comment_id) {
    const class_comment_block = `.comment-block-${post_id}`;
    $(class_comment_block).load(`/admin/delete/comment/${post_id}/${comment_id}`);
}


// LIKES CLICK
function processClick(type, post_id, user_id) {
    const class_post = `.like-block-${post_id}`;
    $(class_post).load(`/post/${type}/${user_id}/${post_id}`);
}



// LIST OF POSTS BACKGROUND CHANGE
const posts = $('.view_post');
if (posts) {
    for (var i=0; i< posts.length; i+=2) {
        posts[i].css('backgroundColor', 'rgba(0, 0, 0, 0.05)');
    }
}



// TITLE & CURSOR ANIMATION
const home = $('.home-feed');
if (home) {
    const titleAnm = $(".title-anm");
    const cursor = $(".cursor");
    const title = "Tiny Journeys";
    const description = $(".small-jumb p");
    const descWord = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor.";
    let letterNumber = 0;
    const animation = () => {
        titleAnm.textContent += title[letterNumber++];
        if (letterNumber === title.length){
            clearInterval(anmInt);
            $(".underline").css('opacity', "1");
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
    const jumb_video = $(".jumb-video");
    const anmInt = setInterval(animation, 250);
    const cursorAnimation = () => {
        cursor.toggleClass("cursor-hide");
    };
    if (jumb_video) {
        setInterval(cursorAnimation, 500);
        jumb_video.on("loadedmetadata", function (){
                this.currentTime = 27;
            }, false
        );
    }
}




//  N0 CONTENT HEIGHT ADJUSTMENT
const section_style = $('.section-style')[0];
const no_content = $('.no-content')[0];
if (no_content) {
    section_style.css('height', '100vh');
}
