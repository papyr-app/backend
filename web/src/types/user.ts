export interface User {
    id: string,
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

export interface UpdateUser {
    first_name: string;
    last_name: string;
}

enum RoleType {
  User = "USER",
  Admin = "ADMIN",
}
