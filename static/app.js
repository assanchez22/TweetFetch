let tweets = document.querySelectorAll(".tweet");
let tweetIndex = 0;

setInterval(function() {

    tweets[tweetIndex].style.display = "none";

    tweetIndex++;

    if (tweetIndex >= tweets.length) {
        tweetIndex = 0;
        window.location.reload();
        
    }

    tweets[tweetIndex].style.display = "block";
}, 15000);