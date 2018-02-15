# Mail Man

Hey there!
This project will help you spread some mails around with a simple RestFUL API.

## For whom?
Anyone who already has a SMTP server and whouldn't want to pay for third-party services such as Mailgun or Sendgrid.

## Why?

Sometimes you just need to be able to let your users send a mail with a click of a button. But on some occasions, that wouldn't be so simple to implement.

1. You may have a static website that doesn't have any SMTP logic.
2. You might have a full-scale application that has it's own SMTP integration, but it has it's own rules that you'd like to bypass.

Mail Man would let you define your own HTML files as templates for mailing. You can embed parameters inside of that HTML and sent their values on your request.

I'm free to use! Just rememeber to credit.

### 


### Prerequisites / Deployment 
If you wish to install this as a standalone server, [just contact me](mailto:admin@noamyg.com) for help.

If you wish to make changes, you'll have to get [Python](https://www.python.org/) 3.6.4 or above installed. Then:
1. Make sure to configure your organization's SMTP server in a config.xml file. You may use config.example.xml for reference.
2. If you made changes to the code, you might want to edit app.spec. [See here](https://pythonhosted.org/PyInstaller/spec-files.html).
3. No changes to the spec file needed? Good! just run "pyinstaller app.spec".
4. After pyinstaller is done, your app is ready inside of disk folder.
5. You may run app.exe with a parameter (the name of the connection inside config.xml) or use NSSM to install as a service.


### Example POST request

```javascript
            $.ajax({
                url: 'http://**ServerDNSOrIP**:5000/sendMail',
                type: 'post',
                contentType: 'application/json; charset=utf-8',
                success: function (data){
                    //Do something when you're done;
                },
                data: JSON.stringify(
                    {
                        "t" : "message", //Name of the template you're using
                        "to" : "employee@company.com",
                        "cc" : "pm@company.com",
                        "sp" : { //Subject parameters (embedded inside the HTML <subject> tag)
                            "TaskName" : "A New Task"
                        },
                        "bp" : { //Body parameters (embedded inside of the HTML body)
                            "TaskDescription" : "Develop A Thingy"
                        }
                    }
                )
            })
```

Please refer to message.html to see how parameters are set. 

### Uploading new templates
You can either add .html files manually or upload them. Just refer to http://YourMailManServer:5000/templates.