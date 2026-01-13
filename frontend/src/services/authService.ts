import { jwtDecode } from 'jwt-decode'; // Import jwt_decode

export const getJwtFromHash = (): string | null => {
  if (typeof window !== 'undefined') {
    const hash = window.location.hash;
    if (hash) {
      const params = new URLSearchParams(hash.substring(1));
      return params.get('access_token');
    }
  }
  return null;
};

export const storeJwt = (token: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('jwt', token);
    try {
      const decodedToken: any = jwtDecode(token);
      if (decodedToken && decodedToken.sub) { // Assuming 'sub' contains the user_id
        localStorage.setItem('user_id', decodedToken.sub);
      }
    } catch (error) {
      console.error("Failed to decode JWT and extract user_id:", error);
    }
  }
};

export const getStoredJwt = (): string | null => {
  if (typeof window !== 'undefined') {
    const jwt = localStorage.getItem('jwt');
    return jwt;
  }
  return null;
};

export const removeStoredJwt = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('jwt');
    localStorage.removeItem('user_id'); // Also remove user_id on logout
  }
};

// Function to check if the token is expired
export const isTokenExpired = (token: string): boolean => {
  try {
    const decodedToken: any = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decodedToken.exp < currentTime;
  } catch (error) {
    console.error("Error decoding token:", error);
    return true; // If we can't decode the token, treat it as expired
  }
};

// Function to check if the stored token is valid
export const isStoredTokenValid = (): boolean => {
  const token = getStoredJwt();
  if (!token) {
    return false;
  }
  return !isTokenExpired(token);
};
