export interface User {
    _id: string,
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password_hash?: string;
    role: RoleType;
    created_at: Date;
    last_updated: Date;
    last_login: Date;
}

export interface RegisterUser {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password: string;
}

export interface LoginUser {
    username: string;
    password: string;
}

export interface UpdateUser {
    first_name: string;
    last_name: string;
}

enum RoleType {
  User = "USER",
  Admin = "ADMIN",
}
