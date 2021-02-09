// SIGN UP API
$(function(){
    $('#signup_submit').on('click', function (e) {
        e.preventDefault();
        
        let firstname = document.getElementById("firstname").value;
        let lastname = document.getElementById("lastname").value;
        let email = document.getElementById("email").value;
        let phonenumber = document.getElementById("phonenumber").value;
        let password = document.getElementById("password").value;
        let address = document.getElementById("address").value;
        let council = document.getElementById("council").value;
        let state = document.getElementById("state").value;
        let country = document.getElementById("country").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        $.ajax({
            url:'/signup_api',
            type:'POST',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                firstname: firstname,
                lastname: lastname,
                email: email,
                phonenumber: phonenumber,
                password: password,
                address: address,
                council: council,
                state: state,
                country: country
            },
            success:function(response){
                document.getElementById("spinner").style.display = "none";
                if(response.error == true){
                    document.getElementById('server_message_error').innerHTML = response.message;
                    document.getElementById("server_message_error").style.display = "block";
                    setTimeout(function(){ 
                        document.getElementById("server_message_error").style.display = "none"; 
                    }, 3000);
                }
                else{
                    document.getElementById('server_message_success').innerHTML = response.message;
                    document.getElementById("server_message_success").style.display = "block";
                    setTimeout(function(){ 
                        document.getElementById("server_message_success").style.display = "none"; 
                    }, 3000);
                }
                console.log(response);
            },
            error:function(e){
                console.log(e);
            },
        });
        
        
    });
});
// UPDATE ACCOUNT DATA API
$(function(){
    $('#account_modal_submit').on('click', function (e) {
        e.preventDefault();
        let account_name = document.getElementById("account_name").value;
        let account_number = document.getElementById("account_number").value;
        let bank = document.getElementById("bank").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        
        $.ajax({
            url:'/update_account',
            type:'PUT',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                account_name: account_name,
                account_number: account_number,
                bank: bank
            },
            success:function(response){
                console.log(response);
                $('#modal_message_account').text(response.message);
                if(response.error == true){
                    document.getElementById("modal_message_account").classList.add('text-danger');
                    $('.account-data-submit').trigger("reset");
                }
                else{
                    document.getElementById("modal_message_account").classList.add('text-success');
                    $('.account-data-submit').trigger("reset");
                }
                $('.account-data-submit').trigger("reset");
                $('#accountModal').modal('show');
            },
            error:function(e){
                console.log(e);
                // $('#modal_message_account').text(e);
                $('.account-data-submit').trigger("reset");
                $('#modal_message_account').text("Sorry, an error occured!");
                document.getElementById("modal_message_account").classList.add('text-danger');
            },
        });
        
        
    });
});

// CLOSE FUNCTION FOR password update MODAL
$(function(){
    $('#close-password').on('click', function (e) {
        e.preventDefault();
        $('#modal_message_account').text(" ");
        $('#accountModal').modal('hide');
        document.getElementById("account-modal-form").reset();
    });
});


// UPDATE PASSWORD API
$(function(){
    $('.password-data-submit').on('click', function (e) {
        e.preventDefault();
        var token = document.getElementById("token").value;
        var old_password = document.getElementById("update_old_password").value;
        var new_password = document.getElementById("update_new_password").value;
        var confirm_new_password = document.getElementById("update_confirm_new_password").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        if (new_password != confirm_new_password) { 
            $('#password_confirm').text("new password not the same!");
         }
         else{
            $.ajax({
                url:'https://agrilance.herokuapp.com/api/v1/update_password?token='+token,
                type:'PUT',
                data:{
                    old_password: old_password,
                    new_password: new_password,
                },
                success:function(response){
                    console.log(response);
                    $('#modal_message_password').text(response.message);
                    document.getElementById("form-edit-password").classList.add('hide');
                    
                    $('.password-data-submit').trigger("reset");
                    $('#updatePasswordModal').modal('show');
                },
                error:function(e){
                    console.log(e);
                    $('#modal_message_password').text("Sorry, an error occured!");
                },
            });
        }
        
        
    });
});
