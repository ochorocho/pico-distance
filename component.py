def logo():
    return """
        <svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" width="50" height="50" viewBox="0 0 88.1 88.1">
            <path fill="#901917" d="M-1-1h89v89H-1z"/>
            <path fill="#901917" stroke="#901917" stroke-miterlimit="10" stroke-width="3" d="M31 19h8m2 25v-7"/>
            <g style="font-size:70.48px;line-height:1.25;stroke-width:1.762">
                <path d="m61 24 5 8 1 12-1 11-5 8q-3 4-8 5-4 2-10 2-5 0-9-2-5-1-8-5l-5-8-1-11 1-12 5-8q3-4 8-5 4-2 9-2 6 0 10 2 5 1 8 5zm-1 20q0-10-4-16-5-5-12-5-8 0-13 5-4 6-4 16t4 15q5 5 13 5 7 0 12-5 4-5 4-15z" aria-label="O" style="fill:#c6c6c6"/>
            </g>
        </svg>
    """

def favicon():
    return """
        <link rel="shortcut icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20xml%3Aspace%3D%22preserve%22%20width%3D%2250%22%20height%3D%2250%22%20viewBox%3D%220%200%2088.1%2088.1%22%3E%3Cpath%20fill%3D%22%23901917%22%20d%3D%22M-1-1h89v89H-1z%22%2F%3E%3Cpath%20fill%3D%22%23901917%22%20stroke%3D%22%23901917%22%20stroke-miterlimit%3D%2210%22%20stroke-width%3D%223%22%20d%3D%22M31%2019h8m2%2025v-7%22%2F%3E%3Cg%20style%3D%22font-size%3A70.48px%3Bline-height%3A1.25%3Bstroke-width%3A1.762%22%3E%3Cpath%20d%3D%22m61%2024%205%208%201%2012-1%2011-5%208q-3%204-8%205-4%202-10%202-5%200-9-2-5-1-8-5l-5-8-1-11%201-12%205-8q3-4%208-5%204-2%209-2%206%200%2010%202%205%201%208%205zm-1%2020q0-10-4-16-5-5-12-5-8%200-13%205-4%206-4%2016t4%2015q5%205%2013%205%207%200%2012-5%204-5%204-15z%22%20aria-label%3D%22O%22%20style%3D%22fill%3A%23c6c6c6%22%2F%3E%3C%2Fg%3E%3C%2Fsvg%3E">
    """

def css():
    return """
       <style>
            :root {
                --grey: #c6c6c6;
                --green: #79a548;
                --white: #ffffff;
            }

            body, html {
                font-family: arial;
                padding: 0;
                margin: 0
            } 
            .header {
                background-color: var(--grey);
                display: flex;
            }
            .header svg {
                margin-right: 2rem;
            }

            .header h1 {
                font-size: 1.2rem;
            }
            .content {
                padding: 1rem;
            }

            form {
                width: 20%;
                min-width: 300px;
                max-width: 600px;
                margin: auto;
            }
            .submit {
                text-align: right;
            }
            input[name="password"] {
                display: block;
                width: 100%;
                box-sizing: border-box;
                padding: .2rem 1rem;
            }
            hr {
                border: 1px solid var(--grey);
            }
            label {
                padding: 4px 0;
                display: inline-block;
            }
            [type="submit"] {
                border: 0;
                padding: 4px 20px;
                background-color: var(--green);
                color: var(--white);
            }
            p {
                margin: 4px 0;
            }
       </style>
    """

def page() -> str:
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            {2}
            <meta charset="utf-8">
            <title>Pico W - Distance Sensor</title>
            {1}
        </head>
        <body>
            <div class="header">
                {0}
                <h1>Pico W - Distance Sensor Setup</h1>
            </div>
            <div class="content">
                #content#
            </div>
        </body>
        </html>    
    """.format(logo(), css(), favicon())

def form(ssids):
    formRadio = '<p>Select a Wifi:</p>'

    while len(ssids):
        ssid = ssids.pop(0)
        formRadio += """<p><label><input type="radio" name="ssid" required value="{0}" />{0}</label></p>""".format(ssid)

    return """
        <form action="configure" method="post">
            {0}
            <p>
                <label for="password">
                    Password:
                </label>
                <input name="password" type="password" required />
            </p>
            <hr>
            <p class="submit">
                <input type="submit" value="Submit" required/>
            </p>
        </form>
    """.format(formRadio)