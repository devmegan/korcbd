function sendMail(contactForm) {
    $("#contactFormSubmitBtn").addClass("disabled").html("<i class='fas fa-circle-notch fa-spin'></i>");
    emailjs.send("gmail", "korcbdcontact", {
        "sender_name": contactForm.sender_name.value,
        "sender_email": contactForm.sender_email.value,
        "sender_phonenumber": contactForm.sender_phonenumber.value,
        "sender_message": contactForm.sender_message.value,
    })
    .then(
        function(response) {
            console.log("EmailJS SUCCESS", response);
            $("#contactFormFields").hide();
            $("#contactFormResponseHeader").text("Message Sent").show();
            $("#contactFormResponseBody").text("Thanks for your message. We'll be in touch as soon as possible!").show();
            $("#contactFormSubmitBtn").prop("type", "button").removeClass("kor-btn-hover disabled").addClass("btn-success").attr("data-dismiss","modal").html("<i class='fas fa-check'></i>");
        },
        function(error) {
            console.log("EmailJS FAILED", error);
            $("#contactFormFields").hide();
            $("#contactFormResponseHeader").text("Message Failed").show();
            $("#contactFormResponseBody").html("Sorry, it looks like somethings gone wrong there. Please send us an email at <b>korcbdproducts@gmail.com</b> and we'll be in touch as soon as possible.").show();
            $("#contactFormSubmitBtn").removeClass("kor-btn-hover disabled").addClass("btn-danger").attr("data-dismiss","modal").html("<i class='fas fa-exclamation-triangle'></i>");
        }
    );
    // prevent page reloading
    return false;
}

function initEmailJS() {
    emailjs.init("user_0BKHc2tjJuMjT7Ysz61mr");
}