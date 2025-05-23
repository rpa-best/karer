export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface Token {
  access: string | null;
  refresh: string | null;
}

