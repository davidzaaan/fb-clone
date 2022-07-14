console.log("Hello Friends!");

/************* Function that retrieves the CSRF token ****************/
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
/***************** End of function that retrieves the CSRF token **********************/


const addFriend = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/add_fr/${userId}/${friendId}/`;
    const addFriendButton = document.querySelector(`#add_fr_btn_${friendId}`);

    let csrfToken = getCSRFToken(document.cookie);

    // Init object parameter to fetch function
    const init = {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': `${csrfToken}`
        },
    };

    if (addFriendButton.innerText === "Cancel friend request") {
        undoFriendRequest(addFriendButton, csrfToken, friendId, userId);
        return;
    }

    fetch(resourceLink, init)
        .then(response => response.json())
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);
            // Updating the add friend button
            addFriendButton.innerText = "Cancel friend request";
            addFriendButton.style.backgroundColor = "#555";
        });
}



const deleteFriend = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/remove_friend/${userId}/${friendId}/`;

    let csrfToken = getCSRFToken(document.cookie);

    let addToCFButton = document.querySelector(`#add_to_cf_${friendId}`);

    let removeFriendButton = document.querySelector(`#remove_friend_${friendId}`);

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);

            removeFriendButton.innerText = "Deleted";
            addToCFButton.style.display = "none";
        });

}


const undoFriendRequest = (addFriendButton, csrfToken, friendIdToRemoveFromFR, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/undo_fr/${userId}/${friendIdToRemoveFromFR}/`;

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);
            // Updating the add friend button
            addFriendButton.innerText = "Add friend";
            addFriendButton.style.backgroundColor = "#0D6EFD";
        });
}


const acceptFR = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/accept_fr/${userId}/${friendId}/`;

    let csrfToken = getCSRFToken(document.cookie);

    const acceptFRBtn = document.querySelector(`#accept_fr_btn_${friendId}`);

    const deleteFRBtn = document.querySelector(`#delete_fr_btn_${friendId}`);

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);

            acceptFRBtn.innerText = "Friends";
            deleteFRBtn.style.display = "none";
        });
}


const deleteFR = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/delete_fr/${userId}/${friendId}/`;

    let csrfToken = getCSRFToken(document.cookie);

    const acceptFRBtn = document.querySelector(`#accept_fr_btn_${friendId}`);

    const deleteFRBtn = document.querySelector(`#delete_fr_btn_${friendId}`);

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);

            deleteFRBtn.innerText = "Deleted";
            acceptFRBtn.style.display = "none";
        });

}



const addFriendToCloseFriends = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/add_to_cf/${userId}/${friendId}/`;

    let csrfToken = getCSRFToken(document.cookie);

    let addToCFButton = document.querySelector(`#add_to_cf_${friendId}`);

    let removeFriendButton = document.querySelector(`#remove_friend_${friendId}`);

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);

            addToCFButton.innerText = "Added to close friends";
            removeFriendButton.style.display = "none";
        });

}



const removeFriendFromCloseFriends = (friendId, userId) => {
    let resourceLink = `http://localhost:8000/api/friends/remove_from_cf/${userId}/${friendId}/`;

    let csrfToken = getCSRFToken(document.cookie);

    let deleteFriendFromCFButton = document.querySelector(`#remove_from_closefriends_${friendId}`);

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
        .catch(error => {
            console.log(error);
        })
        .then(data => {
            console.log(data);

            deleteFriendFromCFButton.innerText = "Removed";
        });

}