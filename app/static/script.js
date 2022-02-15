$(document).ready(function(){

      // GLOBLE VARIABLES
      var currentUserID = NaN;
      var chattingFriendID = NaN;
      var socketList = new Array();
    
    // SCRIPT TO CREATE CSRF_TOKEN IN EXTERNAL JAVASCRIPT FILE.
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    $("#msg-input-div").hide();
    // FUNCTION TO VALIDATE NAME
    function validateName(name) {
        var regex = /^[a-zA-Z ]{2,60}$/;
        if(regex.test(name)){
            return true
        }else{
            alert("Name: only alphabet with space allowed max limit 60.");
            return false
        }
    }

    // FUNCTION TO VALIDATE PASSWORD
    function validatePassword(password) {
        var regex=  /^[0-9A-Za-z]\w{6,10}$/;
        if(regex.test(password)){
            return true;
        }else{
            alert("Password: min 6 max 10 alphanumeric.");
            return false
        }
    }

    // FUNCTION TO VALIDATE EMAIL
    function validateEmail(email) {
        const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(regex.test(String(email).toLowerCase())){
            return true;
        }else{
            alert("email: please write valid email");
            return false
        }
    }

    // FUNCTION TO VALIDATE DATE OF BIRTH
    function validateDOB(dob) {
        var today = new Date();
        month = '' + (today.getMonth() + 1),
        day = '' + today.getDate(),
        year = today.getFullYear();

        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
        
        today = [year, month, day].join('-');
        today = Date.parse(today)
        dob= Date.parse(dob)
        
        if(dob<=today){
            return true;
        }else{
            alert("DOB: can not be future date or empty");
            return false
        }
    };

    // FUNCTION TO VALIDATE CONTACT NUMBER
    function validateContactNumber(contactNumber){
        var regex = /^\d{10}$/;
        if (regex.test(contactNumber)){
            return true
        }else{
            alert("Mobile no: should be of 10 digit.");
            return false
        }
    }

    // SCRIPT FOR REGISTERATION.
    $("#register-submit-btn").click(function(event){
        if(validateName($("#name").val()) && 
        validateEmail($("#email").val()) && 
        validatePassword($("#password").val()) &&
        validateDOB($("#dob").val()) &&
        validateContactNumber($("#contact-number").val())){
            $("#registration-form").submit();     
        }
    });

    // SCRIPT FOR LOGIN.
    $("#login-submit-btn").click(function(event){
        if(validateEmail($("#email").val()) && validatePassword($("#password").val())){ 
            $("#login-form").submit();  
        }
    });
    
    var chatSocket = Array()
    $(".friend").click(function(event){
        $("#chat-log-homepage").remove();
        $("#msg-input-div").show();
        currentUserID =  $('#user-id').data().name;
        if (chattingFriendID==NaN){
            $("#"+event.target.id).css({"border-radius":"30px;","border-top-right-radius":"0px","border-bottom-right-radius":"0px;", "margin-right":"0px"});
            chattingFriendID=event.target.id

        }else{
            $("#"+chattingFriendID).css({"border-radius":"10px"});
            $("#"+event.target.id).css({"border-radius":"30px", "border-top-right-radius":"0px","border-bottom-right-radius":"0px"});
            chattingFriendID=event.target.id
        }    
        chattingFriendID = event.target.id;
        roomName = chattingFriendID>currentUserID?String(chattingFriendID)+String(currentUserID):String(currentUserID)+String(chattingFriendID);

        if(jQuery.inArray(roomName, socketList)==-1){
            
            // CREATING SOCKET
              if (window.location.protocol == "https:") {
                        chatSocket = new WebSocket('wss://'+window.location.host+'/wss/app/'+roomName+'/');
                  } else {
                        chatSocket = new WebSocket('ws://'+window.location.host+'/ws/app/'+roomName+'/');
                  };
            socketList.push(roomName)
        }

        chatSocket.onmessage=function(e) {
            const data = JSON.parse(e.data);
            if(data.message){
                if(Number(data.message_sender_id)==Number(currentUserID)){
                    $("#chat-log").append("<div class='row-lg reply-box'><label class='alert alert-success float-end user-text-reply'>"+data.message+"</label></div><br>");
                    
                }else{
                    $("#chat-log").append("<div class='row-lg reply-box'><label class='alert alert-primary float-start friend-text-reply'>"+data.message+"</label></div><br>");
                }
                $("#chat-log").animate({ scrollTop: $("#chat-box-body").prop('scrollHeight')},10);// 10 is delay time of scroll.
            }
        }
        
        chatSocket.onclose = function(e){
            console.error("Chat socket closed unexpectedly");
            socketList.pop(roomName)
        }

        $.ajax({
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            method: "post",
            url: window.location.href,
            dataType: "json",
            data: {
                message_receiver_id:chattingFriendID
            },
            success:function(chat_history){
                // chat_history=JSON.parse(chat_history);
                console.log(chat_history)
                // $("#chat-log").empty();

                // for(message of chat_history){

                //     if(Number(message.fields.user)==currentUserID){
                //         $("#chat-box-body").append("<div class='row-lg reply-box'><label class='alert alert-success float-end user-text-reply'>"+message.fields.message+"</label></div><br>");

                //     }else{
                //         $("#chat-box-body").append("<div class='row-lg reply-box'><label class='alert alert-success float-end friend-text-reply'>"+message.fields.message+"</label></div><br>");
                //     }
                // } $('#chat-log').animate({ scrollTop: $('#chat-box-body').prop('scrollHeight')},10);// 10 is delay time of scroll.
            },
            error:function(){
                alert("Unable to load chat history, refresh page and try again !");
            }   
        });
    }); 

    $("#chat-message-submit").click(function(e) {
        const message = $("#chat-message-input").val();
        chatSocket.send(JSON.stringify({
            'message': message,
            'message_sender_id':currentUserID,
            'message_receiver_id':chattingFriendID,
        }))
        $("#chat-message-input").val("");
    });
});
