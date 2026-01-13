export interface Task {
  id: string;
  title: string;
  description?: string;
  status: 'pending' | 'completed';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  created_at: string;
  updated_at: string;
  categories?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly';
}

export interface TaskCreate {
  title: string;
  description?: string;
  status: 'pending';
  priority: 'low' | 'medium' | 'high';
  due_date?: string;
  categories?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly';
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: 'pending' | 'completed';
  priority?: 'low' | 'medium' | 'high';
  due_date?: string;
  categories?: string[];
  is_recurring?: boolean;
  recurrence_pattern?: 'daily' | 'weekly' | 'monthly';
}