from django.test import TestCase

# Create your tests here.


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")
        if User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        if User.objects.filter(username=data["username"]).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        # Generate a 6-digit OTP
        otp = str(random.randint(100000, 999999))
        email = validated_data["email"]

        # Save OTP to the database
        EmailOTP.objects.update_or_create(
            email=validated_data["email"],
            defaults={"otp": otp, "created_at": timezone.now()}
        )
 
        # Send OTP via email

        subject = "Your OTP Code"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #444;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .email-container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                }}
                .header {{
                    color: #2c3e50;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 15px;
                    margin-bottom: 20px;
                }}
                .otp-box {{
                    background-color: #f8f9fa;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 20px 0;
                    text-align: center;
                }}
                .otp {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #3498db;
                    letter-spacing: 3px;
                    margin: 10px 0;
                }}
                .note {{
                    font-size: 14px;
                    color: #7f8c8d;
                    margin-top: 25px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 15px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #95a5a6;
                }}
                .button {{
                    background-color: #3498db;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 4px;
                    display: inline-block;
                    margin: 15px 0;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h2>Verification Code For exedu - Hybrid AI Education</h2>
                </div>

                <p>Hello,</p>
                <p>Here's your One-Time Password (OTP) for verification:</p>

                <div class="otp-box">
                    <div class="otp">{otp}</div>
                    <small>This code expires in 5 minutes</small>
                </div>

                <p class="note">
                    <strong>Note:</strong> For your security, please don't share this code with anyone.
                    If you didn't request this code, you can safely ignore this email.
                </p>

                <div class="footer">
                    <p>© {datetime.datetime.now().year} exedu. All rights reserved.</p>
                    <p>Need help? <a href="mailto:exeduone@gmail.com">Contact our support team</a></p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        New Verification Code

        Hello,

        As requested, here's your new One-Time Password (OTP) for verification:
        {otp}

        This code expires in 1 minute.

        Note: For your security, please don't share this code with anyone.
        If you didn't request this code, you can safely ignore this email.

        © {datetime.datetime.now().year} YourCompany. All rights reserved.
        Need help? Contact our support team at exeduone@gmail.com
        """
        msg = EmailMultiAlternatives(
            subject, text_content, "no-reply@gmail.com", [email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        return {"email": validated_data["email"], "message": "OTP sent to email"}

