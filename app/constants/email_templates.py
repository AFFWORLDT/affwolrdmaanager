EMAIL_VERIFICATION_MAIL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallet Payout Processed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .logo {
            max-width: 200px;
            margin: 20px auto;
        }
        .message {
            margin: 20px;
        }
    </style>
</head>
<body>
    <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPq18YtzNLt1uRj6qZwFrfWX2DXgSintiMEvNbfbLt7ahXWmJoWzfoUo9f8c_L0vzFyGaZQbu6o3KswBsW1owQosHAVGIAxcrRseh0RNhFXHT2WPUmYa94h6X0AgFdltTGy-HUIgvaCyEo29IwNWRXmA5nPPBZT9mFWD9CVlm96R2DF5mabMEuBPLGHtwj/s1100/Screenshot_2023-08-16-11-24-12-64_7352322957d4404136654ef4adb64504.jpg" alt="Logo" class="logo">
    <div class="message">
        <h1>Hi %s</h1>
            <p style="font-size: 14px;">Please click on the link below to verify your email :) </p> <br>
            <p> <b>Link will expire in 5 minutes </b></p>
            <h3><a href="%s">Verify Email</a><h3>
            <p style="color:purple;">Thank you for using our services!</p>
        </div>
</body>
</html>
"""
EMAIL_VERIFICATION_SUBJECT = "Verify your email - Affworld Tech."


EMAIL_RESET_PASSWORD_MAIL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wallet Payout Processed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }
        .logo {
            max-width: 200px;
            margin: 20px auto;
        }
        .message {
            margin: 20px;
        }
    </style>
</head>
<body>
    <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhPq18YtzNLt1uRj6qZwFrfWX2DXgSintiMEvNbfbLt7ahXWmJoWzfoUo9f8c_L0vzFyGaZQbu6o3KswBsW1owQosHAVGIAxcrRseh0RNhFXHT2WPUmYa94h6X0AgFdltTGy-HUIgvaCyEo29IwNWRXmA5nPPBZT9mFWD9CVlm96R2DF5mabMEuBPLGHtwj/s1100/Screenshot_2023-08-16-11-24-12-64_7352322957d4404136654ef4adb64504.jpg" alt="Logo" class="logo">
    <div class="message">
        <h1>Hi %s</h1>
            <p style="font-size: 14px;">Please click on the link below to reset your password :) </p> <br>
            <p> <b>Link will expire in 5 minutes </b></p>
            <h3><a href="%s">Reset Password</a><h3>
            <p style="color:purple;">Thank you for using our services!</p>
        </div>
</body>
</html>
"""
EMAIL_RESET_PASSWORD_SUBJECT = "RESET PASSWORD - Affworld Tech."

