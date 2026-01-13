// frontend/src/app/types/user.ts

import { Task } from './task';

export interface User {
    id: string;
    email: string;
    name: string;
    created_at: string;
    tasks: Task[];
}

export interface UserCreate {
    email: string;
    name: string;
}
