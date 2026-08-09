from src.servicenow import create_incident


response = create_incident(
    short_description="VPN not connecting",
    description="User is unable to connect to the company VPN.",
    category="network",
    priority="2",
    assignment_group=""
)

print("Status Code:", response.status_code)

print("\nResponse Headers:")
print(response.headers)

print("\nResponse Body:")
print(response.text)