import tkinter as tk
import smtplib
import imaplib
import email

def send_email():
    """Send an email."""
    # Fill in the necessary details
    sender_email = "sawerkit23@gmail.com"
    sender_password = "samuelbefikadu123."
    recipient_email = to_entry.get()
    subject = subject_entry.get()
    message = message_text.get("1.0", tk.END)

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Compose the email
        email_content = f"Subject: {subject}\n\n{message}"

        # Send the email
        server.sendmail(sender_email, recipient_email, email_content)
        server.quit()

        # Display success message
        status_label.config(text="Email sent successfully!", fg="green")
    except Exception as e:
        # Display error message
        status_label.config(text="Failed to send email.", fg="red")
        print(str(e))

def show_inbox():
    """Show the inbox page."""
    inbox_window = tk.Toplevel(window)
    inbox_window.title("Inbox")

    # Fill in the necessary details
    email_address = "your_email@example.com"
    email_password = "your_password"

    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL("imap.example.com")
        mail.login(email_address, email_password)
        mail.select("inbox")

        # Search for email messages
        result, data = mail.search(None, "ALL")
        email_ids = data[0].split()

        # Create a listbox to display the email subjects
        listbox = tk.Listbox(inbox_window, width=80)
        listbox.pack()

        for email_id in email_ids:
            result, data = mail.fetch(email_id, "(RFC822)")
            raw_email = data[0][1]
            email_message = email.message_from_bytes(raw_email)

            subject = email_message["Subject"]
            sender = email_message["From"]
            listbox.insert(tk.END, f"From: {sender} | Subject: {subject}")
            listbox.bind("<Double-Button-1>", lambda event, email_id=email_id: show_email_details(mail, email_id))

        mail.close()
        mail.logout()
    except Exception as e:
        print(str(e))

def show_email_details(mail, email_id):
    """Show the details of an email."""
    email_window = tk.Toplevel(window)
    email_window.title("Email Details")

    try:
        # Fetch the email details
        result, data = mail.fetch(email_id, "(RFC822)")
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # Extract necessary details
        subject = email_message["Subject"]
        sender = email_message["From"]
        recipient = email_message["To"]
        date = email_message["Date"]

        # Create labels to display the details
        subject_label = tk.Label(email_window, text=f"Subject: {subject}")
        subject_label.pack()

        sender_label = tk.Label(email_window, text=f"From: {sender}")
        sender_label.pack()

        recipient_label = tk.Label(email_window, text=f"To: {recipient}")
        recipient_label.pack()

        date_label = tk.Label(email_window, text=f"Date: {date}")
        date_label.pack()

        # Extract the email body
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("UTF-8")
                    break
        else:
            body = email_message.get_payload(decode=True).decode("UTF-8")

        # Create a text widget to display the email body
        body_text = tk.Text(email_window, width=80, height=20)
        body_text.pack()
        body_text.insert(tk.END, body)

    except Exception as e:
        print(str(e))

# Create the main window
window = tk.Tk()
window.title("Mail Application")

# Create input fields for recipient, subject, and message
to_label = tk.Label(window, text="To:")
to_label.pack()
to_entry = tk.Entry(window, width=50)
to_entry.pack()

subject_label = tk.Label(window, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(window, width=50)
subject_entry.pack()

message_label = tk.Label(window, text="Message:")
message_label.pack()
message_text = tk.Text(window, width=50, height=10)
message_text.pack()

# Create a button to send the email
send_button = tk.Button(window, text="Send", command=send_email)
send_button.pack()

# Create abutton to show the inbox
inbox_button = tk.Button(window, text="Inbox", command=show_inbox)
inbox_button.pack()

# Create a label for displaying the status
status_label = tk.Label(window, text="")
status_label.pack()

# Start the main event loop
window.mainloop()