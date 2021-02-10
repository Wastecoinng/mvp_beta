// back page function for micropages
function goBack() {
    window.history.back();
  }


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
                        window.location.href = '/signin';
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
        document.getElementById("spinner").style.display = "block";
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
                document.getElementById("spinner").style.display = "none";
                console.log(response);
                $('#modal_message_account').text(response.message);
                if(response.error == true){
                    document.getElementById("modal_message_account").classList.add('text-danger');
                    document.getElementById("account-modal-form").style.display = "none"; 
                    $('.account-data-submit').trigger("reset");
                }
                else{
                    // document.getElementById("modal_message_account").classList.add('text-success');
                    document.getElementById("modal_message_account").style.color = "#fff"; 
                    $('.account-data-submit').trigger("reset");
                    document.getElementById("account-modal-form").style.display = "none"; 
                    document.getElementById("modal-bodii").style.margin = "auto"; 
                    document.getElementById("update_modal_icon").style.display = "block";
                    document.getElementById("modal-bodi").style.background = "linear-gradient(166.41deg, #14F0C8 30.11%, rgba(48, 193, 176, 0.9) 93.7%)";
                }
                $('.account-data-submit').trigger("reset");
                $('#accountModal').modal('show');
            },
            error:function(e){
                document.getElementById("spinner").style.display = "none";
                console.log(e);
                // $('#modal_message_account').text(e);
                $('.account-data-submit').trigger("reset");
                $('#modal_message_account').text("Sorry, an error occured!");
                document.getElementById("modal_message_account").classList.add('text-danger');
            },
        });
        
        
    });
});
// UPDATE BIO-DATA API
$(function(){
    $('#bio_modal_submit').on('click', function (e) {
        e.preventDefault();
        let update_first_name = document.getElementById("update_first_name").value;
        let update_last_name = document.getElementById("update_last_name").value;
        let update_email = document.getElementById("update_email").value;
        let update_phone = document.getElementById("update_phone").value;
        let update_address = document.getElementById("update_address").value;
        let update_council = document.getElementById("update_council").value;
        let update_state = document.getElementById("update_state").value;
        let update_country = document.getElementById("update_country").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        $.ajax({
            url:'/update_bio',
            type:'PUT',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                update_first_name: update_first_name,
                update_last_name: update_last_name,
                update_email: update_email,
                update_phone: update_phone,
                update_address: update_address,
                update_council: update_council,
                update_state: update_state,
                update_country: update_country
            },
            success:function(response){
                document.getElementById("spinner").style.display = "none";
                console.log(response);
                $('#modal_message_bio').text(response.message);
                if(response.error == true){
                    document.getElementById("modal_message_bio").classList.add('text-danger');
                    document.getElementById("bio-modal-form").style.display = "none"; 
                    $('.bio-data-submit').trigger("reset");
                }
                else{
                    // document.getElementById("modal_message_account").classList.add('text-success');
                    document.getElementById("modal_message_bio").style.color = "#fff"; 
                    $('.bio-data-submit').trigger("reset");
                    document.getElementById("bio-modal-form").style.display = "none"; 
                    document.getElementById("modal-bodii-bio").style.margin = "auto"; 
                    document.getElementById("update_modal_icon-bio").style.display = "block";
                    document.getElementById("modal-bodi-bio").style.background = "linear-gradient(166.41deg, #14F0C8 30.11%, rgba(48, 193, 176, 0.9) 93.7%)";
                }
                $('#bio_modal_submit').trigger("reset");
                $('#bioModal').modal('show');
            },
            error:function(e){
                document.getElementById("spinner").style.display = "none";
                console.log(e);
                // $('#modal_message_account').text(e);
                $('#bio_modal_submit').trigger("reset");
                $('#modal_message_bio').text("Sorry, an error occured!");
                document.getElementById("modal_message_bio").classList.add('text-danger');
            },
        });
        
        
    });
});

// CLOSE FUNCTION FOR password update MODAL
$(function(){
    $('#close-password').on('click', function (e) {
        e.preventDefault();
        $('#modal_message_account').text(" ");
        document.getElementById("account-modal-form").style.display = "block"; 
        document.getElementById("modal-bodii").style.margin = "0.5rem"; 
        document.getElementById("update_modal_icon").style.display = "none";
        document.getElementById("modal-bodi").style.background = "#fff";
        $('#accountModal').modal('hide');
        window.location.reload()
        document.getElementById("account-modal-form").reset();
    });
});

// UPDATE PASSWORD API
$(function(){
    $('#password_modal_submit').on('click', function (e) {
        e.preventDefault();
        // var token = document.getElementById("token").value;
        var old_password = document.getElementById("update_old_password").value;
        var new_password = document.getElementById("update_new_password").value;
        var confirm_new_password = document.getElementById("update_confirm_new_password").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        if (new_password != confirm_new_password) { 
            $('#password_confirm').text("new password not the same!");
         }
         else{
            $.ajax({
                url:'/update_password',
                type:'PUT',
                headers:{"X-CSRFToken": $crf_token},
                data:{
                    old_password: old_password,
                    new_password: new_password,
                },
                success:function(response){
                    document.getElementById("spinner").style.display = "none";
                    console.log(response);
                    $('#modal_message_password').text(response.message);
                    document.getElementById("modal_message_password").style.color = "#fff"; 
                    // document.getElementById("form-edit-password").classList.add('hide');
                    
                    $('#form-edit-password').trigger("reset");
                    document.getElementById("form-edit-password").style.display = "none"; 
                    document.getElementById("password-modal-bodii").style.margin = "auto"; 
                    document.getElementById("update_modal_icon_password").style.display = "block";
                    document.getElementById("modal-bodi-password").style.background = "linear-gradient(166.41deg, #14F0C8 30.11%, rgba(48, 193, 176, 0.9) 93.7%)";
                },
                error:function(e){
                    document.getElementById("spinner").style.display = "none";
                    console.log(e);
                    $('#modal_message_password').text("Sorry, an error occured!");
                    document.getElementById("form-edit-password").style.display = "none"; 
                },
            });
        }
        
        
    });
});


$(function(){
    $('#brand_submit').on('click', function (e) {
        e.preventDefault();
        console.log("hi! brand submit")
        let brand = document.getElementById("brand").value;
        let brand_code = document.getElementById("brand_code").value; 
        let category = document.getElementById("category").value; 
        let modal_message = document.getElementById("modal_message").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        $.ajax({
            url:'/brand_collector',
            type:'POST',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                brand_code: brand_code,
                brand: brand,
                category: category,
                modal_message:modal_message
            },
            success:function(response){
                document.getElementById("spinner").style.display = "none";
                console.log(response);
                // $('#modal_message_account').text(response.message);
                if(response.error == true){
                    document.getElementById("scan_result_manufacturer").classList.add('text-yellow');
                    document.getElementById("scan_result_manufacturer").innerHTML= response.message;
                    // document.getElementById("modal_message_account").classList.add('text-danger');
                    // $('.account-data-submit').trigger("reset");
                }
                if(response.error == false){
                    document.getElementById("scan_result_manufacturer").innerHTML= response.message;
                    // document.getElementById("scan_form").classList.add('hide');
                    document.getElementById("scan_form").style.display = "none"; 
                }

            },
            error:function(e){
                console.log(e);
                document.getElementById("spinner").style.display = "none";
                document.getElementById("scan_result_manufacturer").classList.add('text-danger');
                document.getElementById("scan_result_manufacturer").innerHTML= "Sorry, an error occured!";
            },
        });
        
        
    });
});

// CONTACT US API
$(function(){
    $('#contact_submit').on('click', function (e) {
        e.preventDefault();
        let contact_message = document.getElementById("contact_message").value;
        let contact_phone = document.getElementById("contact_phone").value;
        let contact_email = document.getElementById("contact_email").value;
        let contact_name = document.getElementById("contact_name").value;
        let ratings = document.getElementById("rating").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        $.ajax({
            url:'/contact_api',
            type:'POST',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                contact_message: contact_message,
                contact_phone: contact_phone,
                contact_email: contact_email,
                contact_name: contact_name,
                ratings: ratings
            },
            success:function(response){
                document.getElementById("spinner").style.display = "none";
                console.log(response);
                $('#modal_message_contact').text(response.message);
                if(response.error == true){
                    document.getElementById("modal_message_contact").classList.add('text-danger');
                    // document.getElementById("contact_form").style.display = "none"; 
                    $('.account-data-submit').trigger("reset");
                }
                else{
                    
                    // document.getElementById("modal_message_account").classList.add('text-success');
                    document.getElementById("modal_message_contact").style.color = "#fff"; 
                    $('.account-data-submit').trigger("reset");
                    // document.getElementById("contact_form").style.display = "none"; 
                    document.getElementById("modal-bodii-contact").style.margin = "auto"; 
                    document.getElementById("update_modal_icon_contact").style.display = "block";
                    document.getElementById("modal-bodi-contact").style.background = "linear-gradient(166.41deg, #14F0C8 30.11%, rgba(48, 193, 176, 0.9) 93.7%)";
                }
                $('#contact_submit').trigger("reset");
                $('#contactModal').modal('show');
            },
            error:function(e){
                document.getElementById("spinner").style.display = "none";
                console.log(e);
                $('#contactModal').modal('show');
                // $('#modal_message_account').text(e);
                $('contact_submit').trigger("reset");
                $('#modal_message_contact').text("Sorry, an error occured!");
                document.getElementById("modal_message_contact").classList.add('text-danger');
            },
        });
        
        
    });
});
// COllection confirmation US API
$(function(){
    $('#confirmation_submit').on('click', function (e) {
        e.preventDefault();
        let to_deliver = document.getElementById("r-to-deliver").value;
        let phone_number = document.getElementById("ajax_phone_number").value;
        let $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        document.getElementById("spinner").style.display = "block";
        $.ajax({
            url:'/confirmation_api',
            type:'POST',
            headers:{"X-CSRFToken": $crf_token},
            data:{
                to_deliver: to_deliver,
                phone_number: phone_number,
            },
            success:function(response){
                document.getElementById("spinner").style.display = "none";
                console.log(response);
                $('#modal_message_contact').text(response.message);
                if(response.error == true){
                    // document.getElementById("modal_message_contact").classList.add('text-danger');
                    // // document.getElementById("contact_form").style.display = "none"; 
                    // $('.account-data-submit').trigger("reset");
                }
                else{
                    
                    // // document.getElementById("modal_message_account").classList.add('text-success');
                    // document.getElementById("modal_message_contact").style.color = "#fff"; 
                    // $('.account-data-submit').trigger("reset");
                    // // document.getElementById("contact_form").style.display = "none"; 
                    // document.getElementById("modal-bodii-contact").style.margin = "auto"; 
                    // document.getElementById("update_modal_icon_contact").style.display = "block";
                    // document.getElementById("modal-bodi-contact").style.background = "linear-gradient(166.41deg, #14F0C8 30.11%, rgba(48, 193, 176, 0.9) 93.7%)";
                }
                // $('#contact_submit').trigger("reset");
                // $('#contactModal').modal('show');
            },
            error:function(e){
                document.getElementById("spinner").style.display = "none";
                console.log(e);
                // $('#contactModal').modal('show');
                // // $('#modal_message_account').text(e);
                // $('contact_submit').trigger("reset");
                // $('#modal_message_contact').text("Sorry, an error occured!");
                // document.getElementById("modal_message_contact").classList.add('text-danger');
            },
        });
        
        
    });
});
