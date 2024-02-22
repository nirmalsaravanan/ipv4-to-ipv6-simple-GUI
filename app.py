from flask import Flask, render_template, request
import ipaddress  # Import the ipaddress module

app = Flask(__name__)

def convert_ipv4_to_ipv6(ipv4_address):
    try:
        ipaddress.IPv4Address(ipv4_address)
        ipv6_address = ipaddress.IPv6Address(f"::ffff:{ipv4_address}").compressed
        return ipv6_address, None
    except ipaddress.AddressValueError:
        error_message = "Invalid IPv4 address."
        return None, error_message

def convert_ipv6_to_ipv4(ipv6_address):
    try:
        ip6_obj = ipaddress.IPv6Address(ipv6_address)
        if ip6_obj.ipv4_mapped:
            ipv4_address = ip6_obj.ipv4_mapped.exploded
            return ipv4_address, None
        else:
            error_message = "The provided IPv6 Address is not IPv4-mapped."
            return None, error_message
    except ipaddress.AddressValueError:
        error_message = "Invalid IPv6 address."
        return None, error_message

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error_message = None

    if request.method == 'POST':
        choice = request.form['conversionChoice']
        ip_address = request.form['ipAddress']

        if choice == "1":
            result, error_message = convert_ipv4_to_ipv6(ip_address)
        elif choice == "2":
            result, error_message = convert_ipv6_to_ipv4(ip_address)

    return render_template('index.html', result=result, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
