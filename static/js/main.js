// --------- sidebar ---------
$(document).ready(function()  {
    $(".x-mark").click(function() {
        $(".sidebar-main").hide();
    });
    $(".nav-on").click(function() {
        $(".sidebar-main").show();
    });
});


document.getElementById('togglePassword').addEventListener('click', function() {
    var passwordField = document.getElementById('passwordField');
    var eyeIcon = document.getElementById('togglePassword');

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        eyeIcon.classList.remove('bi-eye');
        eyeIcon.classList.add('bi-eye-slash');
    } else {
        passwordField.type = 'password';
        eyeIcon.classList.remove('bi-eye-slash');
        eyeIcon.classList.add('bi-eye');
    }
});


