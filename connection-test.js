const API_BASE_URL = "http://localhost:8000";

async function testConnection() {
    console.log("Testing connection to backend...");
    
    try {
        // Test basic connectivity
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();
        
        if (response.ok) {
            console.log("✅ Successfully connected to backend!");
            console.log("Response:", data);
            
            // Test API endpoints
            console.log("\nTesting API endpoints...");
            
            // Test auth endpoints
            try {
                const tokenResponse = await fetch(`${API_BASE_URL}/api/token`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: 'username=test@example.com&password=testpass'
                });
                
                console.log(`Token endpoint status: ${tokenResponse.status}`);
                
                if (tokenResponse.status === 422) {
                    console.log("✅ Token endpoint accessible (expected 422 for missing data)");
                } else {
                    console.log("⚠️ Token endpoint returned unexpected status:", tokenResponse.status);
                }
            } catch (error) {
                console.error("❌ Error testing token endpoint:", error);
            }
            
            // Test signup endpoint
            try {
                const signupResponse = await fetch(`${API_BASE_URL}/api/signup`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({})
                });
                
                console.log(`Signup endpoint status: ${signupResponse.status}`);
                
                if (signupResponse.status === 422) {
                    console.log("✅ Signup endpoint accessible (expected 422 for missing data)");
                } else {
                    console.log("⚠️ Signup endpoint returned unexpected status:", signupResponse.status);
                }
            } catch (error) {
                console.error("❌ Error testing signup endpoint:", error);
            }
            
        } else {
            console.error("❌ Backend returned error:", response.status, data);
        }
    } catch (error) {
        console.error("❌ Failed to connect to backend:", error.message);
        console.log("\nTroubleshooting steps:");
        console.log("1. Make sure the backend server is running on http://localhost:8000");
        console.log("2. Check if there are any firewall rules blocking the connection");
        console.log("3. Verify the API_BASE_URL in your frontend .env.local file");
    }
}

// Run the test
testConnection();