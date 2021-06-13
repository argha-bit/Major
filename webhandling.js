$('#myForm').on('submit', function(e){
    e.preventDefault();
    var data = $(this).serialize();
    console.log(data)
    let url = 'http://localhost:8080/userdataupload';
    $.ajax({
        url:url,
        type: "POST",
        data: data,
        success : function(response) {
            alert("Successfully Registered");
            window.location='login.html'
            
            
        },
        error: function(){
            alert("Failed");
        }
    })
})


$('#loginForm').on('submit', function(e){
    e.preventDefault();
    var loginData = $(this).serialize();
    console.log(loginData)
    let url = 'http://localhost:8080/authenticate';
    $.ajax({
        url:url,
        type: "POST",
        data: loginData,
        success : function(response) {
            console.log(response.Name);
            
            localStorage.setItem('id',response._id);
            localStorage.setItem('email',response.email);
            localStorage.setItem('Name',response.Name);
            localStorage.setItem('Live',response.live);

            alert(`Welcome ${localStorage.getItem(`Name`)}`);
            window.location = 'collect_samples.html'
            
        },
        error: function(response){
            console.log(response);
            alert("Login Failed ");
            window.location.reload();
        }
    })
})