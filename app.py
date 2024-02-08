import streamlit as st
import subprocess  # Import subprocess to call another script

# Hard-coded user credentials
expected_username = "sendengage"
expected_password = "SEpass1!"

# Simple login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Placeholder for your actual logic to collect domain, hostname, and IP address
# Here you should replace these strings with the actual user input or logic to obtain these values
domain = "your_domain.com"
hostname = "your_hostname"
ip_address = "your_ip_address"

# Check credentials and call create_dns_cloudflare.py if correct
if st.button('Login'):
    if username == expected_username and password == expected_password:
        st.success("You're logged in.")

        # Constructing the command to call create_dns_cloudflare.py with arguments
        command = ["python", "create_dns_cloudflare.py", domain, hostname, ip_address]

        # Using subprocess.run to execute the command
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            # Success
            st.success("DNS record created successfully: " + result.stdout)
        else:
            # Error
            st.error(f"Failed to create DNS record: {result.stderr}")

    else:
        st.error("Incorrect username or password.")

# Displaying the fields for demonstration, remove or replace with actual logic in your app
st.write("Field 1:", domain)
st.write("Field 2:", hostname)
st.write("Field 3:", ip_address)
