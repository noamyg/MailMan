# Mail Man

Hey there!
This project will help you spread some mails around with a simple RestFUL API.

## For whom?
Anyone who already has a SMTP server and whouldn't want to pay for third-party services.

## Why?

Sometimes you just need to be able to let your users send a mail with a click of a button.

1. You may have a static website that doesn't have any SMTP logic (or no back-end at all).
2. You might have a full-scale application that has it's own SMTP integration, but it has it's own rules (styling or event-triggered) that you'd wish to bypass.

Mail Man would let you define your own HTML files as templates for mailing. You can embed parameters inside of that HTML and sent their values on your request.

I'm free to use! Just rememeber to credit.

### 


### Installation
If you wish to install this as a standalone server, [just contact me](mailto:admin@noamyg.com) for help.

If you wish to make changes, you'll have to get [Python](https://www.python.org/) 3.6.4 or above installed. Then:
1. Install with `pip install -r requirements.txt`.
2. Make sure to configure your organization's SMTP server in a `config.xml` file. You may use `config.example.xml` for reference.
3. Run app.py with the the name of your SMTP server as first param, and optional port (default: 5000) as second param (i.e., `python app.py Gmail [8080]`).

### Deployment

1. If you made changes to the code, you might want to edit `app.spec`. [See here](https://pythonhosted.org/PyInstaller/spec-files.html).
2. No changes to the spec file needed? Good! just run `pyinstaller app.spec`.
3. After pyinstaller is done, your app is ready inside of `dist` folder.
4. You may run `app.exe` with the server name and port params or use [NSSM](https://nssm.cc/usage) to install it as a service.
5. To run the server on HTTPS, add a `server.crt` and `server.key` files to `certificates` folder.


### Example POST request

```javascript
            $.ajax({
                url: 'http://**ServerDNSOrIP**:**Port**/sendMail',
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
                        "bcc" : "secret@company.com",
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
You can either add .html files manually or upload them. Just refer to http://**ServerDNSOrIP**:**Port**/templates.