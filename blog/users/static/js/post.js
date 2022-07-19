console.log('Hello post :)');

// // Textareas auto sizing
const commentTextArea = document.querySelectorAll(".comment_text");

/************************ Function that retrieves the CSRF token ************************/
function getCSRFToken(cookie) {
    if (!cookie.length > 0) {
        return null;
    }

    let csrf = cookie.split(";");

    for (let token of csrf) {
        if (token.trim().startsWith("csrf")) {
            return token.split("=")[1];
        }
    }
}
/************************ End of function that retrieves the CSRF token ************************/


/************************ Like post functionality ***********************/
function like(post_id, likedBy) {

    const resourceLink = `http://localhost:8000/api/posts/addlike/${post_id}/${likedBy}/`;
    let csrfToken = document.cookie;

    // Getting the post likes count element
    const likesCount = document.querySelector(`#likes__quantity_${post_id}`);

    // Interaction buttons
    const likeButton = document.querySelector(`#like__btn_${post_id}`);

    // Getting the post dislikes count element
    const dislikesCount = document.querySelector(`#dislikes__quantity_${post_id}`);

    // Interaction buttons
    const dislikeButton = document.querySelector(`#dislike__btn_${post_id}`);

    if (csrfToken) {
        // Parsing all the cookies to get the CSRF token
        csrfToken = getCSRFToken(document.cookie);
    }

    if (likeButton.innerText === "Liked") {
        removeLike(post_id, csrfToken, likesCount, likeButton, likedBy);
        return;
    }

    // Init object parameter to fetch function
    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`
        },
    };

    fetch(resourceLink, init)
        .then(response => response.json())
        .then(data => {
            // Updating the likes and dislikes count
            likesCount.innerText = data['likes'];
            dislikesCount.innerText = data['dislikes'];

            // Updating the dislike and like buttons
            likeButton.innerText = "Liked";
            dislikeButton.innerText = "Dislike";

            // Updating the dislike and like styling
            likeButton.style.color = "#2d85ff";
            dislikeButton.style.color = "inherit";
        });

}


function removeLike(post_id, csrfToken, likesCount, likeButton, likedBy) {
    const resourceLink = `http://localhost:8000/api/posts/remove_like/${post_id}/${likedBy}/`;

    // Init object parameter to fetch function
    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`
        },
    };

    fetch(resourceLink, init)
        .then(response => response.json())
        .then(data => {
            likesCount.innerText = data['likes'];
            likeButton.innerText = "Like";
            likeButton.style.color = "inherit";
        });
}
/************************ End of like post functionality ************************/

/************************ Dislike post functionality ***********************/
function dislike(post_id, dislikedById) {

    const resourceLink = `http://localhost:8000/api/posts/add_dislike/${post_id}/${dislikedById}/`;
    let csrfToken = document.cookie;

    // Getting the post likes count element
    const likesCount = document.querySelector(`#likes__quantity_${post_id}`);

    // Like button
    const likeButton = document.querySelector(`#like__btn_${post_id}`);

    // Getting the post dislikes count element
    const dislikesCount = document.querySelector(`#dislikes__quantity_${post_id}`);

    // Interaction buttons
    const dislikeButton = document.querySelector(`#dislike__btn_${post_id}`);


    if (csrfToken) {
        // Parsing all the cookies to get the CSRF token
        csrfToken = getCSRFToken(document.cookie);
    }

    if (dislikeButton.innerText === "Disliked") {
        removeDislike(post_id, csrfToken, dislikesCount, dislikeButton, dislikedById);
        return;
    }

    // Init object parameter to fetch function
    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`
        },
    };

    fetch(resourceLink, init)
        .then(response => response.json())
        .then(data => {
            // Updating the likes and dislikes count
            dislikesCount.innerText = data['dislikes'];
            likesCount.innerText = data['likes'];

            // Updating the dislike and like buttons
            dislikeButton.innerText = "Disliked";
            likeButton.innerText = "Like";

            // Updating the dislike and like styling
            dislikeButton.style.color = "#cc0001";
            likeButton.style.color = "inherit";
        });

}


function removeDislike(post_id, csrfToken, dislikesCount, dislikeButton, dislikedById) {
    const resourceLink = `http://localhost:8000/api/posts/remove_dislike/${post_id}/${dislikedById}/`;

    // Init object parameter to fetch function
    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`
        },
    };

    fetch(resourceLink, init)
        .then(response => response.json())
        .then(data => {
            dislikesCount.innerText = data['dislikes'];
            dislikeButton.innerText = "Dislike";
            dislikeButton.style.color = "inherit";
        });
}
/************************ End of dislike post functionality ************************/

// Comments box functionality
function commentBoxFocus(commentBoxId) {
    let commentBox = document.querySelector(`#${commentBoxId}`);
    commentBox.focus();
}




/************************ Comment was made functionality ************************/
function comment(postId, commentedById, commentContent) {
    const resourceLink = `http://localhost:8000/api/posts/comment/${postId}/${commentedById}/`;

    let commentQuantity = document.querySelector(`#comments__quantity_${postId}`);

    let csrfToken = getCSRFToken(document.cookie);

    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`,
        },
        body: JSON.stringify(commentContent)
    };

    fetch(resourceLink, init)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            commentQuantity.innerText = data['comments_quantity'];
            window.location.reload();
        });

}


if (commentTextArea.length > 0) {
    for (let i = 0; i < commentTextArea.length; i++) {

        commentTextArea[i].addEventListener("keyup", (event) => {

            commentTextArea[i].style.height = "40px";

            // Form submission
            if (event.key === "Enter" && !event.shiftKey) {
                let content = commentTextArea[i].value.trim();

                // Check that the comment box is not empty
                if (content !== "" && content !== "\n") {
                    console.log(content);
                    let postId = commentTextArea[i].dataset.postId;
                    let commentedBy = commentTextArea[i].dataset.commentedById;
                    comment(postId, commentedBy, content);
                }

                // Cleaning the comment box
                commentTextArea[i].value = "";
            }

            // Dynamic sizing of the comment box
            let scrollHeight = event.target.scrollHeight;
            commentTextArea[i].style.height = `${scrollHeight}px`;


        });
    }
}
/************************ End of comment made functionality ************************/